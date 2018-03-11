'''
A Multilayer Perceptron implementation example using TensorFlow library.

'''
import copy
import tensorflow as tf
import numpy
import logging
import sys
logger = logging.getLogger('percp')
import time
import random


class Perceptron(object):

    _session = tf.Session()
    __tensor_cache = {}

    _ops = {
        'copy': lambda obj1, obj2, factor: tf.assign(obj1, obj2),
        'cross': lambda obj1, obj2, factor: tf.assign(obj1, tf.divide(tf.add(obj1, obj2), 2)),
        'mutate': lambda obj1, obj2, factor: tf.assign(obj1, tf.add(obj1, tf.random_uniform(shape=tf.shape(obj1), minval=factor*-1, maxval=factor))),
        'mutate_index': lambda obj1, obj2, factor: tf.assign(obj1, tf.add(obj1, tf.reshape(obj2, factor))),
        'placeholder': lambda obj1, obj2, factor: tf.placeholder('float32', factor)
    }


    def __init__(self, n_input, n_output):
        self.n_input = n_input
        self.n_output = n_output
        self.fitness = sys.maxsize
        self.x = tf.placeholder('float', [None, self.n_input])
        self.layers = {}
        self.pred = self._multilayer_perceptron()
        self.size = self._get_size()


    @staticmethod
    def init():
        Perceptron._session.run(tf.global_variables_initializer())


    @staticmethod
    def log_tensor_object_counts():
        logger.info("tf operations %s", len(tf.get_default_graph().get_operations()))


    @staticmethod
    def _get_tensor(name, obj1, obj2=None, factor=0):
        tensor = Perceptron.__tensor_cache.get((name, obj1, obj2))
        if tensor == None:
            tensor = Perceptron._ops[name](obj1, obj2, factor)
            Perceptron.__tensor_cache[(name, obj1, obj2)] = tensor
        return tensor

    
    def _get_size(self):
        size = 0
        for key, layer in self.layers.items():
            size += layer.shape.num_elements()
        return size

    def _multilayer_perceptron(self):
        pass


    def set_fitness(self, points):
        self.fitness = points


    # Store layers weight & bias
    def activate(self, inputs):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('activating for input %s' %(str(inputs),))
        outputs = Perceptron._session.run(self.pred, feed_dict={self.x: inputs})
        return outputs


    def copy(self, other):
        for layer in self.layers:
            Perceptron._get_tensor("copy", self.layers[layer], other.layers[layer]).eval(session=Perceptron._session)


    def cross(self, other):
        for layer in self.layers:
            self._cross(self.layers[layer], other.layers[layer])


    def _cross(self, own, other):
        Perceptron._get_tensor("cross", own, other).eval(session=Perceptron._session)


    """
    Ein zufälliger Layer mit einem zufälligen Index wird für eine Mutation ausgewählt
    """
    def get_mutation_index(self, generation=None):
        key = None
        x = None
        length = None
        
        if generation == None:
            key, layer = random.choice(list(self.layers.items()))
            length = layer.shape.num_elements()
            x = random.randint(0, length-1)
        else:
            generation = generation % self.size
            keys = list(self.layers.keys())
            keys.sort()
            for key in keys:
                layer = self.layers[key]
                length = layer.shape.num_elements()
                if length <= generation:
                    generation -= length
                else:
                    x = generation
                    break

        return {'layer':key, 'pos':x, 'length': length}


    """
    Addiert value zum Layer auf den index verweist
    """
    def mutate_index(self, index, value):
        layer = self.layers[index['layer']]
        length = index['length']
        a = [.0] * length
        a[index['pos']] = value

        p = Perceptron._get_tensor('placeholder', length, factor=(1, length))
        op = Perceptron._get_tensor('mutate_index', layer, p, layer.shape)

        return Perceptron._session.run(op, {p:[a]})


    def mutate(self, factor=0.2):
        for layer in self.layers:
            self._mutate(self.layers[layer], factor)


    def _mutate(self, layer, factor):
        Perceptron._get_tensor("mutate", layer, factor=factor).eval(session=self._session)


    def __unicode__(self):
        return str(self.fitness)


