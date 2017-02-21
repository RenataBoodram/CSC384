#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools

def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 8.
       
       
       The input board is specified as a pair (n_grid, last_row). 
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid. 
       If a -1 is in the list it represents an empty cell. 
       Otherwise if a number between 0--9 is in the list then this represents a 
       pre-set board position. E.g., the board
    
       ---------------------  
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists
       
       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]
       
       
       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each 
       column.
    '''
    
#IMPLEMENT
    # Variable list creation
    variable_array = []
    row_ind = 0 
    for row in initial_tenner_board[0]:
        row_var_list = []
        for col in range(0, 10):
            domain = []
            if row[col] == -1:
                domain = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            else:
                domain = [row[col]]
            name = "-V" + str(row_ind + 1) + "," + str(col + 1) + " "
            # Create new variable object
            var = Variable(name, domain)
            row_var_list.append(var)
        # Add the variables for this row to the variable_array 
        variable_array.append(row_var_list)
        row_ind += 1
    print("ROW_IND: ", row_ind)
    row_constr = create_binary_not_equal_constr(variable_array, row_ind - 1, 10, "row")
    #col_csontr = create_binary_not_equal_constr(variable_array, 10, row_ind - 1, "column")
    #diag_constr = create_binary_not_equal_constr(variable_array, 


    csp = CSP(" TENNER-M1")
    for row_var in variable_array:
        for var in row_var:
            csp.add_var(var)

    for c in row_constr:
        csp.add_constraint(c)


    return csp, variable_array

'''Create a list of Constraints'''
def create_binary_not_equal_constr(var_arr, first_range, second_range, constraint_type):
    constraints = []
    for first in range(0,first_range):
        if constraint_type == "row":
            lst = var_arr[first]
        elif constraint_type == "column":
            lst = []
            for row in range(0, second_range):
                lst.append(var_arr[row][first])
        
        for second in range(0, second_range):
            for next_var in range(second + 1, second_range):
                first_var = lst[second]
                sec_var = lst[next_var]
                name = first_var.name + sec_var.name
                # Create a new constraint
                constr = Constraint(name, [first_var, sec_var]) 
                satisfied = []
                for member in lst[second].cur_domain():
                    for next_mem in lst[next_var].cur_domain():
                        if member != next_mem:
                            satisfied.append((member, next_mem))
                constr.add_satisfying_tuples(satisfied)
                constraints.append(constr) 
               
    return constraints    
    
        
            

##############################

def tenner_csp_model_2(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 8.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.
    
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

       However, model_2 has different constraints. In particular,
       model_2 has a combination of n-nary 
       all-different constraints and binary not-equal constraints: all-different 
       constraints for the variables in each row, binary constraints for  
       contiguous cells (including diagonally contiguous cells), and n-nary sum 
       constraints for each column. 
       Each n-ary all-different constraint has more than two variables (some of 
       these variables will have a single value in their domain). 
       model_2 should create these all-different constraints between the relevant 
       variables.
    '''

#IMPLEMENT
