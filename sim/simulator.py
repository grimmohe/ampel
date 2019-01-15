import time
import sys
from sim.model import Car, Street, Model
from sim.generator import Generator
from tensor.model import Action, Event

"""
"""
class Simulator(object):

    def __init__(self, model = Model(), generator = Generator(), stepSize=0.1):
        self.model = model
        self.generator = generator
        self.error = .0
        self.stepSize = stepSize
        self.events = []

    """
    Erzeugt für alle Fahrzeuge ein initiales Event.
    """
    def init(self):
        for car in self.model.cars:
            e = Event()
            e.carId = car.carId
            e.sourceId = car.sourceId
            e.destinationId = car.destinationId
            e.distance = car.distance
            e.timePassed = 0

            self.events.append(e)

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
        timePassed = float(0)
         # first check event stack
        if len(self.events) == 0:
            # time passes to next event
            timePassed = self._getNextEventDistance()

        timePassed += 0.001
        self._moveCars(timePassed) # adds events

        if len(self.events):
            event = self.events.pop(0)
        else:
            event = Event()

        event.timePassed = timePassed

        print("sim: send event", event.sourceId, event.destinationId, event.distance, event.timePassed)

        return event

    def _getNextEventDistance(self):
        next = sys.float_info.max
        trigger_car = None

        for car in self.model.cars:
            if car.distance < next:
                next = car.distance
                trigger_car = car

        print("sim: trigger car", car.sourceId, car.destinationId, next)

        return max(0.001, min(self.stepSize, next))

    def _moveCars(self, distance=.0):
        if distance == 0:
            return

        # closer to event first
        self.model.cars.sort(key=lambda x: x.distance)

        for car in self.model.cars:
            moveTo = car.distance - distance

            # dont drive over other cars
            frontCars = [c for c in self.model.cars if c.sourceId == car.sourceId and c.destinationId == car.destinationId and c != car]
            for frontCar in frontCars:
                if frontCar.distance < car.distance and frontCar.distance + 1 > car.distance:
                    moveTo = frontCar.distance + 1

            # arrive at crossing
            if moveTo <= 0:

                if self._isGreenFor(car):
                    newStreet = self.getNextDestination(car)

                    car.sourceId = newStreet.sourceId
                    car.destinationId = newStreet.destinationId
                    car.distance = newStreet.distance + moveTo

                # wait for red lights
                else:
                    car.distance = 0
                    self.error += 1

                e = Event()
                e.carId = car.carId
                e.sourceId = car.sourceId
                e.destinationId = car.destinationId
                e.distance = car.distance

                self.events.append(e)

            else:
                car.distance = moveTo


    def getNextDestination(self, car):
        streets = [s for s in self.model.streets if s.sourceId == car.destinationId]

        return streets[self.generator.getNextFactor(len(streets) - 1)]

    def _isGreenFor(self, car):
        for crossing in self.model.crossings:
            if crossing.nodeId == car.destinationId and crossing.green and crossing.connectingNodes.count(car.sourceId):
                return True

        return False

    def _applyAction(self, action=Action()):
        crossings = [c for c in self.model.crossings if c.nodeId == action.destinationId]

        for crossing in crossings:
            crossing.green = (crossing.connectingNodes.count(action.sourceId) == 1)
            print("sim: green for", crossing.green, crossing.nodeId, crossing.connectingNodes)
