import env.verkehr
import logging
from learner import Learner

logging.basicConfig(level=logging.INFO)

learner = Learner(genomeUnits=15, selection=5, mutations=5, mutationProb=0.001)
learner.state = 'LEARNING'
learner.startLearning()

