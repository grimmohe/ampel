import pygame
from sim.model import Model, Street, Car

class Visual(object):

    def __init__(self):
        self.model = Model()

    def init(self, model):
        self.model = model

    def update(self):
        pass

class _StreetLine(object):

    def __init__(self, street=Street):
        self.street = street
        self.position = (.0, .0)
        self.vector = (.0, .0)

class _CarBlock(object):

    def __init__(self, car=Car):
        self.car = car