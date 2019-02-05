import pygame
import math
import sys
import json
from sim.model import Model, Street, Car, Crossing
import json
import random
from matplotlib import colors as mcolors

class Visual(object):

    def __init__(self):
        self.model = Model()
        self.width = 800
        self.height = 600
        self.white = (255, 255, 255)
        self.colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

    def __str__(self):
        #return self.__dict__
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def init(self, model):
        print(mcolors.BASE_COLORS)
        self.model = model

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption("Ampel AI Krams")
        pygame.mouse.set_visible(1)
        pygame.key.set_repeat(1, 30)
        self.clock = pygame.time.Clock()
        self.running = True
        self.printFactor = 4
        self._prepareStreets()

        self.printOffset = self._getPrintOffset()

    def _prepareStreets(self):

        self.streets = []
        self.crossings = []

        crossingWheelDegree = 360 / len(self.model.crossings)

        print("crossings: " + str(len(self.model.crossings)))
        print("crossingWheelDegree: " + str(crossingWheelDegree))

        for crossingIndex, crossing in enumerate(self.model.crossings, start = 1):
            
            self.crossings.append(
                self._newInternalCrossing(
                        crossing,
                        self._getPositionOnCircle(self.width / self.printFactor, 
                        crossingIndex * crossingWheelDegree
                    )
                )
            )

            """ 
            degree = 360 / len(crossings)

            for index, crossing in enumerate(crossings):

                print(json.dumps(crossing, default=lambda o: o.__dict__, sort_keys=True, indent=4))

                for crossingId in crossing.connectingNodes:

                    startPosition = (int(nodeId) * 50, int(nodeId) * 50)
                    streetId = self._getStreetId(crossing.nodeId, crossingId)

                    try:
                        viceVersaStreetId = self._getStreetId(crossingId, crossing.nodeId)

                        if self.streets.get(viceVersaStreetId):
                            startPosition = self.streets.get(viceVersaStreetId).endPosition
                    except:
                        pass

                    if not self.streets.get(streetId):

                        # forward
                        self.streets[streetId] = self._newInternalStreet(
                            self.streetDict[streetId],
                            startPosition,
                            self._getTargetCoords(startPosition, degree * index, self.streetDict[streetId].distance),
                            list(self.colors.keys())[streetId]
                        )

                        # backward
                        #for nextHopStreetId in crossingDict[streetDict[streetId].destinationId].connectingNodes:
                        #    if nextHopStreetId == crossing.nodeId:
                        #        if not self.streets.get(nextHopStreetId):
                        #            self.streets[nextHopStreetId] = self._newInternalStreet(
                        #                streetDict[nextHopStreetId],
                        #                self.streets[streetId].endPosition,
                        #                startPosition,
                        #                list(self.colors.keys())[streetId]
                        #            )
            """

    def _getPositionOnCircle(self, radius, angle):
        return (
            radius * math.cos(angle), 
            radius * math.sin(angle)
        )

    def _newInternalStreet(self, street, start, end, color):
        o = _StreetLine(street)
        o.startPosition = start
        o.endPosition = end
        o.color = color
        return o

    def _newInternalCrossing(self, crossing, position):
        o = _CrossingBox(crossing)
        o.position = position
        print("created crossing on position: " + str(position))
        return o

    def update(self):
        self.clock.tick(30)

        self.printNet()

        self.handleEvents()

    def handleEvents(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE \
                or event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Inhalt von screen anzeigen.
        pygame.display.flip()

        return self.running

    def printNet(self):
        self.screen.fill((0, 0, 0))

        for crossing in self.crossings:
            self._printCrossing(crossing)

        """
        for street in self.streets.values():
            self._printStreet(street)

        for car in self.model.cars:
            street = self.streets[self._getStreetId(car.sourceId, car.destinationId)]
            startFactor = car.distance / street.street.distance
            endFactor = (car.distance + 1) / street.street.distance

            self._printOnStreet(street, startFactor, endFactor, (0,0,255))

        for crossing in self.model.crossings:
            for sourceId in crossing.connectingNodes:
                street = self.streets[sourceId]
                color = (255, 0, 0)
                if crossing.green:
                    color = (0, 255, 0)

                self._printOnStreet(street, 0, float(1) / street.street.distance, color)
        """

    def _printCrossing(self, crossing):

        pygame.draw.rect(
            self.screen, 
            self.white, 
            pygame.Rect(
                crossing.position[0] + self.printOffset[0], 
                crossing.position[1] + self.printOffset[1], 
                5, 
                5), 
            2)

    def _printStreet(self, street):
        start = (
            street.startPosition[0] * self.printFactor + self.printOffset[0],
            street.startPosition[1] * self.printFactor + self.printOffset[1]
        )
        end = (
            street.endPosition[0] * self.printFactor + self.printOffset[0],
            street.endPosition[1] * self.printFactor + self.printOffset[1]
        )
        color = mcolors.to_rgba(self.colors[street.color])[:3]
        pygame.draw.line(self.screen, (color[0]*255, color[1]*255, color[2]*255), start, end, 1)

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
            min(self.crossings, key=lambda s: s.position[0]),
            min(self.crossings, key=lambda s: s.position[1])
        )

        minUsed = (
            minUsed[0].position[0],
            minUsed[1].position[1]
        )

        maxUsed = (
            max(self.crossings, key=lambda s: s.position[0]),
            max(self.crossings, key=lambda s: s.position[1])
        )
        maxUsed = (
            maxUsed[0].position[0],
            maxUsed[1].position[1]
        )

        factor = min(
            self.screen.get_rect()[2] / (maxUsed[0] - minUsed[0]),
            self.screen.get_rect()[3] / (maxUsed[1] - minUsed[1])
        )

        return (minUsed[0] * factor * -1, minUsed[1] * factor * -1 )

class _StreetLine(object):

    def __init__(self, street=Street):
        self.street = street
        self.startPosition = (.0, .0)
        self.endPosition = (.0, .0)

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class _CrossingBox(object):

    def __init__(self, crossing=Crossing):
        self.crossing = crossing
        self.position = (.0, .0)

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


