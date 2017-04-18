#!/usr/bin/env python

from pygame.locals import *
from game import Game
import pygame
import math
import time
import util
import config as c
import random as r
from agent import Agent as A
from target import Target as T

class Dummy:
    def __init__(self):
        self.outputs = [r.uniform(2., 4.), r.uniform(2., 4.)]

    def evaluate(self, meh=0):
        return self.outputs

# run the game without GA and ANN
if __name__ == '__main__':
    g = Game()

    for _ in range(c.game['n_agents']):
        g.add_agent(Dummy())

    g.game_loop()
    pygame.quit()
