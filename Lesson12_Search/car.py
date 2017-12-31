# car.py
# ----------
# User Instructions:
# 
# You are given a car in grid with initial state
# init. Your task is to compute and return the car's 
# optimal path to the position specified in goal; 
# the costs for each motion are as defined in cost.
#
# There are four motion directions: up, left, down, and right.
# Increasing the index in this array corresponds to making a
# a left turn, and decreasing the index corresponds to making a 
# right turn.

import numpy as np

#######################################################################################

class Search_Element: # made a class to hold the search information
    
    def __init__(self):
        self.cost = 0 # cost to get to this location
        self.r    = 0 # row
        self.c    = 0 # column
        self.o    = 0 # orientation

    def set(self, cost, r, c, o):
        self.cost = cost
        self.r    = r
        self.c    = c
        self.o    = o
        
    def __getitem__(self, key):
        return self.cost # pretty hacky, but needed to implement this to get the sort() function to work
    
    def loc(self):
        return [self.r, self.c]

    def as_list(self):
        return [self.path_length, self.r, self.c]
    
#######################################################################################

class Logging_Info:

    def __init__(self):
        self.action_index = None # the action used to arrive at that spot ('R', '#', 'L')
        self.motion_index = None # the motion used to arrive at that spot ([0,0], [-1,0], [0,-1], [-1,-1])
    
#######################################################################################

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
actions = [-1, 0, 1]
action_name = ['R', '#', 'L']

# grid format:
#     0 = navigable space
#     1 = unnavigable space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = [4, 3, 0] # given in the form [row,col,direction]
                 # direction = 0: up
                 #             1: left
                 #             2: down
                 #             3: right
                
goal = [2, 0] # given in the form [row,col]

cost = [2, 1, 20] # cost has 3 values, corresponding to making 
                  # a right turn, no turn, and a left turn

# keep track of the order in which cells were searched
expanded = [[-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1]]

# keep track of motion (represented as an index into `delta`) used to reach each cell
search_history = [[Logging_Info() for c in range(len(grid[0]))] for r in range(len(grid))]

# keep track of the shortest path
path = [[' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ']]

# keep track of the minimum cost to get to the goal
min_path_cost = 0

def valid_loc( loc, grid ):
    return loc[0] >= 0                     \
            and  loc[1] >= 0               \
            and  loc[0] < len(grid)        \
            and  loc[1] < len(grid[0])     \
            and  grid[loc[0]][loc[1]] == 0 \
            
def add_new_search_locs( search_list ):
    for action_index,action in enumerate(actions):
        orig_el = search_list[0]
        new_el  = Search_Element()
        new_o   = (action + orig_el.o) % len(forward)
        motion  = forward[new_o]
        new_el.set( orig_el.cost+cost[action_index], orig_el.r+motion[0], orig_el.c+motion[1], new_o )
        if valid_loc( new_el.loc(), grid ):
            history = Logging_Info()
            history.action_index = action_index
            history.motion_index = new_o
            search_history[new_el.r][new_el.c] = history
            search_list.append( new_el )

def search(grid,init,goal,cost):
    init_el = Search_Element();
    init_el.set( 0, init[0], init[1], init[2] )
    search_list = [init_el]
    expanded_counter = 0
#     counter = 0
    while True:
#         print
#         print "counter: ", counter
#         print np.array( expanded )
#         for x in search_list:
#             print x.loc()
#         if counter == 20:
#             assert 3>4 # TEMP
#         counter += 1
        if len(search_list) == 0: # failed to reach the goal
            print 'fail'
        search_el = search_list[0]
        search_loc = search_el.loc()
        if search_loc == goal: # found the goal
            expanded[search_el.r][search_el.c] = expanded_counter
            expanded_counter += 1
            return
        else: # still looking for the goal
            add_new_search_locs( search_list )
            search_list.pop(0)
            search_list.sort(key=lambda x: x[0])
            expanded[search_el.r][search_el.c] = expanded_counter
            expanded_counter += 1

def find_optimal_path():
    global min_path_cost
    path[goal[0]][goal[1]] = '*'
    cur_loc = goal
    while cur_loc != init:
        action_index = search_history[cur_loc[0]][cur_loc[1]].action_index
        motion_index = search_history[cur_loc[0]][cur_loc[1]].motion_index
        motion = forward[motion_index]
        cur_loc[0] -= motion[0]
        cur_loc[1] -= motion[1]
        path[cur_loc[0]][cur_loc[1]] = action_name[action_index]
        min_path_cost += cost[action_index]

#######################################################################################

search( grid,init,goal,cost )

print "expanded: "
print np.array( expanded )

find_optimal_path()

print "min cost to goal: "
print min_path_cost

print "shortest path: "
print path

# CORRECT OUTPUT:
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
