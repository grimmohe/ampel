from tensor.rnn import RNN
from tensor.model import Event

event = Event();

rnn = RNN()
print(rnn.train_neural_network(event))
