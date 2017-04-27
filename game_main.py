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
from deap import base, creator, tools, algorithms
import numpy as np
import sys
import matplotlib.pyplot as plt


def run_GA():
    #create neural Network Configurations
    num_inputs = c.nnet['n_inputs']
    num_hidden_nodes = c.nnet['n_hidden_nodes']
    num_outputs = c.nnet['n_outputs']
    num_hidden_layers = c.nnet['n_hidden_layers']

    numWeights = (num_inputs+1)*num_hidden_nodes[0] #input layer to first hidden
    for i in range(1, num_hidden_layers):
        numWeights += (num_hidden_nodes[i-1]+1)*num_hidden_nodes[i] #all other layers
    numWeights += num_outputs*(num_hidden_nodes[-1]+1) #last hidden to output

    #get constants
    CXPB, MUTPB, MATPB = c.ga['cx_prob'], c.ga['mut_prob'], c.ga['mate_prob']
    NGEN, TSIZE = c.ga['n_gens'], c.ga['tourn_size']
    mu, sigma, percent_best = c.ga['mut_mu'], c.ga['mut_sigma'], c.ga['percent_best']
    num_agents = c.game['n_agents']

    #initialize game
    my_game = game.Game()

    #ga stuff
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("weights", random.uniform,-4,4)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.weights, n = numWeights)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", lambda ind: (my_game.get_ind_fitness(ind),))

    #define selection, crossover, and mutuation functions
    toolbox.register("select", tools.selTournament, tournsize = TSIZE)
    toolbox.register("mate", tools.cxUniform, indpb = MATPB)
    toolbox.register("mutate", tools.mutGaussian, mu = mu, sigma = sigma, indpb = MUTPB)

    pop = toolbox.population(n = num_agents)

    #Create Initial population with its own ANN
    for ind in pop:
        ann = ANN(num_inputs, num_hidden_nodes, num_outputs, ind, num_hidden_layers)
        my_game.add_agent(ann)

    a = my_game.game_loop(True)    #initial game run
    avg = sum(a) / num_agents

    #collect fitness values from simulation
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    bestfile = open('best.txt', 'w+')
    avgfile = open('avg.txt', 'w+')

    bestfile.write(str(a[0])+'\n')
    avgfile.write(str(avg)+'\n')

    #training
    for g in range(1, NGEN):
        my_game.generation += 1
        my_game.reset()

        #choose top given percentile of best parents
        parents = toolbox.select(pop, k = int((1-percent_best)*num_agents))
        keep = tools.selBest(pop, k = int(percent_best*num_agents))

        #perform crossover and mutation on offspring
        offspring = algorithms.varAnd(parents,toolbox,CXPB,MUTPB)

        #combine parents and offspring using elitism
        pop[:] = offspring + keep
        #add agents with new brains
        for ind in pop:
            ann = ANN(num_inputs, num_hidden_nodes, num_outputs, ind, num_hidden_layers)
            my_game.add_agent(ann)
        if ( g != NGEN-1):
            a = my_game.game_loop(False)
        else:
            _ = raw_input("waiting")
            a = my_game.game_loop(True)
        avg = sum(a) / num_agents
        avgfile.write(str(avg)+'\n')
        bestfile.write(str(a[0]) + '\n')
        #collect fitness values from the simulation
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit


    avgfile.close()
    bestfile.close()
    pygame.quit()

random.seed(3)
run_GA()
