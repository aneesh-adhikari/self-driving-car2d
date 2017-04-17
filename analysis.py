import matplotlib.pyplot as plt

f = open('results4-3.txt', 'r+')

s = f.readline()
maxes = []
avgs = []

while s != '':
	a = map(float, s.split(' '))
	avgs.append(a[0])
	maxes.append(a[1])
	s = f.readline()

plt.plot(range(0,51), avgs, ls='-', lw = 2, c = 'r')
plt.plot(range(0,51), maxes, ls='-', lw = 2, c = 'b')

plt.show()