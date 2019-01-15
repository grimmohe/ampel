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
    def __init__(self, id, source, dest, dist):
        self.streetId = id
        self.sourceId = source
        self.destinationId = dest
        self.distance = dist

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

"""
"""
class Car(object):
    def __init__(self, id, sourceId, destinationId, distance):
        self.carId = id
        self.sourceId = sourceId
        self.destinationId = destinationId
        self.distance = distance

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

"""
"""
class Crossing(object):
    def __init__(self, nodeId):
        self.nodeId = nodeId
        self.green = False
        self.connectingNodes = []
