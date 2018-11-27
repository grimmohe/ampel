from sim.simulator import Simulator
from sim.generator import Generator
from tensor.rnn import RNN

rnn = RNN()
model = Generator().buildModel()
s = Simulator(model=model)
s._moveCars()
s.step(rnn.train_neural_network)
