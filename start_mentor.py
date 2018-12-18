import sim.simulator
import mentor.mentor

generator = sim.simulator.Generator()
model = generator.buildModel()
sim = sim.simulator.Simulator(model, generator)

mentor = mentor.mentor.Mentor()

for _ in range(1000):
    sim.step(mentor.getAction)

print(sim.error)