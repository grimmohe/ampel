import json

"""
"""
class Model(object):
    def __init__(self):
        self.streets = []
        self.cars = []
        self.crossings = []

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

"""
"""
class Street(object):
    def __init__(self, id, connectingCrossings=[], dist=.0):
        self.streetId = id
        self.crossings = connectingCrossings
        self.distance = dist

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

"""
"""
class Car(object):
    def __init__(self, id, sourceCrossing, destinationCrossing, distance):
        self.carId = id
        self.sourceCrossing = sourceCrossing
        self.destinationCrossing = destinationCrossing
        self.distance = distance

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

"""
"""
class Crossing(object):
    def __init__(self, crossingId):
        self.crossingId = crossingId
        self.green = False
        self.otherCrossing = None
        self.connectingCrossings = []