class Perceptron_1Layer(Perceptron):

    def __init__(self, n_input, n_hidden_1, n_output):
        self.n_hidden_1 = n_hidden_1
        Perceptron.__init__(self,n_input, n_output)

     # Create model
    def _multilayer_perceptron(self):

        self.layers['h1'] = tf.Variable(tf.random_normal([self.n_input, self.n_hidden_1]))
        self.layers['output'] = tf.Variable(tf.random_normal([self.n_hidden_1, self.n_output]))
        self.layers['b1'] = tf.Variable(tf.random_normal([self.n_hidden_1]))
        self.layers['ob'] = tf.Variable(tf.random_normal([self.n_output]))

        layer_1 =  tf.sigmoid(tf.add(tf.matmul(self.x, self.layers['h1']), self.layers['b1']))
        out = tf.sigmoid(tf.add(tf.matmul(layer_1,  self.layers['output']), self.layers['ob']))

        return out

class Perceptron_2Layer(Perceptron):

    def __init__(self, n_input, n_hidden_1, n_hidden_2, n_output):
        self.n_hidden_1 = n_hidden_1
        self.n_hidden_2 = n_hidden_2
        Perceptron.__init__(self,n_input, n_output)

    # Create model
    def _multilayer_perceptron(self):

        self.layers['h1'] = tf.Variable(tf.random_normal([self.n_input, self.n_hidden_1]))
        self.layers['h2'] = tf.Variable(tf.random_normal([self.n_hidden_1, self.n_hidden_2]))
        self.layers['output'] = tf.Variable(tf.random_normal([self.n_hidden_2, self.n_output]))
        
        self.layers['b1'] = tf.Variable(tf.random_normal([self.n_hidden_1]))
        self.layers['b2'] = tf.Variable(tf.random_normal([self.n_hidden_2]))
        self.layers['ob'] = tf.Variable(tf.random_normal([self.n_output]))

        layer_1 =  tf.tanh(tf.add(tf.matmul(self.x, self.layers['h1']), self.layers['b1']))
        layer_2 =  tf.tanh(tf.add(tf.matmul(layer_1, self.layers['h2']), self.layers['b2']))
        out = tf.add(tf.matmul(layer_2,  self.layers['output']), self.layers['ob'])

        return out


"""
Recurrent Neural Network
Der Input bleibt als Durchschnitt mit dem letzten Input bestehen.
Damit kann das Netz theoretisch anhand der Fließkommazahl feststellen, 
wie lange die letze 1 her ist.
"""
class Perceptron_RNN(Perceptron):

    def __init__(self, n_input, n_hidden_1, n_output):
        self.n_hidden_1 = n_hidden_1
        Perceptron.__init__(self, n_input, n_output)


     # Create model
    def _multilayer_perceptron(self):

        self.layers['input_mem'] = tf.Variable(tf.zeros([1, self.n_input]))
        self.layers['weights1'] = tf.Variable(tf.random_normal([self.n_input, self.n_hidden_1]))
        self.layers['output'] = tf.Variable(tf.random_normal([self.n_hidden_1, self.n_output]))
        self.layers['bias1'] = tf.Variable(tf.random_normal([self.n_hidden_1]))
        self.layers['outputbias'] = tf.Variable(tf.random_normal([self.n_output]))

        mem = tf.assign(self.layers['input_mem'], tf.div(tf.add(self.x, self.layers['input_mem']), 2))
        layer_1 =  tf.tanh(tf.add(tf.matmul(mem, self.layers['weights1']), self.layers['bias1']))
        out = tf.add(tf.matmul(layer_1,  self.layers['output']), self.layers['outputbias'])

        return out
