# constrained_cyclic_smoothing.py
# -------------
# User Instructions
#
# Now you will be incorporating fixed points into
# your smoother. 
#
# You will need to use the equations from gradient
# descent AND the new equations presented in the
# previous lecture to implement smoothing with
# fixed points.
#
# Your function should return the newpath that it
# calculates. 
#
# Feel free to use the provided solution_check function
# to test your code. You can find it at the bottom.
#

from math import *
from copy import deepcopy
import numpy as np

# Do not modify path inside your function.
path=[[0, 0],
      [1, 0],
      [2, 0],
      [3, 0],
      [4, 0],
      [5, 0],
      [6, 0],
      [6, 1],
      [6, 2],
      [6, 3],
      [5, 3],
      [4, 3],
      [3, 3],
      [2, 3],
      [1, 3],
      [0, 3],
      [0, 2],
      [0, 1]]

fix = [1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0]

def print_array(path, newpath):
    for i in range(len(path)):
        print '['+ ', '.join('%.3f'%x for x in path[i]) +'] -> ['+ ', '.join('%.3f'%x for x in newpath[i]) +']'

def smooth(path, fix, weight_data = 0.0, weight_smooth = 0.1, tolerance = 0.00001):
    path = np.array(path).astype(float)
    newpath = np.copy(path).astype(float)
    change = tolerance
    weight_constrained = 0.5 * weight_smooth
    while change >= tolerance:
        change = 0
        for i in range(len(path)):
            if not fix[i]:
                aux = np.copy(newpath[i])
                newpath[i] += weight_data*(path[i] - newpath[i]) \
                              + weight_smooth*(newpath[i-1] + newpath[(i+1)%len(path)] - 2*newpath[i]) \
                              + weight_constrained*( 2*newpath[i-1] - newpath[i-2] - newpath[i] ) \
                              + weight_constrained*( 2*newpath[(i+1)%len(path)] - newpath[(i+2)%len(path)] - newpath[i] )
                change += abs(newpath[i][0] - aux[0]) + abs(newpath[i][1] - aux[1])
    return newpath.tolist()

# newpath = smooth(path, fix)
# print_array(path, newpath)

##### TESTING ######

# --------------------------------------------------
# check if two numbers are 'close enough,'used in
# solution_check function.
#
def close_enough(user_answer, true_answer, epsilon = 0.001):
    if abs(user_answer - true_answer) > epsilon:
        return False
    return True

# --------------------------------------------------
# check your solution against our reference solution for
# a variety of test cases (given below)
#
def solution_check(newpath, answer):
    if type(newpath) != type(answer):
        print "Error. You do not return a list."
        return False
    if len(newpath) != len(answer):
        print 'Error. Your newpath is not the correct length.'
        return False
    if len(newpath[0]) != len(answer[0]):
        print 'Error. Your entries do not contain an (x, y) coordinate pair.'
        return False
    for i in range(len(newpath)):
        for j in range(len(newpath[0])):
            if not close_enough(newpath[i][j], answer[i][j]):
                print 'Error, at least one of your entries is not correct.'
                return False
    print "Test case correct!"
    return True

# --------------
# Testing Instructions
#
# To test your code, call the solution_check function with
# two arguments. The first argument should be the result of your
# smooth function. The second should be the corresponding answer.
# For example, calling
#
# solution_check(smooth(testpath1), answer1)
#
# should return True if your answer is correct and False if
# it is not.

# --------------
# Testing Instructions
# To test your code, call the solution_check function with the argument smooth:
# solution_check(smooth)
#

