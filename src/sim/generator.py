from sim.model import Model, Street, Car
import random

"""
"""
class Generator:
    def __init__(self, formId = 123456):
        self.formId = formId

    def buildModel(self, numNodes=10, minTravelTime=10, maxTravelTime=60, numCars=10):
        model = Model()
        targeted = []

        for streetId in range(numNodes):
            connected = [streetId]
            for _ in range(self._getNextFactor(2)+1):
                time = minTravelTime + self._getNextFactor(maxTravelTime - minTravelTime)
                
                target = streetId
                while connected.count(target) > 0 or targeted.count(target) > 3:
                    target = self._getNextFactor(numNodes - 1)
                connected.append(target)
                targeted.append(target)

                model.streets.append(Street(streetId, target, time))

        for carId in range(numCars):
            streetId = self._getNextFactor(numNodes - 1)
            
            possibleDestinations = [s for s in model.streets if s.id == streetId]
            destination = possibleDestinations[self._getNextFactor(len(possibleDestinations) - 1)]

            model.cars.append(Car(carId, destination.id, destination.destination, self._getNextFactor(destination.distance)))

        return model

    """
    returns value between 0 and max
    """
    def _getNextFactor(self, max = 1):
        if max < 1:
            return 0;
        else: 
            return random.randint(0, max) #todo




