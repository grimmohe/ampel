from tensor.model import Action, Event
from mentor.model import Car

"""
"""
class Mentor(object):

    def __init__(self):
        self.stack = []

    def getAction(self, event=Event()):
        self._updateTime(event.timePassed)
        self._addCar(event)
        action = self._createAction()
        self._cleanStack(action)

        return action


    def _addCar(self, event):
        c = Car()
        c.streetId = event.streetId
        c.destinationId = event.destinationId
        c.timeLeft = event.distance

        self.stack.append(c)

    def _cleanStack(self, action):
        self.stack = [c for c in self.stack if c.timeLeft > 0 or c.streetId != action.streetId]

    def _createAction(self):
        action = Action()

        if len(self.stack):
            self.stack.sort(key=lambda car: car.timeLeft)
            car = self.stack[0]

            action.streetId = car.streetId
            action.destinationId = car.destinationId

        else:
            action.streetId = -1
            action.destinationId = -1

        return action

    def _updateTime(self, timePassed):
        for car in self.stack:
            car.timeLeft -= timePassed
