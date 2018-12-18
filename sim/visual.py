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
                            if not self.streets.get(streetId):
                                self.streets[streetId] = self._newInternalStreet(
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
 
        self.screen.fill((0, 0, 0))
        self.printNet()
 
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.running = False
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
 
        # Inhalt von screen anzeigen.
        pygame.display.flip()        

    def printNet(self):
        for street in self.streets:
            pygame.draw.line(self.screen, (255,255,255), [1,1], [200,200], 1)


class _StreetLine(object):

    def __init__(self, street=Street):
        self.street = street
        self.startPosition = (.0, .0)
        self.endPosition = (.0, .0)

class _CarBlock(object):

    def __init__(self, car=Car):
        self.car = car