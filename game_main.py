#!/usr/bin/env python
import random
from game import Game
import pygame
import math
import time
import util
import game
import config as c
import random as r
from agent import Agent as A
from target import Target as T
from ANN import ANN
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import numpy as np
import sys
import matplotlib.pyplot as plt

def run_GA():
    avgFitness = []
    bestFitness = []
    def evalANN(individual):
        return my_game.get_ind_fitness(individual),

    #create neural Network Configurations
    num_inputs = c.nnet['n_inputs']
    num_hidden_nodes = c.nnet['n_hidden_nodes']
    num_outputs = c.nnet['n_outputs']

    #create new game
    my_game = game.Game()
    creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    toolbox.register("weights", random.uniform,-4,4)
    numWeights = ((num_inputs +1) * num_hidden_nodes) + ((num_hidden_nodes+1) * num_outputs)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.weights, n = numWeights)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evalANN)

    #define selection, crossover, and mutuation functions
    toolbox.register("select", tools.selTournament, tournsize = 2)
    toolbox.register("mate", tools.cxUniform, indpb = 0.15)
    toolbox.register("mutate", tools.mutGaussian, mu = 0, sigma = 1 , indpb = 0.15)

    CXPB, MUTPB, NGEN = .15, .2, 30

    pop = toolbox.population( n = c.game['n_agents'])

    #Create Initial population with its own ANN
    for ind in pop:
        ann = ANN(num_inputs, num_hidden_nodes, num_outputs, ind)
        my_game.add_agent(ann)

    a = my_game.game_loop(True)
    avg = sum(a) / c.game['n_agents']
    avgFitness.append(avg)
    bestFitness.append(a[0])
    #collect fitness values from simulation
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    bestfile = open('best.txt', 'w+')
    avgfile = open('avg.txt', 'w+')

    #training
    for g in range(1, NGEN):
        my_game.generation += 1
        my_game.reset()
        #select 25 of best individuals
        numSelect = int(round(float(g)/NGEN * c.game['n_agents']))
        #offspring = toolbox.select(pop, tournsize = 2, k = c.game['n_agents']-numSelect)
        offspring = toolbox.select(pop, tournsize = 2, k = 28)

        #choose 2 of best parents
        #parents = tools.selBest(pop, k = numSelect)
        parents = tools.selBest(pop, k = 2)

        #perform crossover and mutation on offspring
        offspring = algorithms.varAnd(offspring,toolbox,CXPB,MUTPB)

        #combine parents and offspring using elitism
        pop[:] = offspring + parents
        count = 1
        #add agents with new brains
        for ind in pop:
            ann = ANN(num_inputs, num_hidden_nodes, num_outputs, ind)
            my_game.add_agent(ann)

        a = my_game.game_loop(True)
        avg = sum(a) / c.game['n_agents']
        avgFitness.append(avg)
        bestFitness.append(a[0])
        avgfile.write(str(avg))
        bestfile.write(str(a[0]))
        #collect fitness values from the simulation
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
    gens = range(len(avgFitness))
    gens2 = range(len(avgFitness))
    plt.plot(gens, avgFitness, color = 'black')
    plt.plot(gens2, bestFitness, color = 'blue')
    plt.xlabel('Generation Number')
    plt.ylabel(' Fitness')
    plt.show()

    avgfile.close()
    bestfile.close()

    #raw_input("Training is over!")
    #while True:
    #    my_game.game_loop(True)

    pygame.quit()

# random.seed(3)
run_GA()
