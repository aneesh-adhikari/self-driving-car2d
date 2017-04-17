# target.py
import math
import random as r
import config as c

class Target:
    def __init__(self, tup):
        self.tup = tup
        self.reset()

    def reset(self):
        self.position = [self.tup[0], self.tup[1]]
