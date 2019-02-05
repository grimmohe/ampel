import json

"""
"""
class Model(object):
    def __init__(self):
        self.streets = []
        self.cars = []
        self.crossings = []

    def __str__(self):
        return json.dumps(self, default=lambda o: o.to_json(), indent=4)

    def to_json(self):
        return {
            'streets': self.streets,
            'cars': self.cars,
            'crossings': self.crossings
        }

"""
"""
class Street(object):
    def __init__(self, id, connectingCrossings=[], dist=.0):
        self.streetId = id
        self.crossings = connectingCrossings
        self.distance = dist

    def __str__(self):
        return json.dumps(self, default=lambda o: o.to_json(), indent=4)

    def to_json(self):
        return {
            'streetId': self.streetId,
            'crossings': [str(c.crossingId) + ":" + str([cc.crossingId for cc in c.connectingCrossings]) for c in self.crossings],
            'distance': self.distance
        }

"""
"""
class Car(object):
    def __init__(self, id, sourceCrossing, destinationCrossing, distance):
        self.carId = id
        self.sourceCrossing = sourceCrossing
        self.destinationCrossing = destinationCrossing
        self.distance = distance

    def __str__(self):
        return json.dumps(self, default=lambda o: o.to_json(), indent=4)

    def to_json(self):
        return {
            'carId': self.carId,
            'sourceCrossing': self.sourceCrossing.crossingId,
            'destinationCrossing': self.destinationCrossing.crossingId,
            'distance': self.distance
        }

"""
"""
class Crossing(object):
    def __init__(self, crossingId):
        self.crossingId = crossingId
        self.green = False
        self.otherCrossing = None
        self.connectingCrossings = []

    def __str__(self):
        return json.dumps(self, default=lambda o: o.to_json(), indent=4)

    def to_json(self):
        return {
            'crossingId': self.crossingId,
            'green': self.green,
            'otherCrossing': self.otherCrossing.crossingId,
            'connectingCrossings': [c.crossingId for c in self.connectingCrossings]
        }
