# bfs.py
# ----------
# User Instructions:
# 
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

import numpy as np

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

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

# keep track of the shortest path
path = [[' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ']]


# made a new class to hold the tuple of information desired
class BFS_El:
    
    def __init__(self):
        self.path_length = 0
        self.r = 0
        self.c = 0

    def set(self, path_length, r, c):
        self.path_length = path_length
        self.r = r
        self.c = c
    
    def copy(self, orig_el):
        copy = BFS_El()
        copy.path_length = orig_el.path_length
        copy.r = orig_el.r
        copy.c = orig_el.c
        return copy

    def loc(self):
        return [self.r, self.c]

    def as_list(self):
        return [self.path_length, self.r, self.c]

def valid_loc( loc, grid ):
    return loc[0] >= 0                                 \
            and  loc[1] >= 0                           \
            and  loc[0] < len(grid)                    \
            and  loc[1] < len(grid[0])                 \
            and  searched_already[loc[0]][loc[1]] == 0 \
            and  grid[loc[0]][loc[1]] == 0             \
            
def valid_loc_reverse_path( loc, grid ):
    return loc[0] >= 0                                 \
            and  loc[1] >= 0                           \
            and  loc[0] < len(grid)                    \
            and  loc[1] < len(grid[0])                 \
            and  grid[loc[0]][loc[1]] == 0             \

def add_new_search_locs( search_list, cost ):
    for index,motion in enumerate(delta):
        orig_el = search_list[0]
        new_el = BFS_El()
        new_el.set( orig_el.path_length+cost, orig_el.r+motion[0], orig_el.c+motion[1] )
        if valid_loc( new_el.loc(), grid ):
            search_motions[new_el.r][new_el.c] = index
            search_list.append( new_el )
            searched_already[ new_el.r][new_el.c ] = 1

def search(grid,init,goal,cost):
    init_el = BFS_El();
    init_el.set( 0, init[0], init[1] )
    search_list = [init_el]
    expanded_counter = 0
    while True:
        if len(search_list) == 0:
#             return expanded
            return 'fail'
        search_el = search_list[0]
        search_loc = search_el.loc()
        if search_loc == goal:
            expanded[search_el.r][search_el.c] = expanded_counter
            expanded_counter += 1
#             return expanded
            return search_el.as_list()
        else:
            add_new_search_locs( search_list, cost )
            searched_already[search_el.r][search_el.c] = 1
            expanded[search_el.r][search_el.c] = expanded_counter
            expanded_counter += 1
            search_list.pop(0)

def found_next_step( search_loc, min_steps ):
    search_path_length = search_history[search_loc[0]][search_loc[1]]
    return search_path_length == (min_steps - 1)

def reverse_delta_name( delta_name ):
    if delta_name == '^':
        return 'v'
    elif delta_name == '<':
        return '>'
    elif delta_name == 'v':
        return '^'
    elif delta_name == '>':
        return '<'
    else:
        return None

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

print np.array( search( grid, init, goal, cost ) )
print np.array( get_path() )

