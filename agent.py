# agent.py
from __future__ import division
import math
import pygame
import random as r
import config as c
import copy
import numpy as np

class Agent:
    def __init__(self, number, brain):
        self.number         = number # agent number
        self.brain          = brain
        self.fitness        = 0 # fitness
        self.t_closest      = 0 # index of the closest target
        self.speed          = 0.0 # movement speed
        self.track          = [4., 4.] # [l_track, r_track]
        self.vision         = [0.0, 0.0] # [x, y] vision
        self.position       = [0,0] #placeholder, set in reset
        self.hasCrashed     = False
        self.reset()

    def reset(self):
        self.fitness = 0
        self.rotation = (math.pi*1.5)
        self.position = [c.game['agent_startx'], c.game['agent_starty']] # [x, y] position
        self.hasCrashed = False
        self.vision[0] = -math.sin(self.rotation)
        self.vision[1] = math.cos(self.rotation)


    def update(self, targets):

        straightdist = -1.0
        checkpos = copy.deepcopy(self.position)
        while straightdist == -1.0:
            if checkpos[0] >= 800 or checkpos[1] >= 800:
                print checkpos
                print 'well shit'
                return
            s = pygame.display.get_surface()
            #print s.get_at((int(round(checkpos[0])), int(round(checkpos[1])))).g
            color = s.get_at((int(checkpos[0]), int(checkpos[1])))
            # print color
            if color.g == 255 and color.r == 0:
                straightdist = np.sqrt((checkpos[0]-self.position[0])**2 + (checkpos[1]-self.position[1])**2)
            else:
                checkpos = [checkpos[0]+self.vision[0]*.9, checkpos[1] + self.vision[1]*.9]

        checkpos = copy.deepcopy(self.position)
        leftdist = -1.0
        tempvis = [-math.sin(self.rotation-((math.pi/2))), math.cos(self.rotation-((math.pi/2)))]
        while leftdist == -1.0:
            if checkpos[0] >= 800 or checkpos[1] >= 800:
                print checkpos
                print 'yikes'
            s = pygame.display.get_surface()
            #print s.get_at((int(checkpos[0]), int(checkpos[1]))).g
            color = s.get_at((int(checkpos[0]), int(checkpos[1])))
            if color.g == 255 and color.r == 0:
                leftdist = np.sqrt((checkpos[0]-self.position[0])**2 + (checkpos[1]-self.position[1])**2)
            else:
                checkpos = [checkpos[0]+tempvis[0]*.9, checkpos[1] + tempvis[1]*.9]


        checkpos = copy.deepcopy(self.position)
        rightdist = -1.0
        tempvis = [-math.sin(self.rotation+((math.pi/2))), math.cos(self.rotation+((math.pi/2)))]
        while rightdist == -1.0:
            if checkpos[0] >= 800 or checkpos[1] >= 800:
                print checkpos
                print 'oh no'
            s = pygame.display.get_surface()
            #print s.get_at((int(checkpos[0]), int(checkpos[1]))).g
            color = s.get_at((int(checkpos[0]), int(checkpos[1])))
            if color.g == 255 and color.r == 0:
                rightdist = np.sqrt((checkpos[0]-self.position[0])**2 + (checkpos[1]-self.position[1])**2)
            else:
                checkpos = [checkpos[0]+tempvis[0]*.9, checkpos[1] + tempvis[1]*.9]

        checkpos = copy.deepcopy(self.position)
        NWDist = -1.0
        tempvis = [-math.sin(self.rotation-((math.pi/4))), math.cos(self.rotation-((math.pi/4)))]
        while NWDist == -1.0:
            if checkpos[0] >= 800 or checkpos[1] >= 800:
                print checkpos
                print 'uh oh'
            s = pygame.display.get_surface()
            #print s.get_at((int(checkpos[0]), int(checkpos[1]))).g
            color = s.get_at((int(checkpos[0]), int(checkpos[1])))
            if color.g == 255 and color.r == 0:
                NWDist = np.sqrt((checkpos[0]-self.position[0])**2 + (checkpos[1]-self.position[1])**2)
            else:
                checkpos = [checkpos[0]+tempvis[0]*.9, checkpos[1] + tempvis[1]*.9]


        checkpos = copy.deepcopy(self.position)
        NEDist = -1.0
        tempvis = [-math.sin(self.rotation+((math.pi/4))), math.cos(self.rotation+((math.pi/4)))]
        while NEDist == -1.0:
            if checkpos[0] >= 800 or checkpos[1] >= 800:
                print 'FUCK'
            s = pygame.display.get_surface()
            #print s.get_at((int(checkpos[0]), int(checkpos[1]))).g
            color = s.get_at((int(checkpos[0]), int(checkpos[1])))
            if color.g == 255 and color.r == 0:
                NEDist = np.sqrt((checkpos[0]-self.position[0])**2 + (checkpos[1]-self.position[1])**2)
            else:
                checkpos = [checkpos[0]+tempvis[0]*.9, checkpos[1] + tempvis[1]*.9]

        # get vector to closest mine
        closest = self.get_closest_target(targets)
        dist = math.sqrt(closest[0] * closest[0] + closest[1] * closest[1])

        normalized = [0.0, 0.0]
        if dist != 0:
            normalized = [closest[0]/dist, closest[1]/dist]

        # inputs for neural network
        inputs = []

        inputs.append(straightdist)
        inputs.append(rightdist)
        inputs.append(leftdist)
        inputs.append(NWDist)
        inputs.append(NEDist)

        # print inputs

        # outputs from neural network
        outputs = self.brain.evaluate(inputs)
        self.track[0] = outputs[0]
        self.track[1] = outputs[1]

        # define rotation rate
        r_rotation = self.track[0] - self.track[1]
        if r_rotation < c.game['r_min']:
            r_rotation = c.game['r_min']
        elif r_rotation > c.game['r_max']:
            r_rotation = c.game['r_max']

        # update rotation
        self.rotation += r_rotation

        # update speed
        self.speed = self.track[0] + self.track[1]

        # update vision
        self.vision[0] = -math.sin(self.rotation)
        self.vision[1] = math.cos(self.rotation)

        # update position
        self.position[0] += self.vision[0] * self.speed
        self.position[1] += self.vision[1] * self.speed

        # wrap around window limits
        if self.position[0] > c.game['width']:
            self.position[0] = 0.0
        if self.position[0] < 0.0:
            self.position[0] = c.game['width']
        if self.position[1] > c.game['height']:
            self.position[1] = 0.0
        if self.position[1] < 0.0:
            self.position[1] = c.game['height']

    def get_closest_target(self, targets):
        closest = float('inf')
        closestVec = [0.0, 0.0]

        # search for the closest mine
        for index, t in enumerate(targets):
            diff = [self.position[0] - t.position[0],
                    self.position[1] - t.position[1]]
            dist = math.sqrt(diff[0] * diff[0] + diff[1] * diff[1])

            if dist < closest:
                closest = dist
                closestVec = diff
                self.t_closest = index

        return closestVec

    def check_collision(self, targets):
        closest = targets[self.t_closest]
        diff = [self.position[0] - closest.position[0],
                self.position[1] - closest.position[1]]
        dist = math.sqrt(diff[0] * diff[0] + diff[1] * diff[1])

        if dist < (c.game['s_target'] + c.game['s_agent']):
            self.hasCrashed = True
            return self.t_closest

        return -1
