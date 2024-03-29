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
    constraints = []
    row_ind = len(initial_tenner_board[0])

    # Variable list creation
    variable_array = create_var_list(initial_tenner_board[0])

    for col in range(0, 10):
        constr = create_nary_constr(variable_array, initial_tenner_board[1], row_ind, col)
        constraints.append(constr)

    # Create binary constraints of not-equal
    prev_domain = -2
    for row in range(0, row_ind):
        lst = variable_array[row]
        for col in range (0, 10):
            # Make sure all values in the same row are not equal
            first_var = lst[col]
            if first_var.cur_domain_size() == 1:
                prev_domain = first_var.cur_domain()[0]
            else:
                prev_domain = -2

            for next_col in range(col + 1, 10):
                sec_var = lst[next_col]

                name = first_var.name + sec_var.name

                # Create new constraint
                constr = create_constr(name, [first_var, sec_var])
                constraints.append(constr)

            # Check adjacent cells below 
            var_pairs = []
            if row != row_ind - 1:
                name = ""
                # Check diagonal left
                if col != 0:  
                    sec_var = variable_array[row + 1][col - 1]
                    name = first_var.name + sec_var.name
                    if prev_domain != -2 and sec_var.in_cur_domain(prev_domain):
                        sec_var.prune_value(prev_domain)
                        
                    var_pairs.append([name, first_var, sec_var])
                # Check diagonal right
                if col != 9:
                    sec_var = variable_array[row + 1][col + 1]
                    name = first_var.name + sec_var.name
                    if prev_domain != -2 and sec_var.in_cur_domain(prev_domain):
                        sec_var.prune_value(prev_domain)

                    var_pairs.append([name, first_var, sec_var])

                # Check directly below
                sec_var = variable_array[row + 1][col]
                name = first_var.name + sec_var.name
                if prev_domain != -2 and sec_var.in_cur_domain(prev_domain):
                        sec_var.prune_value(prev_domain)

                var_pairs.append([name, first_var, sec_var])

                for var_pair in var_pairs:
                    constr = create_constr(var_pair[0], [var_pair[1], var_pair[2]])
                    constraints.append(constr)


    csp = CSP("TENNER-M1")
    for row_var in variable_array:
        for var in row_var:
            csp.add_var(var)

    for c in constraints: 
        csp.add_constraint(c)


    return csp, variable_array

def create_var_list(board):
    '''Create list of Variables for all spots on the board.'''
    variable_array = []
    row_ind = 0
    prev_domain = -2 
    for row in board:
        row_var_list = []
        for col in range(0, 10):
            domain = []
            if row[col] == -1:
                domain = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                if prev_domain in domain:
                    domain.remove(prev_domain)
                prev_domain = -2 
            else:
                domain = [row[col]]
                prev_domain = [row[col]]
            name = "V" + str(row_ind + 1) + "," + str(col + 1)
            # Create new variable object
            var = Variable(name, domain)
            row_var_list.append(var)
        # Add the variables for this row to the variable_array
        variable_array.append(row_var_list)
        prev_domain = -2
        row_ind += 1
    return variable_array

def create_constr(name, scope):
    # Create a new constraint
    constr = Constraint(name, [scope[0], scope[1]]) 
    # Check for unique elements
    if scope[0].cur_domain_size() == 1:
        val = scope[0].cur_domain()[0]
        if scope[1].in_cur_domain(val):
            scope[1].prune_value(val)

    if scope[1].cur_domain_size() == 2:
        val = scope[1].cur_domain()[0]
        if scope[0].in_cur_domain(val):
            scope[0].prune_value(val)

    for i in itertools.product(scope[0].cur_domain(), scope[1].cur_domain()):
        if i[0] != i[1]:
            constr.add_satisfying_tuples([i])
               
    return constr    

def create_nary_constr(variable_array, sum_constr, row_ind, col):
    '''Create n-ary column sum constraint, where n is the number of rows.'''
    entire_col = []
    entire_var = []
    name = ""
    prev_domain = -2
    for r in range(0, row_ind):
        var = variable_array[r][col]
        name = "Col-" + str(col)

        # Prune consecutive values in column 
        if prev_domain != 2 and var.in_cur_domain(prev_domain):
            var.prune_value(prev_domain)
        if var.cur_domain_size() == 1:
            prev_domain = var.cur_domain()[0]
        else:
            prev_domain = -2

        entire_col.append(var.cur_domain())
        entire_var.append(var)
    constr = Constraint(name, entire_var)
    for i in pproduct(entire_col):
        if sum(list(i)) == sum_constr[col]:
            constr.add_satisfying_tuples([i])

    return constr

def create_nary_not_eq(variable_array):
    '''Create n-ary row all-diff constraint, where n is the length of the rows.'''
    entire_row = []
    #satisfied = []
    name = ""
    for var in variable_array:
        name += var.name
        entire_row.append(var.cur_domain())
    constr = Constraint(name, variable_array)
    for i in pproduct(entire_row):
        if len(i) == len(set(i)):
            constr.add_satisfying_tuples([i])
    #        satisfied.append(i)
    #constr.add_satisfying_tuples(satisfied)
    return constr 


def pproduct(*args, repeat=1):
    '''itertools.product that takes 2D list as input.
       Original code:
       https://docs.python.org/3/library/itertools.html#itertools.product
    ''' 
    pools = [tuple(p) for pool in args for p in pool] * repeat
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool if y not in x[-1:]]
    for prod in result:
        yield tuple(prod)
    
        
            

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
    constraints = []
    row_ind = len(initial_tenner_board[0])
    # Variable list creation
    variable_array = create_var_list(initial_tenner_board[0])

    for col in range(0, 10):
        constr = create_nary_constr(variable_array, initial_tenner_board[1], row_ind, col)
        constraints.append(constr)


    # Create binary constraints of not-equal
    row_var_name = ""
    prev_domain = -2
    for row in range(0, row_ind):
        lst = variable_array[row]
        for col in range (0, 10):
            # Check adjacent cells below
            var_pairs = []
            if row != row_ind - 1:
                name = ""
                first_var = lst[col]
                if first_var.cur_domain_size() == 1:
                    prev_domain = first_var.cur_domain()[0]
                else:
                    prev_domain = -2
                # Check diagonal left
                if col != 0:
                    sec_var = variable_array[row + 1][col - 1]
                    if prev_domain != -2 and sec_var.in_cur_domain(prev_domain):
                        sec_var.prune_value(prev_domain)

                    name = first_var.name + sec_var.name
                    var_pairs.append([name, first_var, sec_var])
                # Check diagonal right
                if col != 9:
                    sec_var = variable_array[row + 1][col + 1]
                    if prev_domain != -2 and sec_var.in_cur_domain(prev_domain):
                        sec_var.prune_value(prev_domain)

                    name = first_var.name + sec_var.name
                    var_pairs.append([name, first_var, sec_var])

                # Check directly below
                sec_var = variable_array[row + 1][col]
                if prev_domain != -2 and sec_var.in_cur_domain(prev_domain):
                    sec_var.prune_value(prev_domain)

                name = first_var.name + sec_var.name
                var_pairs.append([name, first_var, sec_var])

                for var_pair in var_pairs:
                    constr = create_constr(var_pair[0], [var_pair[1], var_pair[2]])
                    constraints.append(constr)
        constr = create_nary_not_eq(lst)
        constraints.append(constr)


    csp = CSP("TENNER-M2")
    for row_var in variable_array:
        for var in row_var:
            csp.add_var(var)

    for c in constraints:
        csp.add_constraint(c)


    return csp, variable_array

