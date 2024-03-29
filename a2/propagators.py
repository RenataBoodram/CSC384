#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newVar=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newVar (newly instaniated variable) is an optional argument.
      if newVar is not None:
          then newVar is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newVar = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newVar = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
#IMPLEMENT
    pruned_vals = []
    if not newVar:
        iterlist = csp.get_all_cons()
    else:
        iterlist = csp.get_cons_with_var(newVar)
    for c in iterlist:
        if c.get_n_unasgn() == 1:
            unassigned = c.get_unasgn_vars()
            dead_end, pruned = FCCheck(c, unassigned[0])
            pruned_vals += pruned

            # If there is a Domain Wipe Out, return it
            if dead_end is False:
                return dead_end, pruned_vals

    return True, pruned_vals

def FCCheck(c, x):
    '''Do forward checking on a single constraint with unassigned variable x.'''
    pruned_vals = []
    for domain_member in x.cur_domain():
        constraint_vars = c.get_scope()
        val_assigns = []
        # Check if making x = constraint_var together with previous
        # assignments to variables in scope C falsify C
        for var in constraint_vars:
            if var == x:
                val_assigns.append(domain_member)
            else:
                assigned_val = var.get_assigned_value()
                val_assigns.append(assigned_val)
        if c.check(val_assigns) is False:
            pruned_vals.append((x, domain_member))
            x.prune_value(domain_member)
        # Constraint was falsified
        if x.cur_domain() == []:
            return False, pruned_vals
    return True, pruned_vals


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
#IMPLEMENT
    queue = []
    pruned_vals = []
    if not newVar:
        iterlist = csp.get_all_cons()
    else:
        iterlist = csp.get_cons_with_var(newVar)
    for c in iterlist:
        queue = [c] + queue
    dead_end, prune = GAC_Enforce(queue, csp)
    pruned_vals = pruned_vals + prune
    if dead_end is False:
        return dead_end, pruned_vals
    return True, pruned_vals

def GAC_Enforce(GACQueue, csp):
    '''GAC-Queue contains all constraints one of whose variables has had its 
       domain reduced.'''
    pruned_vals = []
    while GACQueue != []:
        c = GACQueue.pop()
        all_constr = c.get_scope()
        for constraint in all_constr:
            for member in constraint.cur_domain():
                if (c.has_support(constraint, member) is False):
                    pruned_vals.append((constraint, member))
                    constraint.prune_value(member)
                    if constraint.cur_domain() != []:
                        for constr in csp.get_cons_with_var(constraint):
                            if constr not in GACQueue:
                                GACQueue = [constr] + GACQueue
                    else:
                        return False, pruned_vals
    return True, pruned_vals
