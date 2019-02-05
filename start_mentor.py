from  sim.simulator import Generator, Simulator
from  mentor.mentor import Mentor
#from sim.visual import Visual

stepSize = 1.0

generator = Generator()
model = generator.buildModel()
sim = Simulator(model, generator, stepSize)
sim.init()
mentor = Mentor(stepSize)

#visual = Visual()
#visual.init(model)

#with open('1.json', 'w') as outfile:
#        outfile.write(str(model))

for _ in range(100):
    sim.step(mentor.getAction)

    #if not visual.update():
    #    break

#with open('2.json', 'w') as outfile:
#        outfile.write(str(model))

print(sim.error)
