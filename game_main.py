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
    num_hidden_layers = c.nnet['n_hidden_layers']

    #create new game
    my_game = game.Game()
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    toolbox.register("weights", random.uniform,-4,4)
    # numWeights = ((num_inputs +1) * num_hidden_nodes) + ((num_hidden_nodes+1) * num_outputs)
    numWeights = (num_inputs+1)*num_hidden_nodes[0]
    for i in range(1, num_hidden_layers):
        numWeights += (num_hidden_nodes[i-1]+1)*num_hidden_nodes[i]
    numWeights += num_outputs*(num_hidden_nodes[-1]+1)

    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.weights, n = numWeights)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evalANN)

    #define selection, crossover, and mutuation functions
    toolbox.register("select", tools.selTournament, tournsize = 5)
    toolbox.register("mate", tools.cxUniform, indpb = 0.15)
    toolbox.register("mutate", tools.mutGaussian, mu = 0, sigma = 10, indpb = 0.02)

    CXPB, MUTPB= .15, .2
    NGEN = c.game['n_gens']

    pop = toolbox.population( n = c.game['n_agents'])

    #Create Initial population with its own ANN
    for ind in pop:
        ann = ANN(num_inputs, num_hidden_nodes, num_outputs, ind, num_hidden_layers)
        my_game.add_agent(ann)

    a = my_game.game_loop(False)
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
        percentBest = c.game['percent_best']
        offspring = toolbox.select(pop, tournsize = 2, k = int(c.game['n_agents']*(1-percentBest)))

        #choose 2 of best parents
        #parents = tools.selBest(pop, k = numSelect)
        parents = tools.selBest(pop, k = int(percentBest*c.game['n_agents']))

        #perform crossover and mutation on offspring
        offspring = algorithms.varAnd(offspring,toolbox,CXPB,MUTPB)

        #combine parents and offspring using elitism
        pop[:] = offspring + parents
        count = 1
        #add agents with new brains
        for ind in pop:
            ann = ANN(num_inputs, num_hidden_nodes, num_outputs, ind, num_hidden_layers)
            my_game.add_agent(ann)
        if ( g != NGEN-1):
            a = my_game.game_loop(False)
        else:
            _ = raw_input("waiting")
            a = my_game.game_loop(True)
        avg = sum(a) / c.game['n_agents']
        avgFitness.append(avg)
        bestFitness.append(a[0])
        avgfile.write(str(avg)+'\n')
        bestfile.write(str(a[0]) + '\n')
        #collect fitness values from the simulation
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit


    avgfile.close()
    bestfile.close()
    while(1):
        my_game.game_loop(True)
    #raw_input("Training is over!")
    #while True:
    #    my_game.game_loop(True)

    pygame.quit()

random.seed(3)
run_GA()
