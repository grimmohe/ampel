import collections
from collections import OrderedDict
import copy
import logging
import random
from tfperceptron import Perceptron_1Layer as Perceptron
import time
from env import verkehr
import gc
import sys

logger = logging.getLogger('dino.learner')

class Learner(object):

    def __init__(self, genomeUnits, selection, mutations, mutationProb):
        self.genomes = []
        self.generation = 0
        self.shouldCheckExperience = False
        self.genomeUnits = genomeUnits
        self.selection = selection
        self.mutations = mutations
        self.mutationProb = mutationProb
        self.interuptted = False
        self.traffic_sim_mem_depth = 15
        self.traffic_sim_num_cars = 1
        self.traffic_sim_num_iterations = 100


    """
    Build genomes before calling executeGeneration.
    """
    def startLearning(self):

        try:

            # Build genomes if needed
            while (len(self.genomes) < self.genomeUnits):
                self.genomes.append(self._buildGenome(44 * self.traffic_sim_mem_depth, 7))

            Perceptron.init()
    
            logger.debug('Build genomes done')
            
            while True:
                self._executeGeneration()

        except KeyboardInterrupt:
            pass

        

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
        logger.debug('Executing generation %d'%(self.generation,))

        self._executeGenomes()

        if self.generation < 3 or self.generation % 3 == 0:
            self._genify_random_all()
        else:
            self._train()

        self._log_fitness()

        if self.genomes[0].fitness < self.traffic_sim_num_cars * 2.5:
            self.traffic_sim_num_cars += 1
        
        logger.debug('Completed generation %d' %(self.generation,))


    def _genify_random_one(self):
        # best genome to the front
        self.genomes.sort(key=lambda x: x.fitness)

        # get the weight or bias index to mutate
        index = self.genomes[0].get_mutation_index(self.generation)


        # overwrite and mutate loosers
        for genome in self.genomes[self.selection:]:
            genome.copy(random.choice(self.genomes[:self.selection]))
            genome.mutate_index(index, random.random() * 2 - 1)


    def _genify_random_all(self):
        # best genomes to the front
        self.genomes.sort(key=lambda x: x.fitness)

        bestGenomes = self.genomes[:self.selection]

        # overwrite loosers
        for genome in self.genomes[self.selection:]:
            genome.copy(random.choice(bestGenomes))
        # some get crossed
        for genome in self.genomes[self.selection:self.genomeUnits-self.mutations]:
            genome.cross(random.choice(bestGenomes))
        # all loosers get mutated
        for genome in self.genomes[self.selection:]:
            factor = genome.fitness * self.mutationProb / self.traffic_sim_num_cars
            genome.mutate_all_layers(factor=factor)


    def _train(self):
        # best genome to the front
        self.genomes.sort(key=lambda x: x.fitness)

        for genome in self.genomes[self.selection:]:
            master = random.choice(self.genomes[:self.selection])
            genome.learn(master.input, master.output)


    def _log_fitness(self):
        f = []
        for g in self.genomes:
            f.append(g.fitness)
        logger.info('Generation %s cars %s fitness: %s', self.generation, self.traffic_sim_num_cars, f)


    """
    Waits the game to end, and start a new one, then:
    1) Set's listener for sensorData
    2) On data read, applyes the neural network, and
       set it's output
    3) When the game has ended and compute the fitness
    """
    def _executeGenomes(self): 
        genomes = self.genomes
        traffic = []
        result = []

        for g in genomes:
            v = verkehr.Verkehr(self.traffic_sim_mem_depth)
            v.setup(self.traffic_sim_num_cars)
            traffic.append(v)
            g.input.clear() #parameter für genome
            g.output.clear() #ergebnis des netzes
            result.append([0] * 7) #aufbereitetes ergebnis

        for _ in range(self.traffic_sim_num_iterations):
            for g in range(len(genomes)):
                input = traffic[g].step(lights=result[g])
                output = genomes[g].activate([input])

                result[g].clear()
                for out in output[0]:
                    if (out < 0):
                        result[g].append(0)
                    else:
                        result[g].append(1)

                genomes[g].set_fitness(traffic[g].get_cost())


    """
    Builds a new genome based on the 
    expected number of inputs and outputs
    """
    def _buildGenome(self, inputs, outputs):
        logger.debug('Build genome %d' %(len(self.genomes)+1,))
        #Intialize one genome network with one layer perceptron
        network = Perceptron(inputs, 50, outputs)

        logger.debug('Build genome %d done' %(len(self.genomes)+1))
        return network
