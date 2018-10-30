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
import datetime


class Perceptron(object):

    _session = tf.Session()
    __tensor_cache = {}

    _ops = {
        'copy': lambda obj1, obj2, factor: tf.assign(obj1, obj2),
        'cross': lambda obj1, obj2, factor: tf.assign(obj1, tf.divide(tf.add(obj1, obj2), 2)),
        'mutate': lambda obj1, obj2, factor: tf.assign(obj1, tf.add(obj1, tf.random_uniform(shape=obj1.shape, minval=factor*-1, maxval=factor))),
        'mutate_layer': lambda obj1, obj2, factor: tf.assign(obj1, tf.add(obj1, tf.reshape(obj2, factor))),
        'placeholder': lambda obj1, obj2, factor: tf.placeholder('float32', factor),
        'loss': lambda obj1, obj2, factor: tf.abs(obj2 - obj1),
        'learn': lambda obj1, obj2, factor: tf.train.AdamOptimizer(learning_rate=factor, beta1=0.9, beta2=0.999,).minimize(obj1)
    }


    def __init__(self, n_input, n_output):
        self.n_input = n_input  
        self.n_output = n_output
        self.fitness = sys.maxsize
        self.x = tf.placeholder('float', [None, self.n_input])
        self.layers = {}
        self.pred = self._multilayer_perceptron()

        self.ph = Perceptron._get_tensor('placeholder', self.pred, factor=(None, self.n_output))
        self.loss_op = Perceptron._get_tensor('loss', self.pred, self.ph)
        self.train_op = Perceptron._get_tensor('learn', self.loss_op, self.pred, 0.001)

        self.size = self._get_size()
        self.story = []
        self.input = []
        self.output = []


    @staticmethod
    def init():
        Perceptron._session.run(tf.global_variables_initializer())


    @staticmethod
    def log_tensor_object_counts():
        logger.info('tf operations %s', len(tf.get_default_graph().get_operations()))


    @staticmethod
    def _get_tensor(name, obj1, obj2=None, factor=0):
        tensor = Perceptron.__tensor_cache.get((name, obj1, obj2))
        if tensor == None:
            tensor = Perceptron._ops[name](obj1, obj2, factor)
            Perceptron.__tensor_cache[(name, obj1, obj2)] = tensor
        return tensor


    @staticmethod
    def loadTensor(file):
        tf.train.Saver().restore(Perceptron._session, file)


    @staticmethod
    def saveTensor():
        tf.train.Saver().save(Perceptron._session, './saves/%s.dump'%datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S"))

    
    def _get_size(self):
        size = 0
        for layer in self.layers.values():
            size += layer.shape.num_elements()
        return size
        

    def _multilayer_perceptron(self):
        pass


    def set_fitness(self, points):
        self.fitness = points


    # Store layers weight & bias
    def activate(self, inputs):
        if len(self.story) > 100:
            self.story = self.story[-10:]
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('activating for input %s' %(str(inputs),))

        outputs = Perceptron._session.run(self.pred, feed_dict={self.x: inputs})

        self.input.append(inputs[0])
        self.output.append(outputs[0])

        return outputs


    def copy(self, other):
        self.story.append('accept copy')
        for layer in self.layers:
            Perceptron._get_tensor('copy', self.layers[layer], other.layers[layer]).eval(session=Perceptron._session)


    def cross(self, other):
        self.story.append('cross')
        for layer in self.layers:
            self._cross(self.layers[layer], other.layers[layer])


    def _cross(self, own, other):
        Perceptron._get_tensor('cross', own, other).eval(session=Perceptron._session)


    '''
    Ein zufälliger Layer mit einem zufälligen Index wird für eine Mutation ausgewählt
    '''
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


    def learn(self, input, output, iterations):
        Perceptron._session.run(self.train_op, feed_dict={self.x: input * iterations, self.ph: output * iterations})
        
    '''
    Addiert value zum Layer auf den index verweist
    '''
    def mutate_index(self, index, value):
        self.story.append('mutate index')
        layer = self.layers[index['layer']]
        length = index['length']
        a = [.0] * length
        a[index['pos']] = value

        p = Perceptron._get_tensor('placeholder', length, factor=(1, length))
        op = Perceptron._get_tensor('mutate_layer', layer, p, layer.shape)

        return Perceptron._session.run(op, {p:[a]})


    def mutate_heavy(self, factor=0.2):
        self.story.append('mutate heavy')
        for layer in self.layers:
            self._mutate(self.layers[layer], factor)


    def mutate_layer(self, factor=0.2):
        key, layer = random.choice(list(self.layers.items()))
        self.story.append('mutate layer %s' % key)
        self._mutate_layer(key, layer, factor)


    def mutate_all_layers(self, factor=0.2):
        self.story.append('mutate layers')
        for key, layer in self.layers.items():
            self._mutate_layer(key, layer, factor)


    """
    mutate only a random amount of entries
    """
    def _mutate_layer(self, key, layer, factor=0.2):
        length = layer.shape.num_elements()
        a = [.0] * length
        for _ in range(random.randint(1, len(a) - 1)):
            a[random.randint(0, len(a) - 1)] = random.random() * factor * 2 - factor

        p = Perceptron._get_tensor('placeholder', length, factor=(1, length))
        op = Perceptron._get_tensor('mutate_layer', layer, p, layer.shape)

        return Perceptron._session.run(op, {p:[a]})


    def _mutate(self, layer, factor):
        Perceptron._get_tensor('mutate', layer, factor=factor).eval(session=self._session)


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

        layer_1 =  tf.add(tf.matmul(self.x, self.layers['h1']), self.layers['b1'])
        out = tf.add(tf.matmul(layer_1,  self.layers['output']), self.layers['ob'])

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

        layer_1 =  tf.sigmoid(tf.add(tf.matmul(self.x, self.layers['h1']), self.layers['b1']))
        layer_2 =  tf.sigmoid(tf.add(tf.matmul(layer_1, self.layers['h2']), self.layers['b2']))
        out = tf.add(tf.matmul(layer_2,  self.layers['output']), self.layers['ob'])
        
        return out

class Perceptron_5Layer(Perceptron):

    def __init__(self, n_input, n_hidden_1, n_hidden_2, n_hidden_3, n_hidden_4, n_hidden_5, n_output):
        self.n_hidden_1 = n_hidden_1
        self.n_hidden_2 = n_hidden_2
        self.n_hidden_3 = n_hidden_3
        self.n_hidden_4 = n_hidden_4
        self.n_hidden_5 = n_hidden_5
        Perceptron.__init__(self,n_input, n_output)

    # Create model
    def _multilayer_perceptron(self):

        self.layers['h1'] = tf.Variable(tf.random_normal([self.n_input, self.n_hidden_1]))
        self.layers['h2'] = tf.Variable(tf.random_normal([self.n_hidden_1, self.n_hidden_2]))
        self.layers['h3'] = tf.Variable(tf.random_normal([self.n_hidden_2, self.n_hidden_3]))
        self.layers['h4'] = tf.Variable(tf.random_normal([self.n_hidden_3, self.n_hidden_4]))
        self.layers['h5'] = tf.Variable(tf.random_normal([self.n_hidden_4, self.n_hidden_5]))
        self.layers['out'] = tf.Variable(tf.random_normal([self.n_hidden_5, self.n_output]))
 
        self.layers['b1'] = tf.Variable(tf.random_normal([self.n_hidden_1]))
        self.layers['b2'] = tf.Variable(tf.random_normal([self.n_hidden_2]))
        self.layers['b3'] = tf.Variable(tf.random_normal([self.n_hidden_3]))
        self.layers['b4'] = tf.Variable(tf.random_normal([self.n_hidden_4]))
        self.layers['b5'] = tf.Variable(tf.random_normal([self.n_hidden_5]))
        self.layers['ob'] = tf.Variable(tf.random_normal([self.n_output]))

        layer_1 = tf.tanh(tf.add(tf.matmul(self.x, self.layers['h1']), self.layers['b1']))
        layer_2 = tf.tanh(tf.add(tf.matmul(layer_1, self.layers['h2']), self.layers['b2']))
        layer_3 = tf.tanh(tf.add(tf.matmul(layer_2, self.layers['h3']), self.layers['b3']))
        layer_4 = tf.tanh(tf.add(tf.matmul(layer_3, self.layers['h4']), self.layers['b4']))
        layer_5 = tf.tanh(tf.add(tf.matmul(layer_4, self.layers['h5']), self.layers['b5']))
        out = tf.tanh(tf.add(tf.matmul(layer_5,  self.layers['out']), self.layers['ob']))
        
        return out

'''
Recurrent Neural Network
Der Input bleibt als Durchschnitt mit dem letzten Input bestehen.
Damit kann das Netz theoretisch anhand der Fließkommazahl feststellen, 
wie lange die letze 1 her ist.
'''
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
        layer_1 =  tf.nn.relu(tf.add(tf.matmul(mem, self.layers['weights1']), self.layers['bias1']))
        out = tf.add(tf.matmul(layer_1,  self.layers['output']), self.layers['outputbias'])

        return out


'''
Recurrent Neural Network
Der Input bleibt als Durchschnitt mit dem letzten Input bestehen.
Damit kann das Netz theoretisch anhand der Fließkommazahl feststellen, 
wie lange die letze 1 her ist.
'''
class Perceptron_RNN_2Layer(Perceptron):

    def __init__(self, n_input, n_hidden_1, n_hidden_2, n_output):
        self.n_hidden_1 = n_hidden_1
        self.n_hidden_2 = n_hidden_2
        Perceptron.__init__(self, n_input, n_output)


     # Create model
    def _multilayer_perceptron(self):

        self.layers['input_mem'] = tf.Variable(tf.zeros([1, self.n_input]))

        self.layers['weights1'] = tf.Variable(tf.random_normal([self.n_input, self.n_hidden_1]))
        self.layers['bias1'] = tf.Variable(tf.random_normal([self.n_hidden_1]))

        self.layers['mem1'] = tf.Variable(tf.zeros([self.n_input, self.n_hidden_1]))

        self.layers['weights2'] = tf.Variable(tf.random_normal([self.n_hidden_1, self.n_hidden_2]))
        self.layers['bias2'] = tf.Variable(tf.random_normal([self.n_hidden_2]))

        self.layers['output'] = tf.Variable(tf.random_normal([self.n_hidden_2, self.n_output]))
        self.layers['outputbias'] = tf.Variable(tf.random_normal([self.n_output]))


        mem = tf.assign(self.layers['input_mem'], tf.div(tf.add(self.x, self.layers['input_mem']), 2))
        layer_1 =  tf.sigmoid(tf.add(tf.matmul(mem, self.layers['weights1']), self.layers['bias1']))

        mem1 = tf.assign(self.layers['mem1'], tf.div(tf.add( layer_1, self.layers['mem1']), 2))
        layer_2 =  tf.sigmoid(tf.add(tf.matmul(mem1, self.layers['weights2']), self.layers['bias2']))

        out = tf.add(tf.matmul(layer_2,  self.layers['output']), self.layers['outputbias'])

        return out
