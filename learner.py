import collections
from collections import OrderedDict
import copy
import logging
import random
from tfperceptron import Perceptron_1Layer as Perceptron
import time
from env import verkehr
import gc


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
            self.genomes.append(self._buildGenome(660, 7))

        Perceptron.init()
  
        logger.debug('Build genomes done')
        
        while True:
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
        # best genomes to the front
        self.genomes.sort(key=lambda x: x.fitness)

        f = []
        for g in self.genomes:
            f.append(g.fitness)
        logger.info('Fitness: %s', f)

        bestGenomes = self.genomes[:self.selection]

        # overwrite loosers
        for genome in self.genomes[self.selection:self.genomeUnits]:
            genome.copy(random.choice(bestGenomes))
        # some get crossed
        for genome in self.genomes[self.selection:self.genomeUnits-self.mutations]:
            genome.cross(random.choice(bestGenomes))
        # all loosers get mutated
        for genome in self.genomes[self.selection:self.genomeUnits]:
            factor = genome.fitness / 1000.
            genome.mutate(factor=factor)

        logger.debug('Completed generation %d' %(self.generation,))

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
        logger.debug('Executing genome %d' %(self.genome,))
    
        v = verkehr.Verkehr(15)
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
        logger.debug('Build genome %d' %(len(self.genomes)+1,))
        #Intialize one genome network with one layer perceptron
        network = Perceptron(inputs, 1024, outputs)

        logger.debug('Build genome %d done' %(len(self.genomes)+1,))
        return network
