import env.verkehr
import logging
from learner import Learner
import sys
import tfperceptron

logging.basicConfig(level=logging.INFO)

learner = Learner(genomeUnits=10, selection=1, mutations=9, mutationProb=0.02)
learner.state = 'LEARNING'

if len(sys.argv) > 1:
    tfperceptron.Perceptron.loadTensor(sys.argv[1])

learner.startLearning()

