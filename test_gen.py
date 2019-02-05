from sim.generator import Generator
from sim.visual import Visual
import json

gen = Generator()
model = gen.buildModel()

#print(model)

visual = Visual()
visual.init(model)


#with open('model.json', 'w') as outfile: 
#    outfile.write(json.dumps(model, default=lambda o: o.__dict__, sort_keys=True, indent=4))

#with open('streetLines.json', 'w') as outfile: 
#    outfile.write(json.dumps(visual.streets, default=lambda o: o.__dict__, sort_keys=True, indent=4))


#print(json.dumps(visual.streets, default=lambda o: o.__dict__, sort_keys=True, indent=4))

while visual.running:
    visual.update()

