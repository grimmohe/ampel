"""
ELEMENTS YEA
"""

from enum import IntEnum

class CarStatus(IntEnum):

    FREE = 0
    FRONTCAR = 1
    WAITING = 2


class Car:

    def __init__(self, id, speed):
        self.id = id
        self.speed = speed
        self.next_node = None
        self.street = None
        self.status = CarStatus.FREE
        self.distance_left = 0
        self.next_indicator_type = None

    def __str__(self, level=0):
        return "<id: " + str(self.id) + " distance_left: " + str(self.distance_left) + " speed: " + str(self.speed) + " status: " + str(self.status) + ">"

    def __repr__(self):
        return str(self)


class Street:

    def __init__(self, id, length):
        self.id = id
        self.length = length


class IndicatorType(IntEnum):

    INCOMING = 1
    OUTGOING = 2


class Connection:

    def __init__(self, street1, street2=None):
        self.streets = []
        self.streets.append(street1)

        if street2:
            self.streets.append(street2)


class Node:

    def __init__(self, size, connection1, connection2):
        self.green_for = 0
        self.connections = []
        self.size = size
        self.connections.append(connection1)
        self.connections.append(connection2)
