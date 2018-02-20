import env.verkehr
import logging
from learner import Learner

logging.basicConfig(level=logging.INFO)

learner = Learner(20, 10, 0.2)
learner.state = 'LEARNING'
learner.startLearning()

