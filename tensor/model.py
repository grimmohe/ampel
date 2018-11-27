import sys

"""
"""
class Event(object):

    def __init__(self):
        self.distance = sys.float_info.max
        self.carId = 0.
        self.streetId = 0.
        self.destinantionId = 0.

"""
"""
class Action(object):

    def __init__(self):
        self.streetId = 0
        self.destinationId = 0