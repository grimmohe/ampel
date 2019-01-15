from tensor.model import Action, Event
from mentor.model import Car

"""
"""
class Mentor(object):

    def __init__(self, stepSize=0.1):
        self.stack = []
        self.stepSize = stepSize

    def getAction(self, event=Event()):
        print("mentor: time passed", event.timePassed)
        print("mentor: add event", event.sourceId, event.destinationId, event.distance)

        self._updateTime(event.timePassed)
        self._addCar(event)
        action = self._createAction()

        return action

    def _addCar(self, event):
        c = Car()
        c.sourceId = event.sourceId
        c.destinationId = event.destinationId
        c.timeLeft = event.distance

        self.stack.append(c)

    def _createAction(self):
        action = Action()
        timeLeft = None

        self.stack.sort(key=lambda car: car.timeLeft)

        if len(self.stack) and self.stack[0].timeLeft < self.stepSize * 2:
            car = self.stack.pop(0)

            action.sourceId = car.sourceId
            action.destinationId = car.destinationId
            timeLeft = car.timeLeft

        else:
            action.sourceId = -1
            action.destinationId = -1

        print("mentor: set green for ", action.sourceId, action.destinationId, timeLeft)

        return action

    def _updateTime(self, timePassed):
        for car in self.stack:
            car.timeLeft -= timePassed
