import matplotlib.pyplot as plt


for i in range(0, 10):
	f = open('avg' + str(i) + '.txt', 'r+')
	f2 = open('best' + str(i) + '.txt', 'r+')

	s = f.readline()
	s2 = f2.readline()
	maxes = []
	avgs = []

	while s != '':
		avgs.append(float(s))
		maxes.append(float(s2))
		s = f.readline()
		s2 = f2.readline()

	plt.plot(range(0,len(avgs)), avgs, ls='-', lw = 2, c = 'r')
	plt.plot(range(0,len(maxes)), maxes, ls='-', lw = 2, c = 'b')

	plt.show()
