import env.verkehr

v = env.verkehr.Verkehr()
v.setup()

for i in range(100):
    lights = [i%2, i%3%2, i%4%2, i%5%2, i%6%2, i%7%2, i%8%2]
    v.step(lights=lights)

