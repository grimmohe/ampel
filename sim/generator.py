from sim.model import Model, Street, Car, Crossing
import random
import math

"""
"""
class Generator:
    def __init__(self, formId=123456):
        self.formId = formId
        self._factorCount = 0

    def buildModel(self, numNodes=10, minTravelTime=10, maxTravelTime=60, numCars=10):
        model = Model()

        self._buildStreets(model, numNodes, minTravelTime, maxTravelTime)
        self._buidlCrossings(model, numNodes)
        self._buildCars(model, numNodes, numCars)

        return model

    def _buildStreets(self, model=Model(), numNodes=0, minTravelTime=0, maxTravelTime=0):
        targeted = []
        streetId = 0

        for nodeId in range(numNodes): #TODO Einbahnstraßen ausbauen
            connected = [nodeId]
            for _ in range(self.getNextFactor(1)+3):
                time = minTravelTime + self.getNextFactor(maxTravelTime - minTravelTime)

                target = nodeId
                while connected.count(target) > 0 or targeted.count(target) > 3:
                    target = self.getNextFactor(numNodes - 1)
                connected.append(target)
                targeted.append(target)

                model.streets.append(Street(streetId, nodeId, target, time))
                streetId += 1

    def _buidlCrossings(self, model=Model(), numNodes=0):
        for nodeId in range(numNodes):
            destinations = [s.destinationId for s in model.streets if s.sourceId == nodeId]
            distances = []

            for destination1 in destinations:
                max = {'sourceId': destination1, 'destinationId': 0, 'distance': 0}
                for destination2 in [d for d in destinations if d != destination1]:
                    d = self._getDistance(model, destination1, destination2, nodeId)
                    if d > max['distance']:
                        max['destinationId'] = destination2
                        max['distance'] = d

                distances.append(max)

            distances.sort(key=lambda x: x['distance'], reverse=True)

            crossing1 = Crossing(nodeId)
            crossing1.connectingNodes.append(distances[0]['sourceId'])
            crossing1.connectingNodes.append(distances[0]['destinationId'])

            leaving = [d for d in destinations if crossing1.connectingNodes.count(d) == 0]

            crossing2 = Crossing(nodeId)
            crossing2.connectingNodes.extend(leaving)

            model.crossings.append(crossing1)
            model.crossings.append(crossing2)

    def _buildCars(self, model=Model(), numNodes=0, numCars=0):

        for carId in range(numCars):
            nodeId = self.getNextFactor(numNodes - 1)

            streets = [s for s in model.streets if s.sourceId == nodeId]
            street = streets[self.getNextFactor(len(streets) - 1)]

            model.cars.append(
                Car(
                    carId,
                    street.sourceId,
                    street.destinationId,
                    self.getNextFactor(street.distance) + carId / 10000.0
                )
            )

    """
    returns value between 0 and max
    """
    def getNextFactor(self, maxIndex = 1):
        self._factorCount += 1

        a = int(self.formId / self._factorCount)

        return a % max(1, maxIndex+1)

    def _getDistance(self, model=Model(), fromNode=0, toNode=0, excludeNode=0):
        routes = {}
        routes[excludeNode] = []
        routes[fromNode] = [fromNode]
        self.__travel(model, routes, fromNode)

        if toNode not in routes:
            raise "wtf"

        return len(routes[toNode])

    def __travel(self, model, routes, current):
        route = routes[current]
        streets = [s for s in model.streets if s.sourceId == current and route.count(s.destinationId) == 0]

        for street in streets:
            if street.destinationId not in routes or len(routes[street.destinationId]) > len(route) + 1:
                newRoute = route[:]
                newRoute.append(street.destinationId)
                routes[street.destinationId] = newRoute
                self.__travel(model, routes, street.destinationId)

