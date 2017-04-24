import matplotlib.pyplot as plt

f = open('avg.txt', 'r+')
f2 = open('best.txt', 'r+')

s = f.readline()
s2 = f2.readline()
maxes = []
avgs = []

while s != '':
	avgs.append(int(s))
	maxes.append(int(s2))
	s = f.readline()
	s2 = f2.readline()

plt.plot(range(0,98), avgs, ls='-', lw = 2, c = 'r')
plt.plot(range(0,98), maxes, ls='-', lw = 2, c = 'b')

plt.show()
