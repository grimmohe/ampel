import unittest
from sim.model import Model, Street
from sim.generator import Generator

class TestGenerator(unittest.TestCase):

    def setUp(self):
        model = Model()
        model.streets.append(Street(1, 1, 2, 0))
        model.streets.append(Street(2, 1, 3, 0))
        model.streets.append(Street(3, 2, 4, 0))
        model.streets.append(Street(4, 3, 6, 0))
        model.streets.append(Street(5, 1, 2, 0))
        model.streets.append(Street(6, 4, 5, 0))
        model.streets.append(Street(7, 4, 6, 0))
        model.streets.append(Street(8, 5, 6, 0))
        model.streets.append(Street(9, 6, 7, 0))
        self.model = model

        #
        #      1
        #     / \
        #    2   3
        #     \  |
        #      4 |
        #     / \|
        #    5---6
        #       /
        #      7
        #

    def test_getDistance1(self):
        d = Generator()._getDistance(self.model, 1, 7, 0)
        self.assertEqual(4, d)

    def test_getDistance2(self):
        d = Generator()._getDistance(self.model, 1, 5, 0)
        self.assertEqual(4, d)

    def test_getDistance4(self):
        d = Generator()._getDistance(self.model, 4, 7, 0)
        self.assertEqual(3, d)

    def test_getDistance5(self):
        d = Generator()._getDistance(self.model, 1, 7, 0)
        self.assertEqual(4, d)

    def test_getDistance6(self):
        d = Generator()._getDistance(self.model, 4, 5, 0)
        self.assertEqual(2, d)

    def test_getDistance7(self):
        d = Generator()._getDistance(self.model, 5, 6, 0)
        self.assertEqual(2, d)

    def test_getDistance8(self):
        d = Generator()._getDistance(self.model, 1, 7, 3)
        self.assertEqual(5, d)

if __name__ == '__main__':
    unittest.main()
