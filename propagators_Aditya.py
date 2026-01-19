# =============================
# Student Names: Aditya Shetty
# Group ID: 35
# Date: January 29th 2025
# =============================
# CISC 352
# propagators.py
# desc: 
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

    1. prop_FC (worth 0.5/3 marks)
        - a propagator function that propagates according to the FC algorithm that 
          check constraints that have exactly one Variable in their scope that has 
          not assigned with a value, and prune appropriately

    2. prop_GAC (worth 0.5/3 marks)
        - a propagator function that propagates according to the GAC algorithm, as 
          covered in lecture

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned Variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned Variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any Variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of Variable values pairs are all of the values
      the propagator pruned (using the Variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a Variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining Variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one Variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a Variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned Variable left

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
            if not c.check_tuple(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated Variable. Remember to keep
       track of all pruned Variable,value pairs and return '''
    #IMPLEMENT

    # prop_FC returns (status, pruned_list)
    # status = false
    # pruned_list = (Variable, Value)

    removed = []
    if newVar is None:
        constraints = csp.get_all_cons()
    else:
        constraints = csp.get_cons_with_var(newVar)
    for i in constraints:
        if i.get_n_unasgn() == 1:           # checks if the list of unassigned variables equals 1
            un_var = i.get_unasgn_vars()[0] # from this constraint give me the variable that hasnt been assigned yet
                                            # get_unasgn_vars list of unassigned variables 
                                            # [0] -> indexe of the last unassigned variable
            for val in un_var.cur_domain(): # checks the domain of the last remainign unassigned variable
                if not i.has_support(un_var, val):  # Checks if there is a value in the domain of the unassigned domain that has a supproting tuple that abides by the constraint
                    removed.append((un_var, val))   # if not append it to the removed list
                    un_var.prune_value(val)         # prune the value from the variables current domain
            if un_var.cur_domain_size() == 0:
                return False, removed

    return True, removed

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    #IMPLEMENT
    removed = []

    if newVar is None:
        queue = csp.get_all_cons()
    else:
        queue = csp.get_cons_with_var(newVar)

    while queue:
        con = queue.pop(0) # The constraints that need to be checked 
        scope = con.get_scope() # THe current scope of that constraint(The variables associated wiht the constraint)

        for var in scope: # The variables in the current constraint
            for val in var.cur_domain(): # values associated with the variabled

                if not con.has_support(var, val): # If there does not exist a tupel that is associated withe the current variable's value
                    if (var, val) not in removed: # Checks if that tuple is not removed
                        var.prune_value(val)      # If not remove the value from the variable domain
                        removed.append((var, val)) # append it to the removed list

                    if var.cur_domain_size() == 0: # If the current domain size is 0, menaing there are no tuple values that work for the given constraint , return False 
                                                   # and the removed list
                        return False, removed

                    for c in csp.get_cons_with_var(var): # For GAC you have to check all fo the values for all fo the variables for all of the constraints
                        if c not in queue:               # If the constriant is not in the queue, append it
                            queue.append(c)              
    return True, removed
