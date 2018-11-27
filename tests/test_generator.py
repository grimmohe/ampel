import unittest
from sim.model import Model, Street
from sim.generator import Generator

class TestGenerator(unittest.TestCase):

    def test_getDistance(self):
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

        d = Generator()._getDistance(model, 1, 7, 0)
        self.assertEqual(4, d)

if __name__ == '__main__':
    unittest.main()
