#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the Sokoban warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import numpy as np
# import os for time functions
import os
from scipy.optimize import linear_sum_assignment
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS, sokoban_goal_state #for Sokoban specific classes and problems

#SOKOBAN HEURISTICS
def heur_displaced(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''       
  count = 0
  for box in state.boxes:
    if box not in state.storage:
      count += 1
  return count

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''      
    #We want an admissible heuristic, which is an optimistic heuristic. 
    #It must always underestimate the cost to get from the current state to the goal.
    #The sum Manhattan distance of the boxes to their closest storage spaces is such a heuristic.  
    #When calculating distances, assume there are no obstacles on the grid and that several boxes can fit in one storage bin.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.

    manhattan_dist = 0 

    for pos, restriction in state.boxes.items():
        curr_manhattan = float("inf") 
        for storage_pos in state.storage:
            curr_dist = float("inf") 
            if (state.restrictions is not None) and (storage_pos in state.restrictions[restriction]):
                if (np.sum(np.absolute(np.subtract(pos, storage_pos))) < curr_manhattan):
                    curr_manhattan = curr_dist
        manhattan_dist += curr_manhattan
    return manhattan_dist

def heur_alternate(state):
#IMPLEMENT
    '''a better sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''        
    #heur_manhattan_distance has flaws.   
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.

    dict_len = len(state.boxes)
    cost = np.zero
    # Calculate Euclidean distance
    euc_dist = []
    for pos, restriction in state.boxes.items():
        for storage_pos in state.storage:
            euc_dist.append(np.sum(np.square(np.subtract(pos, storage_pos))))
    linear_sum_assignment(cost) 
     
    

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + (weight * sN.hval)

def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False''' 
    i = 0 
    goal_state = False
    best_state = False
    best_gval = 0
    prune = float("inf") 
    se = SearchEngine('best_first')
    se.init_search(initial_state, sokoban_goal_state, heur_fn)
    while timebound > 0:
        if (i == 0):
             goal_state = se.search(timebound) 
             best_state = goal_state
             if goal_state is not False: 
                 best_gval = goal_state.gval
             i += 1
        else:
             # Current path is worse.
             if (goal_state is not False) and (goal_state.gval >= best_gval):
                 prune = goal_state.gval
                 goal_state = se.search(timebound, (prune, float("inf"), float("inf")))
             elif (goal_state is not False) and (goal_state.gval < best_gval):
                 best_state = goal_state
                 best_gval = goal_state.gval
                 goal_state = se.search(timebound, (prune, float("inf"), float("inf")))
        timebound -= os.times()[0] - se.search_start_time

    return best_state 

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False''' 
    i = 0
    best_state = False # The goal state to return
    goal_state = False # Current goal state
    prune = float("inf") # Value to prune on
    best_path = 0 
    se = SearchEngine('custom')
    wrapped_fval_fn = (lambda sN: fval_function(sN, weight))
    se.init_search(initial_state, sokoban_goal_state, heur_fn, wrapped_fval_fn)

    while timebound > 0:
        if (i == 0):
            goal_state = se.search(timebound)
            best_state = goal_state
            if goal_state is not False:
                curr_hval = heur_fn(goal_state)
                best_path = goal_state.gval + curr_hval
            i += 1
        else:
            if (goal_state is not False):
                curr_hval = heur_fn(goal_state) 
                curr_val = goal_state.gval + curr_hval
                # If the path became worse, change the prune value
                if curr_val >= best_path:
                    prune = curr_val
                # A better path was found
                elif curr_val < best_path:
                    # Change the choice of best goal state 
                    best_state = goal_state
                    best_path = curr_val
                goal_state = se.search(timebound, (float("inf"), float("inf"), curr_val))
        timebound -= os.times()[0] - se.search_start_time
    return best_state 

if __name__ == "__main__":
  #TEST CODE
  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 2; #2 second time limit for each problem
  print("*************************************")  
  print("Running A-star")     

  for i in range(0, 10): #note that there are 40 problems in the set that has been provided.  We just run through 10 here for illustration.

    print("*************************************")  
    print("PROBLEM {}".format(i))
    
    s0 = PROBLEMS[i] #Problems will get harder as i gets bigger

    se = SearchEngine('astar', 'full')
    se.init_search(s0, goal_fn=sokoban_goal_state, heur_fn=heur_displaced)
    final = se.search(timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)    
    counter += 1

  if counter > 0:  
    percent = (solved/counter)*100

  print("*************************************")  
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  print("*************************************") 

  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 8; #8 second time limit 
  print("Running Anytime Weighted A-star")   

  for i in range(0, 10):
    print("*************************************")  
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems get harder as i gets bigger
    weight = 10
    final = anytime_weighted_astar(s0, heur_fn=heur_displaced, weight=weight, timebound=timebound)

    if final:
      final.print_path()   
      solved += 1 
    else:
      unsolved.append(i)
    counter += 1      

  if counter > 0:  
    percent = (solved/counter)*100   
      
  print("*************************************")  
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  print("*************************************") 



