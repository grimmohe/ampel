import env.verkehr
import logging
from learner import Learner

logging.basicConfig(level=logging.INFO)

learner = Learner(12, 4, 0.2)
learner.state = 'LEARNING'
learner.startLearning()

