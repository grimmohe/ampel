from sim.simulator import Simulator
from sim.generator import Generator

model = Generator().buildModel()
s = Simulator(model=model)
s._moveCars()
