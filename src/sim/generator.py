from sim.model import Model, Street, Car
import random
import math

"""
"""
class Generator:
    def __init__(self, formId = 123456):
        self.formId = formId
        self._factorCount = 0

    def buildModel(self, numNodes=10, minTravelTime=10, maxTravelTime=60, numCars=10):
        model = Model()
        targeted = []
        streetId = 0

        for nodeId in range(numNodes):
            connected = [nodeId]
            for _ in range(self._getNextFactor(2)+2):
                time = minTravelTime + self._getNextFactor(maxTravelTime - minTravelTime)

                target = nodeId
                while connected.count(target) > 0 or targeted.count(target) > 3:
                    target = self._getNextFactor(numNodes - 1)
                connected.append(target)
                targeted.append(target)

                model.streets.append(Street(streetId, nodeId, target, time))
                streetId+=1

        for carId in range(numCars):
            streetId = self._getNextFactor(numNodes - 1)

            possibleDestinations = [s for s in model.streets if s.id == streetId]
            destination = possibleDestinations[self._getNextFactor(len(possibleDestinations) - 1)]

            model.cars.append(
                Car(
                    carId,
                    destination.id,
                    destination.destination,
                    self._getNextFactor(destination.distance) + carId / 10000.0
                )
            )

        return model

    """
    returns value between 0 and max
    """
    def _getNextFactor(self, maxIndex = 1):
        self._factorCount += 1

        a = int(self.formId / self._factorCount)

        return a % max(1, maxIndex+1)
