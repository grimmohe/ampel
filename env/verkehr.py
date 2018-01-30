"""
Hier haste deinen Docstring
"""

from enum import Enum

class Verkehr:

    cars = []
    streets = []
    nodes = []
    iterator = 0

    def __init__(self):
        pass

    def setup(self):
        self._init_streets()
        self._init_nodes()
        self._init_cars()

    def step(self, lights=[0, 0, 0, 0, 0, 0, 0]):
        # cars next_in_interval runter zählen
        # wenn next_in_interval = 0 dann ausgänge setzen und fahrzeug auf die kreuzung setzen oder warten
        
        pass


    def _init_cars(self):
        self.cars = []
        self.cars.append(Car(13.8, 6.0))

        for car in self.cars:
            self.iterator += 1
            car.next_node = self.nodes[self.iterator % self.nodes.count]
            car.street = car.next_node.connections[0].streets[0]
            car.next_in_interval = self.iterator


    def _init_streets(self):
        self.streets = []
        self.streets.append(Street(100))
        self.streets.append(Street(150))
        self.streets.append(Street(50))
        self.streets.append(Street(50))
        self.streets.append(Street(50))
        self.streets.append(Street(50))
        self.streets.append(Street(100))
        self.streets.append(Street(50))
        self.streets.append(Street(50))
        self.streets.append(Street(50))
        self.streets.append(Street(100))

    def _init_nodes(self):
        self.nodes = []
        self.nodes.append(Node(10, Connection(self.streets[0], self.streets[6]), Connection(self.streets[3])))
        self.nodes.append(Node(10, Connection(self.streets[3], self.streets[4]), Connection(self.streets[2], self.streets[7])))
        self.nodes.append(Node(10, Connection(self.streets[4], self.streets[5]), Connection(self.streets[9])))
        self.nodes.append(Node(10, Connection(self.streets[1], self.streets[10]), Connection(self.streets[5])))
        self.nodes.append(Node(10, Connection(self.streets[8], self.streets[10]), Connection(self.streets[9])))
        self.nodes.append(Node(10, Connection(self.streets[0], self.streets[1]), Connection(self.streets[2])))
        self.nodes.append(Node(10, Connection(self.streets[6], self.streets[8]), Connection(self.streets[7])))


class Car:

    speed = .0
    length = .0
    next_node = None
    street = None
    next_in_interval = 0
    next_indicator_type = None

    def __init__(self, speed, length):
        self.speed = speed
        self.length = length

class Street:

    length = .0

    def __init__(self, length):
        self.length = length


class IndicatorType(Enum):

    INCOMING = 1
    OUTGOING = 2


class Connection:

    streets = []

    def __init__(self, street1, street2=None):
        self.streets.append(street1)

        if street2:
            self.streets.append(street2)


class Node:

    size = .0
    green_for = 0
    connections = []

    def __init__(self, size, connection1, connection2):
        self.size = size
        self.connections.append(connection1)
        self.connections.append(connection2)
