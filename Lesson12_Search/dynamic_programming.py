# dynamic_programming.py
# ----------
# User Instructions:
# 
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal. 
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.
#
# Write a function optimum_policy that returns
# a grid which shows the optimum policy for robot
# motion. This means there should be an optimum
# direction associated with each navigable cell from
# which the goal can be reached.
# 
# Unnavigable cells as well as cells from which 
# the goal cannot be reached should have a string 
# containing a single space (' '), as shown in the 
# previous video. The goal cell should have '*'.
# ----------

import numpy as np

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

# grid = [[0, 0, 0, 0, 0, 0],
#         [0, 0, 1, 0, 0, 0],
#         [0, 0, 1, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0],
#         [0, 0, 1, 1, 1, 0],
#         [0, 0, 0, 0, 1, 0]]

# grid = [[0, 0, 1, 0, 0, 0],
#         [0, 0, 1, 0, 0, 0],
#         [0, 0, 1, 0, 0, 0],
#         [0, 0, 1, 0, 0, 0],
#         [0, 0, 1, 0, 0, 0],
#         [0, 0, 1, 0, 0, 0]]

# grid = [[0, 0, 1, 0, 0, 0],
#         [0, 0, 1, 0, 0, 0],
#         [0, 0, 1, 1, 0, 0],
#         [0, 0, 1, 0, 1, 0],
#         [0, 0, 1, 0, 1, 0],
#         [0, 0, 1, 0, 1, 0]]

# keep track of how much it costs to get from each cell to the goal
values = [[99, 99, 99, 99, 99, 99],
          [99, 99, 99, 99, 99, 99],
          [99, 99, 99, 99, 99, 99],
          [99, 99, 99, 99, 99, 99],
          [99, 99, 99, 99, 99, 99],
          [99, 99, 99, 99, 99, 99]]

# keep track of which cells we've already searched
searched_already = [[0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0]]

# keep track of all possible paths to the goal
paths = [[' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ']]

goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

#######################################################################################
class Search_Element: # made a new class to hold the search information desired 
    
    def __init__(self):
        self.cost = 0 # cost
        self.r    = 0 # row
        self.c    = 0 # col

    def __getitem__(self):
        return self.cost

    def set(self, cost, r, c):
        self.cost = cost
        self.r    = r
        self.c    = c
    
    def loc(self):
        return [self.r, self.c]

    def as_list(self):
        return [self.path_length, self.r, self.c]
#######################################################################################

def valid_loc( loc, grid ):
    return loc[0] >= 0                                 \
            and  loc[1] >= 0                           \
            and  loc[0] < len(grid)                    \
            and  loc[1] < len(grid[0])                 \
            and  searched_already[loc[0]][loc[1]] == 0 \
            and  grid[loc[0]][loc[1]] == 0             \

def reverse_motion_index( motion_index ):
    motion = delta_name[motion_index]
    if motion == 'v':
        return '^'
    elif motion == '>':
        return '<'
    elif motion == '<':
        return '>'
    elif motion == '^':
        return 'v'
    else:
        return None

def add_new_search_locs( search_list, cost ):
    cur_el = search_list[0]
    for index,motion in enumerate(delta):
        new_el = Search_Element()
        new_el.set( cur_el.cost+cost, cur_el.r+motion[0], cur_el.c+motion[1] )
        if valid_loc( new_el.loc(), grid ):
            values[new_el.r][new_el.c] = new_el.cost
            search_list.append(new_el)
            searched_already[new_el.r][new_el.c] = 1
            paths[new_el.r][new_el.c] = reverse_motion_index(index)

def compute_value(grid,goal,cost):

    # initialization
    cur_el = Search_Element()
    cur_el.set( 0, goal[0], goal[1] )
    search_list = [cur_el]
    values[cur_el.r][cur_el.c] = 0
    searched_already[cur_el.r][cur_el.c] = 1
    paths[cur_el.r][cur_el.c] = '*'

    # BFS starting from goal until all valid locations have been searched
    while len(search_list) > 0:
        add_new_search_locs( search_list, cost )
        search_list.pop(0)

compute_value( grid, goal, cost )
print np.array( values )
print np.array( paths  )

