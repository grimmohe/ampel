"""
Hier haste deinen Docstring
"""

from enum import Enum
import math
from elements.elements import *

class Verkehr:

    def __init__(self):
        self.cars = []
        self.streets = []
        self.nodes = []
        self.iterator = 0

    def move(self, car):
        distance_left = car.distance_left - car.speed
        status = CarStatus.FREE
        gap = 10
        self.iterator += 1

        if car.next_indicator_type == IndicatorType.OUTGOING:
            next = self.iterator % 4
            streets = car.next_node.connections[next % 2].streets
            next_street = streets[min(int(next > 1), len(streets)-1)]
            next_node = None
            
            for node in self.nodes:
                if node != car.next_node:
                    for con in node.connections:    
                        if con.streets.count(next_street) > 0:
                            next_node = node
            
            if next_node == None:
                raise "Kein naechster Knoten zur Strasse"

            car.next_indicator_type = IndicatorType.INCOMING
            car.next_node = next_node
            car.street = next_street
            distance_left = next_street.length
            
        else:
            for front in self.cars:
                if front.street == car.street \
                and front.distance_left < car.distance_left \
                and distance_left < front.distance_left + gap:
                    distance_left = front.distance_left + gap
                    status = CarStatus(max(int(front.status), (CarStatus.FRONTCAR)))
            
            if distance_left <= 0: #ab auf die kreuzung
                if car.next_node.connections[car.next_node.green_for].streets.count(car.street) > 0:
                    car.next_indicator_type = IndicatorType.OUTGOING
                else:
                    status = CarStatus.WAITING
                    distance_left = 0

        car.distance_left = distance_left
        car.status = status

        return int(status == CarStatus.WAITING)

    def setup(self):
        self._init_streets()
        self._init_nodes()
        self._init_cars()

    def step(self, lights=[0, 0, 0, 0, 0, 0, 0]):
        self.cars.sort(key=lambda x: x.distance_left)

        if len(lights) != len(self.nodes):
            raise "wrong number of lights"

        for ii in range(7):
            self.nodes[ii].green_for = lights[ii]

        cost = 0
        for car in self.cars:
            cost += self.move(car)

        self.cars.sort(key=lambda x: x.id)
        for car in self.cars:
            print("Car", car)
        print("Step -----------------")

        return cost

    def _init_cars(self):
        self.cars = []
        self.cars.append(Car(0, 13.8))
        self.cars.append(Car(1, 14.0))
        self.cars.append(Car(2, 14.4))

        for car in self.cars:
            self.iterator += 1
            car.next_node = self.nodes[self.iterator % len(self.nodes)]
            car.street = car.next_node.connections[0].streets[0]
            car.distance_left = self.iterator * car.speed

    def _init_streets(self):
        self.streets = []
        self.streets.append(Street(101))
        self.streets.append(Street(150))
        self.streets.append(Street(50))
        self.streets.append(Street(50))
        self.streets.append(Street(50))
        self.streets.append(Street(50))
        self.streets.append(Street(102))
        self.streets.append(Street(50))
        self.streets.append(Street(50))
        self.streets.append(Street(50))
        self.streets.append(Street(103))

    def _init_nodes(self):
        self.nodes = []
        self.nodes.append(Node(10, Connection(self.streets[0], self.streets[6]), Connection(self.streets[3])))
        self.nodes.append(Node(10, Connection(self.streets[3], self.streets[4]), Connection(self.streets[2], self.streets[7])))
        self.nodes.append(Node(10, Connection(self.streets[4], self.streets[5]), Connection(self.streets[9])))
        self.nodes.append(Node(10, Connection(self.streets[1], self.streets[10]), Connection(self.streets[5])))
        self.nodes.append(Node(10, Connection(self.streets[8], self.streets[10]), Connection(self.streets[9])))
        self.nodes.append(Node(10, Connection(self.streets[0], self.streets[1]), Connection(self.streets[2])))
        self.nodes.append(Node(10, Connection(self.streets[6], self.streets[8]), Connection(self.streets[7])))

