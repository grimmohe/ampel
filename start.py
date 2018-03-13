from env import verkehr
import logging

logging.basicConfig(level=logging.DEBUG)

v = verkehr.Verkehr(15)
v.setup()

for i in range(100):
    lights = [i%3%2, i%3%2, i%4%2, i%4%2, i%6%2, i%7%2, i%8%2]
    print(lights)
    v.step(lights=lights)

print(v.cost)
