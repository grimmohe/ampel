from  sim.simulator import Generator, Simulator
from  mentor.mentor import Mentor
from sim.visual import Visual

generator = Generator()
model = generator.buildModel()
sim = Simulator(model, generator)
mentor = Mentor()

visual = Visual()
visual.init(model)

with open('1.json', 'w') as outfile:
        outfile.write(str(model))

for _ in range(10):
    sim.step(mentor.getAction)

    if not visual.update():
        break

with open('2.json', 'w') as outfile:
        outfile.write(str(model))

print(sim.error)
