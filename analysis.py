mport matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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

	avgs, = plt.plot(avgs, ls='-', lw = 2, c = 'r', label="Average Fitness")
	bests, = plt.plot(maxes, ls='-', lw = 2, c = 'b', label="Best Fitness")

	first_legend = plt.legend(handles=[bests], loc = 4, bbox_to_anchor=(1, .095))
	ax = plt.gca().add_artist(first_legend)
	plt.legend(handles=[avgs], loc=4, bbox_to_anchor=(1, 0))

	plt.xlabel('Generation Number')
	plt.ylabel('Fitness')


	plt.show()
