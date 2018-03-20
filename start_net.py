import env.verkehr
import logging
from learner import Learner

logging.basicConfig(level=logging.INFO)

learner = Learner(genomeUnits=10, selection=1, mutations=5, mutationProb=0.0007)
learner.state = 'LEARNING'
learner.startLearning()