def solution_check(smooth, eps = 0.0001):
    
    def test_case_str(path, fix):
        assert( len(path) == len(fix) )

        if len(path) == 0:
            return '[]'
        if len(path) == 1:
            s = '[' + str(path[0]) + ']'
            if fix[0]: s += ' #fix'
            return s

        s = '[' + str(path[0]) + ','
        if fix[0]: s += ' #fix'
        for pt,f in zip(path[1:-1],fix[1:-1]):
            s += '\n ' + str(pt) + ','
            if f: s += ' #fix'
        s += '\n ' + str(path[-1]) + ']'
        if fix[-1]: s += ' #fix'
        return s
    
    testpaths = [[[0, 0],[1, 0],[2, 0],[3, 0],[4, 0],[5, 0],[6, 0],[6, 1],[6, 2],[6, 3],[5, 3],[4, 3],[3, 3],[2, 3],[1, 3],[0, 3],[0, 2],[0, 1]],
                 [[0, 0],[2, 0],[4, 0],[4, 2],[4, 4],[2, 4],[0, 4],[0, 2]]]
    testfixpts = [[1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                  [1, 0, 1, 0, 1, 0, 1, 0]]
    pseudo_answers = [[[0, 0],[0.7938620981547201, -0.8311168821106101],[1.8579052986461084, -1.3834788165869276],[3.053905318597796, -1.5745863173084],[4.23141390533387, -1.3784271816058231],[5.250184859723701, -0.8264215958231558],[6, 0],[6.415150091996651, 0.9836951698796843],[6.41942442687092, 2.019512290770163],[6, 3],[5.206131365604606, 3.831104483245191],[4.142082497497067, 4.383455704596517],[2.9460804122779813, 4.5745592975708105],[1.768574219397359, 4.378404668718541],[0.7498089205417316, 3.826409771585794],[0, 3],[-0.4151464728194156, 2.016311854977891],[-0.4194207879552198, 0.9804948340550833]],
                      [[0, 0],[2.0116767115496095, -0.7015439080661671],[4, 0],[4.701543905420104, 2.0116768147460418],[4, 4],[1.9883231877640861, 4.701543807525115],[0, 4],[-0.7015438099112995, 1.9883232808252207]]]
    true_answers = [[[0, 0],[0.7826068175979299, -0.6922616156406778],[1.826083356960912, -1.107599209206985],[2.999995745732953, -1.2460426422963626],[4.173909508264126, -1.1076018591282746],[5.217389489606966, -0.6922642758483151],[6, 0],[6.391305105067843, 0.969228211275216],[6.391305001845138, 2.0307762911524616],[6, 3],[5.217390488523538, 3.6922567975830876],[4.17391158149052, 4.107590195596796],[2.9999982969959467, 4.246032043344827],[1.8260854997325473, 4.107592961155283],[0.7826078838205919, 3.692259569132191],[0, 3],[-0.3913036785959153, 2.030774470796648], [-0.3913035729270973, 0.9692264531461132]],
                    [[0, 0],[1.9999953708444873, -0.6666702980585777],[4, 0],[4.666670298058577, 2.000005101453379],[4, 4],[1.9999948985466212, 4.6666612524128],[0, 4],[-0.6666612524127998, 2.000003692691148]]]
    newpaths = map(lambda p: smooth(*p), zip(testpaths,testfixpts))
    
    correct = True
    
    for path,fix,p_answer,t_answer,newpath in zip(testpaths,testfixpts,
                                                   pseudo_answers,true_answers,
                                                   newpaths):
        if type(newpath) != list:
            print "Error: smooth did not return a list for the path:"
            print test_case_str(path,fix) + '\n'
            correct = False
            continue
        if len(newpath) != len(path):
            print "Error: smooth did not return a list of the correct length for the path:"
            print test_case_str(path,fix) + '\n'
            correct = False
            continue

        good_pairs = True
        for newpt,pt in zip(newpath,path): 
            if len(newpt) != len(pt):
                good_pairs = False
                break
        if not good_pairs:
            print "Error: smooth did not return a list of coordinate pairs for the path:"
            print test_case_str(path,fix) + '\n'
            correct = False
            continue
        assert( good_pairs )
        
        # check whether to check against true or pseudo answers
        answer = None
        if abs(newpath[1][0] - t_answer[1][0]) <= eps:
            answer = t_answer
        elif abs(newpath[1][0] - p_answer[1][0]) <= eps:
            answer = p_answer
        else:
            print 'smooth returned an incorrect answer for the path:'
            print test_case_str(path,fix) + '\n'
            continue
        assert( answer is not None )

        entries_match = True
        for p,q in zip(newpath,answer):
            for pi,qi in zip(p,q):
                if abs(pi - qi) > eps:
                    entries_match = False
                    break
            if not entries_match: break
        if not entries_match:
            print 'smooth returned an incorrect answer for the path:'
            print test_case_str(path,fix) + '\n'
            continue
            
        assert( entries_match )
        if answer == t_answer:
            print 'smooth returned the correct answer for the path:'
            print test_case_str(path,fix) + '\n'
        elif answer == p_answer:
            print 'smooth returned a correct* answer for the path:'
            print test_case_str(path,fix)
            print '''*However, your answer uses the "nonsimultaneous" update method, which
is not technically correct. You should modify your code so that newpath[i][j] is only 
updated once per iteration, or else the intermediate updates made to newpath[i][j]
will affect the final answer.\n'''

solution_check(smooth)
