import config as c

#class to represent a grid, used as a static variable
class Grid:
    grid = [[False for i in range(c.game['width'])] for i in range(c.game['height'])]
