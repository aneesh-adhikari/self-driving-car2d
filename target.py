# target.py
import math
import random as r
import config as c
import numpy as np

class Target:
    def __init__(self, tup):
        self.tup = tup
        self.reset()

    def reset(self):
        self.position = [self.tup[0], self.tup[1]]

    def isInside(self, a):
        x, y = a[0], a[1]
        dist = np.sqrt((x-self.position[0])**2 + (y-self.position[1])**2)
        return dist < c.game['s_target']
