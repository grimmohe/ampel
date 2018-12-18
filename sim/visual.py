import pygame
import math
import sys
from sim.model import Model, Street, Car

class Visual(object):

    def __init__(self):
        self.model = Model()
        self.width = 800
        self.height = 600

    def init(self, model):
        self.model = model

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption("Ampel AI Krams")
        pygame.mouse.set_visible(1)
        pygame.key.set_repeat(1, 30)
        self.clock = pygame.time.Clock()
        self.running = True

        self._prepareStreets()

        self.printOffset, self.printFactor = self._getPrintOffset()
        print(self.printFactor, self.printOffset)

    def _prepareStreets(self):

        self.streets = {}

        streetDict = {street.id: street for street in self.model.streets}
        crossingDict = {crossing.nodeId: crossing for crossing in self.model.crossings}

        for crossing in self.model.crossings:

            startPosition = (0,0)

            degree = 360 / len(crossing.connectingNodes)

            # do we already have one of the connected nodes?
            for streetId in crossing.connectingNodes:
                if self.streets.get(streetId):
                    startPosition = self.streets[streetId].endPosition
                    break

            for index, streetId in enumerate(crossing.connectingNodes, start=1):

                if not self.streets.get(streetId):

                    # forward
                    self.streets[streetId] = self._newInternalStreet(
                        streetDict[streetId], 
                        startPosition, 
                        self._getTargetCoords(startPosition, degree * index, streetDict[streetId].distance)
                    )

                    # backward
                    for nextHopStreetId in crossingDict[streetDict[streetId].destination].connectingNodes:
                        if nextHopStreetId == crossing.nodeId:
                            if not self.streets.get(nextHopStreetId):
                                self.streets[nextHopStreetId] = self._newInternalStreet(
                                    streetDict[nextHopStreetId], 
                                    self.streets[streetId].endPosition, 
                                    startPosition
                                )


    def _getTargetCoords(self, source, degree, distance):
        return (source[0] + distance, source[1] + (math.tan(degree) * distance))

    def _newInternalStreet(self, street, start, end):
        internalStreet = _StreetLine(street)
        internalStreet.startPosition = start
        internalStreet.endPosition = end
        return internalStreet

    def update(self):
        self.clock.tick(30)

        self.printNet()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Inhalt von screen anzeigen.
        pygame.display.flip()

        return self.running

    def printNet(self):
        self.screen.fill((0, 0, 0))

        for street in self.streets.values():
            self._printStreet(street)

        for car in self.model.cars:
            street = self.streets[car.streetId]
            startFactor = car.distance / street.street.distance
            endFactor = (car.distance + 1) / street.street.distance

            self._printOnStreet(street, startFactor, endFactor, (0,0,255))

        for crossing in self.model.crossings:
            for streetId in crossing.connectingNodes:
                street = self.streets[streetId]
                color = (255, 0, 0)
                if crossing.green:
                    color = (0, 255, 0)

                self._printOnStreet(street, 0, float(1) / street.street.distance, color)

    def _printStreet(self, street):
        start = (
            street.startPosition[0] * self.printFactor + self.printOffset[0],
            street.startPosition[1] * self.printFactor + self.printOffset[1]
        )
        end = (
            street.endPosition[0] * self.printFactor + self.printOffset[0],
            street.endPosition[1] * self.printFactor + self.printOffset[1]
        )
        pygame.draw.line(self.screen, (255,255,255), start, end, 1)

    def _printOnStreet(self, street, startFactor, endFactor, color):

            start = (
                street.startPosition[0] + (street.endPosition[0] - street.startPosition[0]) * startFactor * self.printFactor + self.printOffset[0],
                street.startPosition[1] + (street.endPosition[1] - street.startPosition[1]) * startFactor * self.printFactor + self.printOffset[1]
            )
            end = (
                street.startPosition[0] + (street.endPosition[0] - street.startPosition[0]) * endFactor * self.printFactor + self.printOffset[0],
                street.startPosition[1] + (street.endPosition[1] - street.startPosition[1]) * endFactor * self.printFactor + self.printOffset[1]
            )

            pygame.draw.line(self.screen, color, start, end, 3)

    def _getPrintOffset(self):
        minUsed = (
            min(self.streets.values(), key=lambda s: min(s.startPosition[0], s.endPosition[0])),
            min(self.streets.values(), key=lambda s: min(s.startPosition[1], s.endPosition[1]))
        )
        minUsed = (
            min(minUsed[0].startPosition[0], minUsed[0].endPosition[0]),
            min(minUsed[1].startPosition[1], minUsed[1].endPosition[1])
        )

        maxUsed = (
            max(self.streets.values(), key=lambda s: max(s.startPosition[0], s.endPosition[0])),
            max(self.streets.values(), key=lambda s: max(s.startPosition[1], s.endPosition[1]))
        )
        maxUsed = (
            max(maxUsed[0].startPosition[0], maxUsed[0].endPosition[0]),
            max(maxUsed[1].startPosition[1], maxUsed[1].endPosition[1])
        )

        factor = min(
            self.screen.get_rect()[2] / (maxUsed[0] - minUsed[0]),
            self.screen.get_rect()[3] / (maxUsed[1] - minUsed[1])
        )

        return (minUsed[0] * factor * -1, minUsed[1] * factor * -1 ), factor

class _StreetLine(object):

    def __init__(self, street=Street):
        self.street = street
        self.startPosition = (.0, .0)
        self.endPosition = (.0, .0)
