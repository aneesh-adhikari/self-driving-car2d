from __future__ import division
import random
import math
import pygame


import game
import config

from druvANN import ANN

from deap import base
from deap import creator
from deap import tools
from deap import algorithms


random.seed(30)

# # Read your ANN structure from "config.py":
# num_inputs = config.nnet['n_inputs']
# num_hidden_nodes = config.nnet['n_h_neurons']
# num_outputs = config.nnet['n_outputs']

my_game = game.Game()

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Prepare your individuals below.
# Let's assume that you have a one-hidden layer neural network with 2 hidden nodes:
# You would need to define a list of floating numbers of size: 16 (10+6)
toolbox.register("attr_real", random.uniform, -15, 15)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_real, 30)
toolbox.register("population", tools.initRepeat, list, toolbox.individual, n=30)

# Fitness Evaluation:
def evalANN(individual):
    return my_game.get_ind_fitness(individual),
    # comma at the end is necessarys since DEAP stores fitness values as a tuple

toolbox.register("evaluate", evalANN)

# Define your selection, crossover and mutation operators below:

toolbox.register("select",tools.selTournament, tournsize=3)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=5, indpb=1/30)

toolbox.register("map", map)

# Define EA parameters: n_gen, pop_size, prob_xover, prob_mut:
# You can define them in the "config.py" file too.
CXPB, MUTPB, NGEN = 0.5, 0.1, 50
pop = toolbox.population()

# Create initial population (each individual represents an agent or ANN):
for ind in pop:
    # ind (individual) corresponds to the list of weights
    # ANN class is initialized with ANN parameters and the list of weights
    ann = ANN(4, 4, 2, ind)
    my_game.add_agent(ann)

# Let's evaluate the fitness of each individual.
# First, simulation should be run!
my_game.game_loop(True) # Set it to "False" for headless mode;
#recommended for training, otherwise learning process will be very slow!

f = open('results4.txt', 'w+')

# Let's collect the fitness values from the simulation using
fitnesses = list(map(toolbox.evaluate, pop))
maxFit = -1
total = 0
for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit
    maxFit = fit[0] if fit[0] > maxFit else maxFit
    total += fit[0]
f.write(str(total/len(pop)))
f.write(' ')
f.write(str(maxFit))
f.write('\n')

for g in range(1, NGEN+1):
    my_game.generation += 1
    my_game.reset()
    # Start creating the children (or offspring)

    # First, Apply selection:
    offspring = toolbox.select(pop, len(pop))

    # Apply variations (xover and mutation), Ex: algorithms.varAnd(?, ?, ?, ?)
    offspring = algorithms.varAnd(offspring, toolbox, CXPB, MUTPB)

    # Repeat the process of fitness evaluation below. You need to put the recently
    # created offspring-ANN's into the game (Line 55-89) and extract their fitness values:
    for ind in offspring:
        ann = ANN(4, 4, 2, ind)
        my_game.add_agent(ann)

    offspring_fit = my_game.game_loop(True)
    maxFit = -1
    total = 0
    for ind, fit in zip(offspring, offspring_fit):
        ind.fitness.values = fit,
        maxFit = fit if fit > maxFit else maxFit
        total += fit
    f.write(str(total/len(offspring)))
    f.write(' ')
    f.write(str(maxFit))
    f.write('\n')
    # One way of implementing elitism is to combine parents and children to give them equal chance to compete:
    # For example: pop[:] = pop + offspring
    # Otherwise you can select the parents of the generation from the offspring population only: pop[:] = offspring
    pop[:] = offspring
    # This is the end of the "for" loop (end of generations!)


raw_input("Training is over!")
while True:
    my_game.game_loop(True)


pygame.quit()
