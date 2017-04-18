import math
f = open('line.txt', 'w+')
def makeLine(y):
    for i in range(0, 800, 5):
        f.write(str(800-i) + " " + str(y))
        f.write('\n')
makeLine(800)
makeLine(350)
