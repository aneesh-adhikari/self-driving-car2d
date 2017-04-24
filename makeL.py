import math
f = open('L.txt', 'w+')
def makeL(y):
    for i in range(0, y):
        f.write(str(y) + " " + str(i) + "\n")
        f.write(str(i) + " " + str(y) + "\n")
    f.write(str(y) + " " + str(y) + "\n")
def connect(x, y):
    for i in range(x, y):
        f.write(str(1) + " " + str(i) + "\n")
        f.write(str(i) + " " + str(1) + "\n")


makeL(300)
makeL(500)
connect(300,500)
