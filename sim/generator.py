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

        self._buidlCrossings(model, numNodes)
        self._buildStreets(model, minTravelTime, maxTravelTime)
        self._buildCars(model, numCars, minTravelTime)

        return model

    def _buildStreets(self, model=Model(), minTravelTime=0, maxTravelTime=0):
        targeted = []
        streetId = 0

        for srcCrossing in model.crossings:
            while len(srcCrossing.connectingCrossings) < 2:
                connectCrossing = model.crossings[self.getNextFactor(len(model.crossings) - 1)]
                if connectCrossing.crossingId == srcCrossing.crossingId \
                or len(connectCrossing.connectingCrossings) == 2:
                    continue

                srcCrossing.connectingCrossings.append(connectCrossing)
                connectCrossing.connectingCrossings.append(srcCrossing)

                time = minTravelTime + self.getNextFactor(maxTravelTime - minTravelTime)
                model.streets.append(Street(streetId, [srcCrossing, connectCrossing], time))

                streetId += 1

    def _buidlCrossings(self, model=Model(), numNodes=0):
        for crossingId in range(numNodes):
            crossing1 = Crossing(crossingId)
            crossing2 = Crossing(crossingId)

            crossing1.otherCrossing = crossing2
            crossing2.otherCrossing = crossing1

            model.crossings.append(crossing1)
            model.crossings.append(crossing2)

    def _buildCars(self, model=Model(), numCars=0, minTravelTime=0):

        for carId in range(numCars):
            source = model.crossings[self.getNextFactor(len(model.crossings) - 1)]
            destination = source.connectingCrossings[0]

            model.cars.append(
                Car(
                    carId,
                    source,
                    destination,
                    minTravelTime / (carId + 1)
                )
            )

    """
    returns value between 0 and max
    """
    def getNextFactor(self, maxIndex = 1):
        self._factorCount += 1

        a = int(self.formId / self._factorCount)

        return a % max(1, maxIndex+1)
