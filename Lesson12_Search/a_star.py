# a_star.py
# -----------
# User Instructions:
#
# Modify the the search function so that it becomes
# an A* search algorithm as defined in the previous
# lectures.
#
# Your function should return the expanded grid
# which shows, for each element, the count when
# it was expanded or -1 if the element was never expanded.
# 
# If there is no path from init to goal,
# the function should return the string 'fail'
#
# Modify the function search so that it returns
# a table of values called expand. This table
# will keep track of which step each node was
# expanded.
#
# Make sure that the initial cell in the grid 
# you return has the value 0.
#
# Modify the the search function so that it returns
# a shortest path as follows:
# 
# [['>', 'v', ' ', ' ', ' ', ' '],
#  [' ', '>', '>', '>', '>', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', '*']]
#
# Where '>', '<', '^', and 'v' refer to right, left, 
# up, and down motions. Note that the 'v' should be 
# lowercase. '*' should mark the goal cell.
#
# You may assume that all test cases for this function
# will have a path from init to goal.
# ----------
import numpy as np

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

# grid = [[0, 0, 1, 0, 0, 0],
#         [0, 0, 1, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0],
#         [0, 0, 1, 1, 1, 0],
#         [0, 0, 0, 0, 1, 0]]

# grid = [[0, 0, 1, 0, 0, 0],
#         [0, 0, 1, 0, 0, 0],
#         [0, 0, 1, 0, 1, 0],
#         [0, 0, 1, 0, 1, 0],
#         [0, 0, 0, 0, 1, 0]]

# grid = [[0, 1, 0, 0, 0, 0],
#         [0, 1, 0, 1, 0, 0],
#         [0, 1, 0, 1, 0, 0],
#         [0, 1, 0, 1, 0, 0],
#         [0, 0, 0, 1, 0, 0]]

# grid = [[0, 1, 0, 0, 0, 0],
#         [0, 1, 0, 1, 0, 0],
#         [0, 1, 0, 1, 0, 0],
#         [0, 1, 0, 1, 0, 0],
#         [0, 1, 0, 1, 0, 0]]

# grid = [[0, 0, 1, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0],
#         [0, 0, 1, 0, 1, 0],
#         [0, 0, 1, 0, 1, 0],
#         [0, 0, 1, 0, 1, 0]]

# grid = [[0, 1, 1, 1, 1],
#         [0, 1, 0, 0, 0],
#         [0, 0, 0, 1, 0],
#         [1, 1, 1, 1, 0],
#         [0, 0, 0, 1, 0]]

# grid = [[0, 0, 1, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0],
#         [0, 0, 1, 0, 1, 0],
#         [0, 0, 1, 0, 1, 0],
#         [0, 0, 1, 0, 1, 0]]

# grid = [[0, 0, 1, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0],
#         [0, 0, 1, 1, 0, 0],
#         [0, 0, 1, 0, 0, 0]]

# grid = [[0, 1, 0, 0, 0, 0],
#         [0, 1, 0, 0, 0, 0],
#         [0, 1, 0, 0, 0, 0],
#         [0, 1, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0]]

# grid = [[0, 1, 0, 0, 0, 0],
#         [0, 1, 0, 0, 0, 0],
#         [0, 1, 0, 0, 0, 0],
#         [0, 1, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0]]

grid = [[0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0]]

heuristic = [[9, 8, 7, 6, 5, 4],
             [8, 7, 6, 5, 4, 3],
             [7, 6, 5, 4, 3, 2],
             [6, 5, 4, 3, 2, 1],
             [5, 4, 3, 2, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']

# keep track of which cells we've already searched
searched_already = [[0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0]]

# keep track of the order in which cells were searched
expanded = [[-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1]]

# keep track of motion (represented as an index into `delta`) used to reach each cell
search_motions = [[-1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1]]

# DEBUG: used this to see how the heuristic predicted costs
search_cost = [[-1, -1, -1, -1, -1, -1],
               [-1, -1, -1, -1, -1, -1],
               [-1, -1, -1, -1, -1, -1],
               [-1, -1, -1, -1, -1, -1],
               [-1, -1, -1, -1, -1, -1]]

# keep track of the shortest path
path = [[' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ']]


#######################################################################################
class Search_Element: # made a new class to hold the search information desired 
    
    def __init__(self):
        self.cost = 0        # predicted cost (path_length + h) to get to goal
        self.path_length = 0 # cost to get to this cell
        self.r = 0           # row
        self.c = 0           # col
        self.h = 0           # heuristic value

    def __getitem__(self, key):
        return self.cost # pretty hacky, but needed to implement this to get the sort() function to work

    def set(self, path_length, r, c, h):
        self.cost = path_length + h
        self.path_length = path_length
        self.r = r
        self.c = c
        self.h = h
    
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
            
def add_new_search_locs( search_list, cost ):
    for index,motion in enumerate(delta):
        orig_el = search_list[0]
        new_el = Search_Element()
        new_el.path_length = orig_el.path_length+cost
        new_el.r = orig_el.r+motion[0]
        new_el.c = orig_el.c+motion[1]
        if valid_loc( new_el.loc(), grid ):
            new_el.h = heuristic[new_el.r][new_el.c]
            new_el.cost = new_el.path_length + new_el.h
            search_motions[new_el.r][new_el.c] = index
            search_list.append( new_el )
            searched_already[new_el.r][new_el.c] = 1
            search_cost[new_el.r][new_el.c] = new_el.cost

def search(grid,init,goal,cost,heuristic):
    init_el = Search_Element();
    init_el.set( 0, init[0], init[1], heuristic[init[0]][init[1]] )
    search_list = [init_el]
    expanded_counter = 0
    while True:
        if len(search_list) == 0:
            return 'fail'
        search_el = search_list[0]
        search_loc = search_el.loc()
        if search_loc == goal:
            expanded[search_el.r][search_el.c] = expanded_counter
            expanded_counter += 1
            return search_el.as_list()
        else:
            add_new_search_locs( search_list, cost )
            search_list.pop(0)
            search_list.sort(key=lambda x: x[0])
            searched_already[search_el.r][search_el.c] = 1
            expanded[search_el.r][search_el.c] = expanded_counter
            expanded_counter += 1

def get_path():
    path[goal[0]][goal[1]] = '*'
    cur_loc = goal
    while cur_loc != init:
        motion_index = search_motions[cur_loc[0]][cur_loc[1]]
        motion = delta[motion_index]
        cur_loc[0] -= motion[0]
        cur_loc[1] -= motion[1]
        path[cur_loc[0]][cur_loc[1]] = delta_name[motion_index]
    return path

# print np.array( grid )
print np.array( search( grid, init, goal, cost, heuristic ) )
print np.array( expanded )
print np.array( get_path() )
# print np.array( search_cost )

