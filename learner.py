import collections
from collections import OrderedDict
import copy
import logging
import numpy as np
import random
import tensorflow as tf
from tfperceptron import Perceptron
import time
from env import verkehr


logger = logging.getLogger('dino.learner')
class Learner(object):

    def __init__(self, genomeUnits, selection, mutations, mutationProb):
        self.genomes = []
        self.genome = 0
        self.generation = 0
        self.shouldCheckExperience = False
        self.genomeUnits = genomeUnits
        self.selection = selection
        self.mutations = mutations
        self.mutationProb = mutationProb
        self.interuptted = False
        

    """
    Build genomes before calling executeGeneration.
    """
    def startLearning(self):

        # Build genomes if needed
        while (len(self.genomes) < self.genomeUnits):
            self.genomes.append(self._buildGenome(440, 7))
  
        logger.info('Build genomes done')
        self._executeGeneration()

    """
    Given the entire generation of genomes (An array),
    applyes method `executeGenome` for each element.
    After all elements have completed executing:
     
    1) Select best genomes
    2) Does cross over (except for 2 genomes)
    3) Does Mutation-only on remaining genomes
    4) Execute generation (recursivelly)
    """
    def _executeGeneration(self):
        self.generation += 1
        logger.info('Executing generation %d'%(self.generation,))

        self.genome = 0

        while(self.genome < len(self.genomes) and not self.interuptted):
            self._executeGenome()

        self._genify()

    def _genify(self):

        # Kill worst genomes
        self.genomes = self._selectBestGenomes()

        # Copy best genomes
        bestGenomes = self.genomes

        # Cross Over ()
        while len(self.genomes) < self.genomeUnits - self.mutations:
            # Get two random Genomes
            genA = random.choice(bestGenomes).copy()
            genB = random.choice(bestGenomes).copy()
            #Cross over and Mutate
            newGenome = self._mutate(self._crossOver(genA, genB))
            genA = None
            genB = None
            #Add to generation
            self.genomes.append(newGenome)
    

        # Mutation-only
        while len(self.genomes) < self.genomeUnits:
            # Get two random Genomes
            gen = random.choice(bestGenomes).copy()
            #logger.info('mutation old genome %s'%(str(gen.as_dict),))
            # Cross over and Mutate
            newGenome = self._mutate(gen)
            #logger.info('mutation new genome %s'%(str(newGenome.as_dict),))
            # Add to generation
            self.genomes.append(newGenome)
            #logger.info('mutation old genome after mutation %s'%(str(gen.as_dict),))
    

        logger.info('Completed generation %d' %(self.generation,))

        #Execute next generation
        self._executeGeneration()


    """
    Sort all the genomes, and delete the worst one
    untill the genome list has selectN elements.
    """
    def _selectBestGenomes(self):
        self.genomes.sort(key=lambda x: x.fitness)

        selected = self.genomes[:self.selection]
        tf.reset_default_graph()

        s = []
        f = []
        for select in selected:
            fit = select.copy()
            fit.reload()
            s.append(fit)
            f.append(select.fitness)

        selected = None
        logger.info('Fitness: #### %s', f)
        return s

    """
    Waits the game to end, and start a new one, then:
    1) Set's listener for sensorData
    2) On data read, applyes the neural network, and
       set it's output
    3) When the game has ended and compute the fitness
    """
    def _executeGenome(self):
        genome = self.genomes[self.genome]
        self.genome += 1
        logger.info('Executing genome %d' %(self.genome,))
    
        v = verkehr.Verkehr()
        v.setup()

        netOutput = [0] * 7
        for _ in range(100):
            gameOutput = v.step(lights=netOutput)
            netOutput = genome.activate([gameOutput])[0]
    
            new_out = []
            for out in netOutput:
                if (out < 0.5):
                    new_out.append(0)
                else:
                    new_out.append(1)

            netOutput = new_out

        genome.set_fitness(v.get_cost())

    """
    Builds a new genome based on the 
    expected number of inputs and outputs
    """
    def _buildGenome(self, inputs, outputs):
        logger.info('Build genome %d' %(len(self.genomes)+1,))
        #Intialize one genome network with one layer perceptron
        network = Perceptron(inputs, 128, outputs)

        logger.info('Build genome %d done' %(len(self.genomes)+1,))
        return network

    """
    SPECIFIC to Neural Network.
    Crossover two networks
    """
    def _crossOver(self, netA, netB):
        #Swap (50% prob.)
        if (random.random() > 0.5):
            temp = netA
            netA = netB
            netB = temp
  
        # get dict from net
        netA_dict = netA.as_dict
        netB_dict = netB.as_dict

        # Cross over bias
        netA_biases = netA_dict['biases']
        netB_biases = netB_dict['biases']
        cutLocation = int(len(netA_biases) * random.random())
        netA_updated_biases = np.append(netA_biases[(range(0,cutLocation)),],
            netB_biases[(range(cutLocation, len(netB_biases))),]) 
        netB_updated_biases = np.append(netB_biases[(range(0,cutLocation)),],
            netA_biases[(range(cutLocation, len(netA_biases))),]) 
        netA_dict['biases'] = netA_updated_biases
        netB_dict['biases'] = netB_updated_biases
        netA.reload()
        netB.reload()

        return netA

    """
    Does random mutations across all
    the biases and weights of the Networks
    (This must be done in the JSON to
    prevent modifying the current one)
    """
    def _mutate(self, net):
        # Mutate
        # get dict from net
        net_dict = net.as_dict
        self._mutateDataKeys(net_dict, 'biases', self.mutationProb)
        self._mutateDataKeys(net_dict, 'weights', self.mutationProb)
        net.reload()
        return net

    """
    Given an Array of objects with key `key`,
    and also a `mutationRate`, randomly Mutate
    the value of each key, if random value is
    lower than mutationRate for each element.
    """
    def _mutateDataKeys(self, a, key, mutationRate):
        for k in range(len(a[key])):
        # Should mutate?
            if (random.random() > mutationRate):
                continue
            a[key][k] += a[key][k] * (random.random() - 0.5) * 1.5 + (random.random() - 0.5)
