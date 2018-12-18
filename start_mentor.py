from  sim.simulator import Generator, Simulator
from  mentor.mentor import Mentor
from sim.visual import Visual

generator = Generator()
model = generator.buildModel()
sim = Simulator(model, generator)
mentor = Mentor()

visual = Visual()
visual.init(model)

for _ in range(1000):
    sim.step(mentor.getAction)

    if not visual.update():
        break

print(sim.error)