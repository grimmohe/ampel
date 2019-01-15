import sys

"""
"""
class Event(object):

    def __init__(self):
        self.distance = sys.float_info.max
        self.carId = -1
        self.sourceId = -1
        self.destinationId = -1
        self.timePassed = .0

"""
"""
class Action(object):

    def __init__(self, sourceId=0., destinationId=0.):
        self.sourceId = sourceId
        self.destinationId = destinationId