import math
f = open('circle.txt', 'w+')
def printCircle(radius):
    angs = [x * .001 for x in range(628)]
    for a in angs:
        x = int((400 + radius * math.cos(a)))
        y = int((400 + radius * math.sin(a)))
        f.write(str(x) + ' ' + str(y))
        f.write('\n')

printCircle(150)
printCircle(300)
