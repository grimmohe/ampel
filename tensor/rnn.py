import tensorflow as tf
from tensorflow.python.ops import rnn, rnn_cell
from tensor.model import Event

class RNN(object):

    def __init__(self):

        self.n_classes = 5
        self.chunk_size = 4
        self.n_chunks = 1
        self.rnn_size = 128

        self.init_rnn()

    def init_rnn(self):

        self.x = tf.placeholder('float', [None, self.n_chunks, self.chunk_size])
        #y = tf.placeholder('float')

        self.prediction = self.recurrent_neural_network(self.x)
        #self.cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.prediction,labels=y) )
        #self.optimizer = tf.train.AdamOptimizer().minimize(self.cost)
        
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
        #x = tf.shape(x)
        #x = tf.unstack(x, num=1)
        #x = tf.TensorArray(tf.int32, 1, dynamic_size=True, infer_shape=False)
        #x = TensorArr.unpack(x)

        lstm_cell = rnn_cell.LSTMCell(self.rnn_size,state_is_tuple=True)
        #lstm_cell2 = rnn_cell.LSTMCell(rnn_size,state_is_tuple=True)
        #outputs = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)
        outputs, states=rnn.static_rnn(lstm_cell, x, dtype=tf.float32)

        output = tf.matmul(outputs[-1],layer['weights']) + layer['biases']

        return output


    def train_neural_network(self, event=Event()):
        print(type(self.x))
        _, c = self.sess.run(self.prediction, feed_dict={self.x: [
            [
                [event.distance, event.carId, event.streetId, event.destinantionId]
            ],
            [
                [event.distance, event.carId, event.streetId, event.destinantionId]
            ]
        ]})
        print(_[0])
        #epoch_loss += c

        #correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
        #accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        #print('Accuracy:',accuracy.eval({x:mnist.test.images.reshape((-1, n_chunks, chunk_size)), y:mnist.test.labels}))
