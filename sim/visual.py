import pygame
import math
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

    def _prepareStreets(self):

        self.streets = {}

        self.streetDict = {x.id: x for x in self.model.streets}

        for crossing in self.model.crossings:

            position = (0,0)

            degree = 360 / len(crossing.connectingNodes)

            # do we already have one of the connected nodes?
            for streetId in crossing.connectingNodes:
                if self.streets.get(streetId):
                    position = self.streets[streetId].endPosition
                    break

            for index, streetId in enumerate(crossing.connectingNodes, start=1):

                if not self.streets.get(streetId):

                    internalStreet = _StreetLine(self.streetDict[streetId])
                    internalStreet.startPosition = position
                    internalStreet.endPosition = self._getTargetCoords(position, degree * (index), self.streetDict[streetId].distance)
                    self.streets[streetId] = internalStreet


    def _getTargetCoords(self, source, degree, distance):
        return (source[0] + distance, source[1] + (math.tan(degree) * distance))

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
            pygame.draw.line(self.screen, (255,255,255), street.startPosition, street.endPosition, 1)

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

    def _printOnStreet(self, street, startFactor, endFactor, color):

            start = (
                street.startPosition[0] + (street.endPosition[0] - street.startPosition[0]) * startFactor,
                street.startPosition[1] + (street.endPosition[1] - street.startPosition[1]) * startFactor
            )
            end = (
                street.startPosition[0] + (street.endPosition[0] - street.startPosition[0]) * endFactor,
                street.startPosition[1] + (street.endPosition[1] - street.startPosition[1]) * endFactor
            )

            pygame.draw.line(self.screen, color, start, end, 3)


class _StreetLine(object):

    def __init__(self, street=Street):
        self.street = street
        self.startPosition = (.0, .0)
        self.endPosition = (.0, .0)
