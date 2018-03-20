import env.verkehr
import logging
from learner import Learner

logging.basicConfig(level=logging.INFO)

learner = Learner(genomeUnits=10, selection=1, mutations=9, mutationProb=0.02)
learner.state = 'LEARNING'
learner.startLearning()

