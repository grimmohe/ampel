"""
Hier haste deinen Docstring
"""

from enum import Enum
import math
import logging
from .structs import *

class Verkehr:

    def __init__(self, accumulate):
        self.cars = []
        self.streets = []
        self.nodes = []
        self.iterator = 0
        self.steps = 0
        self.cost = 0
        self.sensor_out = []
        self.accumulate = accumulate
        self.logger = logging.getLogger(__name__)

    def move(self, car):
        distance_left = car.distance_left - car.speed
        status = CarStatus.FREE
        gap = 10
        stopped = False
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

            self._set_sensor(next_street.id, IndicatorType.OUTGOING, next_node.id > car.next_node.id)

            car.next_indicator_type = IndicatorType.INCOMING
            car.last_node = car.next_node
            car.next_node = next_node
            car.street = next_street
            distance_left = next_street.length

            self.logger.info('car %s goes to street %s', car.id, car.street.id)
            
        else:
            for front in self.cars:
                if front.street == car.street \
                and front.distance_left < car.distance_left \
                and distance_left < front.distance_left + gap:
                    distance_left = front.distance_left + gap
                    status = CarStatus(max(int(front.status), (CarStatus.FRONTCAR)))
            
            if distance_left <= 0: #ab auf die kreuzung
                self._set_sensor(car.street.id, IndicatorType.INCOMING, car.next_node.id > car.last_node.id)

                if car.next_node.connections[car.next_node.green_for].streets.count(car.street) > 0:
                    car.next_indicator_type = IndicatorType.OUTGOING
                else:
                    status = CarStatus.WAITING
                    distance_left = 0
                    stopped = (car.status != CarStatus.WAITING)

        car.distance_left = distance_left
        car.status = status

        if distance_left > car.street.length:
            self.logger.warning('car %s has %s left on street %s with a length of %s!', car.id, distance_left, car.street.id, car.street.length)

        return int(status == CarStatus.WAITING) + int(stopped)

    def setup(self):
        self._init_streets()
        self._init_nodes()
        self._init_cars()
        self._init_accu()

    def step(self, lights=[0, 0, 0, 0, 0, 0, 0]):
        self.steps += 1
        self.sensor_out = [0] * len(self.streets) * 4
        self.cars.sort(key=lambda x: x.distance_left)

        if len(lights) != len(self.nodes):
            raise "wrong number of lights"

        for ii in range(7):
            self.nodes[ii].green_for = lights[ii]

        for car in self.cars:
            self.cost += self.move(car)

        if self.logger.isEnabledFor(logging.DEBUG):
            for car in self.cars:
                self.logger.debug(car)
        self.logger.info('step %s, cost %s', self.steps, self.cost)
        self.logger.debug(self.sensor_out)

        self.sensor_out_accu = self.sensor_out_accu[:self.accumulate-1]
        self.sensor_out_accu.insert(0,self.sensor_out)

        return [item for sublist in self.sensor_out_accu for item in sublist]

    def get_cost(self):
        return self.cost

    def _init_cars(self):
        self.cars = []
        for i in range(20):
            self.cars.append(Car(i, 10 + (i % 50) / 10))

        for car in self.cars:
            self.iterator += 1
            car.next_node = self.nodes[self.iterator % len(self.nodes)]
            car.street = car.next_node.connections[0].streets[0]
            car.distance_left = car.street.length / self.iterator

            for node in self.nodes:
                if node == car.next_node: continue
                if node.connections[0].streets.count(car.street) > 0 \
                or node.connections[1].streets.count(car.street) > 0:
                    car.last_node = node
                    break

    def _init_streets(self):
        self.streets = []
        self.streets.append(Street(1, 100))
        self.streets.append(Street(2, 150))
        self.streets.append(Street(3, 50))
        self.streets.append(Street(4, 50))
        self.streets.append(Street(5, 50))
        self.streets.append(Street(6, 50))
        self.streets.append(Street(7, 100))
        self.streets.append(Street(8, 50))
        self.streets.append(Street(9, 50))
        self.streets.append(Street(10, 50))
        self.streets.append(Street(11, 100))

    def _init_nodes(self):
        self.nodes = []
        self.nodes.append(Node(0, 10, Connection(self.streets[0], self.streets[6]), Connection(self.streets[3])))
        self.nodes.append(Node(1, 10, Connection(self.streets[3], self.streets[4]), Connection(self.streets[2], self.streets[7])))
        self.nodes.append(Node(2, 10, Connection(self.streets[4], self.streets[5]), Connection(self.streets[9])))
        self.nodes.append(Node(3, 10, Connection(self.streets[1], self.streets[10]), Connection(self.streets[5])))
        self.nodes.append(Node(4, 10, Connection(self.streets[8], self.streets[10]), Connection(self.streets[9])))
        self.nodes.append(Node(5, 10, Connection(self.streets[0], self.streets[1]), Connection(self.streets[2])))
        self.nodes.append(Node(6, 10, Connection(self.streets[6], self.streets[8]), Connection(self.streets[7])))

    def _init_accu(self):
        self.sensor_out_accu = [[0] * len(self.streets) * 4] * self.accumulate

    """
     1, 0, 0, 1, 0, 0, 1, 1 
    [          ][          ] street
    [    ][    ] to the crossing, from the crossing
    [ ][ ] small node id, big node id
    """
    def _set_sensor(self, street_id=0, indicator=IndicatorType.OUTGOING, up_the_street=False):
        offset = (street_id - 1) * 4
        offset += int(indicator == IndicatorType.OUTGOING) * 2
        offset += int(up_the_street)

        self.logger.debug('set_sensor %s (street %s, indicator %s, up %s)', offset, street_id, indicator, up_the_street)
        self.sensor_out[offset] = 1
