import time
import sys
from sim.model import Car, Street, Model
from sim.generator import Generator
from tensor.model import Action, Event

"""
"""
class Simulator(object):

    def __init__(self, model = Model(), generator = Generator()):
        self.model = model
        self.generator = generator
        self.time = time.time()
        self.error = .0
        self.events = []

    """
    1. Signal vom Verkehrsnetz
    2. Reaktion vom Tensor

    Jeder Reaktion des Verkehrs mit Ergebnis vom Tensor folgt ein weiteres Signal.
    Nach einer Sekunde ohne Events im Verkehr folgt ein weiteres Signal an den Tensor.

    step() springt an den nächsten Zeitpunkt der ein Signal vom Verkehrsnetz erfordert.
    """
    def step(self, callbackMethod):
        event = self._getNextEvent()
        action = callbackMethod(event)

        self._applyAction(action)

    def _getNextEvent(self):
         # first check event stack
        if len(self.events) == 0:
            # time passes to next event
            self._moveCars(self._getNextEventDistance())

        if len(self.events):
            event = self.events.pop(0)
        else:
            event = Event()
            event.timePassed = float(1)

        return event

    def _getNextEventDistance(self):
        next = sys.float_info.max

        for car in self.model.cars:
            if car.distance < next:
                next = car.distance

        if next > 1:
            next = float(1)

        return next

    def _moveCars(self, distance=.0):
        if distance == 0:
            return

        # update event time
        for event in self.events:
            event.timePassed += distance

        self.time += distance

        # closer to event first
        self.model.cars.sort(key=lambda x: x.distance)

        for car in self.model.cars:
            moveTo = car.distance - distance

            # dont drive over other cars
            frontCars = [c for c in self.model.cars if c.streetId == car.streetId and c.destinationId == car.destinationId and c != car]
            for frontCar in frontCars:
                if frontCar.distance < car.distance and frontCar.distance + 1 > car.distance:
                    moveTo = frontCar.distance + 1

            # arrive at crossing
            if moveTo <= 0:
                e = Event()
                e.carId = car.id
                e.timePassed = distance
                self.events.append(e)

                if self._isGreenFor(car):
                    newStreet = self.getNextDestination(car)
                    e.streetId = newStreet.source
                    e.destinationId = newStreet.destination
                    e.distance = newStreet.distance + moveTo

                # wait for red lights
                else:
                    e.streetId = car.streetId
                    e.destinationId = car.destinationId
                    e.distance = 0

                    self.error += 1

            else:
                car.distance = moveTo

    def getNextDestination(self, car):
        streets = [s for s in self.model.streets if s.source == car.destinationId]

        return streets[self.generator.getNextFactor(len(streets) - 1)]

    def _isGreenFor(self, car):
        for crossing in self.model.crossings:
            if crossing.nodeId == car.destinationId and crossing.green and crossing.connectingNodes.count(car.streetId):
                return True

        return False

    def _applyAction(self, action=Action()):
        crossings = [c for c in self.model.crossings if c.nodeId == action.destinationId]

        for crossing in crossings:
            crossing.green = (crossing.connectingNodes.count(action.streetId) == 1)
