import math
f = open('circle.txt', 'w+')
def printCircle(radius, num):
    for i in range(num):
        a = (float(i)/num) * math.pi *2
        x = 400 + radius * math.cos(a)
        y = 400 + radius * math.sin(a)
        f.write(str(x) + ' ' + str(y))
        f.write('\n')
printCircle(150, 100)
printCircle(300, 200)
