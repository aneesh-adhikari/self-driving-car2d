# game.py
from pygame.locals import *
import pygame
import math
import time
import util
import config as c
from agent import Agent as A
from target import Target as T
import numpy as np
from grid import Grid

class Game:


    def __init__(self):
        # pygame setup
        pygame.init()
        pygame.display.set_caption(c.game['g_name'])

        self.clock      = pygame.time.Clock()
        self.display    = pygame.display.set_mode(
                            (c.game['width'], c.game['height']))

        self.agents     = []
        target_coor = []
        f = open('L.txt', 'r+')
        s = f.readline()
        while s != '':
            a = s.split(' ')
            target_coor.append((float(a[0]), float(a[1])))
            s = f.readline()
            for i in range(-2, 3):
                for j in range(-2, 3):
                    Grid.grid[int(a[0])+i+j][int(a[1])+i+j] = True

        self.targets    = [T(tup) for tup in target_coor]

        self.generation = 0

        # save terminal
        print "\033[?47h"

    # add an agent with nnet argument
    def add_agent(self, nnet):
        self.agents.append(A(len(self.agents), nnet))

    def reset(self):
        self.agents = []

    # find an agent with weights argument
    def get_ind_fitness(self, ind):
        for a in self.agents:
            for i,weight in enumerate(a.brain.weights):
                if weight != ind[i]:
                    continue
                return a.fitness
        return None

    # game_loop(False) runs the game without graphics
    def game_loop(self, display=True):
        for i in range(c.game['g_time']):

            num = self.game_logic()

            if num == c.game['n_agents']:
                break

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    None
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit()
                    else:
                        None

            # for GA, comment this out for better performance
            if i % c.game['delay'] == 0: self.update_terminal()
            if display: self.process_graphic()

        # for a in self.agents:
        #     startx = c.game['agent_startx']
        #     starty = c.game['agent_starty']
        #     endx = a.position[0]
        #     endy = a.position[1]
        #     a.fitness = int(round(np.sqrt((startx-endx)**2 + (starty-endy)**2)))
        #     if endy < 90:
        #         a.fitness += 1000
        #     if endy < 120:
        #         a.fitness +=750
        #     if endy < 150:
        #         a.fitness += 200
        return [a.fitness for a in self.agents]

    def game_logic(self):
        numCrashed = 0
        for a in self.agents:
            if not a.check_collision(self.targets) != -1:
                a.update(self.targets)
            else:
                numCrashed += 1
            pos = a.position
            index = a.gate

            if index == 19:
                continue
            else:
                s = c.gates[index]
                num = int(s[1:])
                if "x" in s and pos[0] > num:
                    a.gate += 1
                    a.fitness += 1
                elif "y" in s and pos[1] < num:
                    a.gate += 1
                    a.fitness += 5

        self.agents = util.quicksort(self.agents)
        return numCrashed

	# shows graphics of the game using pygame
    def process_graphic(self):
        self.display.fill((0xff, 0xff, 0xff))

        for t in self.targets:
            t_img = pygame.image.load(c.image['target']).convert_alpha()
            self.display.blit(t_img, (t.position[0], t.position[1]))

        if len(self.agents) == c.game['n_agents']:
            for i in range(c.game['n_best']):
                a_img = pygame.transform.rotate(
                    pygame.image.load(c.image['best']).convert_alpha(),
                    self.agents[i].rotation * -180 / math.pi)
                self.display.blit(a_img, (self.agents[i].position[0],
                                        self.agents[i].position[1]))

            for i in range(c.game['n_best'], c.game['n_agents']):
                a_img = pygame.transform.rotate(
                    pygame.image.load(c.image['agent']).convert_alpha(),
                    self.agents[i].rotation * -180 / math.pi)
                self.display.blit(a_img, (self.agents[i].position[0],
                                        self.agents[i].position[1]))
        else:
            for a in self.agents:
                a_img = pygame.transform.rotate(
                    pygame.image.load(c.image['best']).convert_alpha(),
                                    a.rotation * -180 / math.pi)
                self.display.blit(a_img, (a.position[0], a.position[1]))

        pygame.display.update()
        self.clock.tick(c.game['fps'])

    def update_terminal(self):
        print "\033[2J\033[H",
        print c.game['g_name'],
        print "\tGEN.: " + str(self.generation),
        print "\tTIME: " + str(time.clock()) + '\n'

        for a in self.agents:
            print "AGENT " + repr(a.number).rjust(2) + ": ",
            print "FITN.:" + repr(a.fitness).rjust(5)

# run the game without GA and ANN
if __name__ == '__main__':
    g = Game()
    g.game_loop()
    pygame.quit()
