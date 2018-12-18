import tensorflow as tf
from tensorflow.python.ops import rnn, rnn_cell
from tensor.model import Event, Action

class RNN(object):

    def __init__(self):

        self.n_classes = 2
        self.chunk_size = 4
        self.n_chunks = 1
        self.rnn_size = 128

        self.init_rnn()

    def init_rnn(self):

        self.x = tf.placeholder('float', [None, self.n_chunks, self.chunk_size])

        self.prediction = self.recurrent_neural_network(self.x)

        config = tf.ConfigProto(
            device_count = {'GPU': 0}
        )

        self.sess = tf.Session(config=config)
        self.sess.run(tf.global_variables_initializer())

    def recurrent_neural_network(self, x):
        layer = {'weights':tf.Variable(tf.random_normal([self.rnn_size,self.n_classes])),
                'biases':tf.Variable(tf.random_normal([self.n_classes]))}

        x = tf.transpose(x, [1,0,2])
        x = tf.reshape(x, [-1, self.chunk_size])
        x = tf.split(x, self.n_chunks, 0)

        lstm_cell = rnn_cell.LSTMCell(self.rnn_size,state_is_tuple=True)
        outputs, states=rnn.static_rnn(lstm_cell, x, dtype=tf.float32)

        output = tf.matmul(outputs[-1],layer['weights']) + layer['biases']

        return output


    def train_neural_network(self, event=Event()):
        _, c = self.sess.run(self.prediction, feed_dict={self.x: [
            [
                [event.distance, event.carId, event.streetId, event.destinationId]
            ],
            [
                [event.distance, event.carId, event.streetId, event.destinationId]
            ]
        ]})
        return Action(_[0], _[1])
