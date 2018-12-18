import pygame
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

        self.streets = []

        for crossing in self.model.crossings:

            degree = 360 / len(crossing.connectingNodes)
            for street in crossing.connectingNodes:
                
                intStreet = _StreetLine(street)
                self.streets[street.streetId] = intStreet


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
        self.position = (.0, .0)
        self.vector = (.0, .0)

class _CarBlock(object):

    def __init__(self, car=Car):
        self.car = car