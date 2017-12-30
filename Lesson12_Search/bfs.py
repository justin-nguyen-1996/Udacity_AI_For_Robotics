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

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 0]]

# grid = [[0, 1, 0, 0, 0, 0],
#         [0, 1, 0, 1, 0, 0],
#         [0, 1, 0, 1, 0, 0],
#         [0, 1, 0, 1, 0, 0],
#         [0, 1, 0, 1, 0, 0]]

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

def valid_loc( el, grid ):
    return el.r >= 0                               \
            and  el.c >= 0                         \
            and  el.r < len(grid)                  \
            and  el.c < len(grid[0])               \
            and  searched_already[el.r][el.c] == 0 \
            and  grid[el.r][el.c] == 0             \

def add_new_search_locs( search_list, cost ):
    for motion in delta:
        orig_el = search_list[0]
        new_el = BFS_El()
        new_el.set( orig_el.path_length+cost, orig_el.r+motion[0], orig_el.c+motion[1] )
        if valid_loc( new_el, grid ):
            search_list.append( new_el )
            searched_already[ new_el.r][new_el.c ] = 1

def search(grid,init,goal,cost):
    init_el = BFS_El();
    init_el.set( 0, init[0], init[1] )
    search_list = [init_el]
#     temp_counter = 0
    while True:
        if len(search_list) == 0:
            return 'fail'
        search_el = search_list[0]
        search_loc = search_el.loc()
#         print; print("search_loc: "); print(search_loc);
#         if temp_counter == 6:
#             pass
#             assert 3>4 # TEMP
#         else:
#             temp_counter += 1
#             import numpy as np
#             print; print("np.array(searched_already): "); print(np.array(searched_already));
        if search_loc == goal:
            return search_el.as_list()
        else:
            add_new_search_locs( search_list, cost )
            searched_already[ search_el.r][search_el.c ] = 1
            search_list.pop(0)

print search( grid, init, goal, cost )
