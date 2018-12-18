from sim.generator import Generator
from sim.visual import Visual

gen = Generator()
model = gen.buildModel()

print(gen.buildModel())

visual = Visual()
visual.init(model)

while visual.running:
    visual.update()

