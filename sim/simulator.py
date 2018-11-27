import time
from sim.model import Car, Street, Model
from tensor.model import Action, Event

"""
"""
class Simulator(object):

    def __init__(self, model = Model()):
        self.model = model
        self.time = time.time()

    """
    1. Signal vom Verkehrsnetz
    2. Reaktion vom Tensor

    Jeder Reaktion des Verkehrs mit Ergebnis vom Tensor folgt ein weiteres Signal.
    Nach einer Sekunde ohne Events im Verkehr folgt ein weiteres Signal an den Tensor.

    step() springt an den nächsten Zeitpunkt der ein Signal vom Verkehrsnetz erfordert.
    """
    def step(self, callbackMethod):
        event = self._getNextEvent()

        if event.distance > 1:
            event.carId = None
            event.destinantionId = None
            event.distance = 1.
            event.streetId = None

        self._moveCars(event.distance)

        timestamp = time.time()

        action = callbackMethod(event)

        self._moveCars(time.time() - timestamp)
        self._applyAction(action)


    def _getNextEvent(self):
        next = Event()

        for car in self.model.cars:
            if car.distance < next.distance:
                next.carId = car.carId
                next.streetId = car.streetId
                next.destinantionId = car.destinantionId
                next.distance = car.distance

        return next

    def _moveCars(self, distance=.0):
        self.model.cars.sort(key=lambda x: x.distance)

    def _applyAction(self, action):
        pass

