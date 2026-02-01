# =============================
# Student Names: Aditya Shetty (SID : 20320373, 21ass17@queensu.ca)
# Group ID: 35
# Date: January 29th 2026
# =============================
# CISC 352
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all Variables in the given csp. If you are returning an entire grid's worth of Variables
they should be arranged linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional Variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 0.5/3 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
| n^2-n | n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '%' for modular addition
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *
import itertools

def binary_ne_grid(cagey_grid):

    n = cagey_grid[0] # cage size 
    domain = list(range(1, n+1))  # domain size
    # set row col and cell holding
    row_vars = []
    col_vars = []
    cells = {}

    # Iterate through both the rows index and record them as the row_name
    for i in range(n):
        for j in range(n):
            row_name = f"Cell({i+1},{j+1})"

            # The current cell is the Variable and its domain value
            cell = Variable(row_name, domain)

            # append the row and column variables to the cell
            row_vars.append(cell)
            col_vars.append(cell)

            cells[(i+1, j+1)] = cell

    # create the CSP variabe as the Binray grid using the row_variables as the count
    csp = CSP(f"{n}x{n}-Binary-NE-Grid", row_vars)

    for var in row_vars:  # add all variables to csp
        csp.add_var(var)

    for i in range(n):
        # collect all cells in row i
        row_cells = []
        for j in range(n):
            row_cells.append(cells[(i+1, j+1)])

        # compare each pair in the row
        for index1 in range(len(row_cells)):
            for index2 in range(index1 + 1, len(row_cells)):
                first_cell = row_cells[index1]
                second_cell = row_cells[index2]

                # See if the constraint is satsfied between the first and second cell
                constraint = Constraint(
                    f"Row{i+1}-{first_cell.name}!={second_cell.name}",
                    [first_cell, second_cell]
                )

                # Create a list of satisfying row and column cells
                sat_tuples = []
                for value1 in domain:
                    for value2 in domain:
                        if value1 != value2:
                             # If constraint is satisfied append
                            sat_tuples.append((value1, value2))

                # Add the constraint and the satisfying tuple list
                constraint.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(constraint)

    # Iterate through columns
    # Do the same as with rows
    for j in range(n):
        col_cells = []
        for i in range(n):
            col_cells.append(cells[(i+1, j+1)])

        for index1 in range(len(col_cells)):
            for index2 in range(index1 + 1, len(col_cells)):
                first_cell = col_cells[index1]
                second_cell = col_cells[index2]

                constraint = Constraint(
                    f"Col{j+1}-{first_cell.name}!={second_cell.name}",
                    [first_cell, second_cell]
                )

                sat_tuples = []
                for value1 in domain:
                    for value2 in domain:
                        if value1 != value2:
                            sat_tuples.append((value1, value2))

                constraint.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(constraint)

    return csp, row_vars


def nary_ad_grid(cagey_grid):

    # Initialize the size as n
    n = cagey_grid[0]
    # Initialize domain 
    domain = []
    # find each value in the domain and append it
    for val in range(1, n + 1):
        domain.append(val)
    
    # use itertools to iterate thethe pairs of the domain
    var_arr = []
    index_pairs = list(itertools.product(domain, domain))
    for pair in index_pairs:
        # name the pair and append the cell name to the variable domain list
        cell_name = "Cell(" + str(pair[0]) + "," + str(pair[1]) + ")"
        var_arr.append(Variable(cell_name, domain))

    # all row and col constraints
    constraint = []

    for i in range(n):

        row_vars = []
        # base index of row i and all n variables in the array
        base = i * n
        for k in range(n):
            # add each cell to current row
            row_vars.append(var_arr[base + k])

        # create the nary for all constraints in this row

        row_constraint = Constraint("Row-AD-{}".format(i + 1), row_vars)

        #append all all permutations of the domain list as row tuples
        row_tuples = []
        perms = itertools.permutations(domain)
        for p in perms:
            row_tuples.append(p)

        # add the satisfying row pairs , to the constriant list
        row_constraint.add_satisfying_tuples(row_tuples)
        constraint.append(row_constraint)


        # do the same thing with the columns 
        col_vars = []
        for l in range(n):
            # move down the grid by jumping n positions each time
            col_vars.append(var_arr[i + l * n])

        col_constraint = Constraint("Col-AD-{}".format(i + 1), col_vars)

        col_tuples = []
        perms = itertools.permutations(domain)
        for p in perms:
            col_tuples.append(p)

        col_constraint.add_satisfying_tuples(col_tuples)
        constraint.append(col_constraint)

    # Creat the nxn nary grid 
    csp = CSP("{}x{}-N-naryGrid".format(n, n), var_arr)

    # add all the sontraints to the inital csp list and return
    for con in constraint:
        csp.add_constraint(con)

    return csp, var_arr

def cagey_csp_model(cagey_grid):
    # size of the grid
    n = cagey_grid[0]

    # base grid using not equal constraint
    csp, var_arr = binary_ne_grid((n, []))

    # iterate through each cage
    for cage in cagey_grid[1]:

        # inital target, operator and list of cage variables
        target = cage[0]
        operator = cage[2]
        cage_vars = []

        # convert each acage coord into an index and append the vell variable
        for coord in cage[1]:
            index = (coord[0] - 1) * n + (coord[1] - 1)
            cage_vars.append(var_arr[index])

                
        # operator domain
        domain = ["+", "-", "*", "/", "%"]

        # cage operator variable
        cage_oper = Variable(
            "Cage_op({}:{})".format(target, cage_vars),
            domain
        )


        # add the operator variable to the csp
        csp.add_var(cage_oper)

        # find full scope of cage constraint,
        # and apped all cell and operator variables
        varlist = []
        for v in cage_vars:
            varlist.append(v)
        varlist.append(cage_oper)

        # cage constraint
        constraint = Constraint(
            "Cage({}:{})".format(target, cage_vars),
            varlist
        )

        # store current domains of all variables in the constraint
        varDoms = []
        for v in varlist:
            varDoms.append(v.cur_domain())

        # lsit of satisfying tuples for cage restraint
        sat_tuples = []

        # CASE 1) If the operator is unknown or cage has only 1 cell
        if operator != "?":

            varDoms[-1] = [operator]
            # use itertools to create all combinations of variable values
            for t in itertools.product(*varDoms):
                # seperate cell values and operator
                values = list(t[:-1])
                oper = t[-1]
                valid = False

                if len(values) == 1:
                    valid = (values[0] == target)

                # The rest of these operators, do the same thing
                # The compute the value given the specific operation
                # And then check the validity
                elif oper == "+":
                    total = 0
                    for v in values:
                        total += v
                    valid = (total == target)

                elif oper == "*":
                    prod = 1
                    for v in values:
                        prod *= v
                    valid = (prod == target)

                elif oper == "-":
                    for perm in itertools.permutations(values):
                        res = perm[0]
                        for x in perm[1:]:
                            res -= x
                        if res == target:
                            valid = True
                            break

                elif oper == "/":
                    for perm in itertools.permutations(values):
                        res = perm[0]
                        good = True
                        for x in perm[1:]:
                            if x == 0 or res % x != 0:
                                good = False
                                break
                            res //= x
                        if good and res == target:
                            valid = True
                            break

                elif oper == "%":
                    total = 0
                    for v in values:
                        total += v
                    valid = (total % n == target)

                # If the value is valid it is added to the satisfying tuple list
                if valid:
                    sat_tuples.append(t)

            constraint.add_satisfying_tuples(sat_tuples)

        # CASE 2) Unkown opertor
        # The first part of our first condition
        else:
            # If not it tries all other operations
            # The program iterates through all operations 
            # Tries each operation and if the value is not valid tries the next in the sequence
            # If the value is valid the operation is added to the tuple list
            trys = ["+", "-", "*", "/", "%"]

            for oper in trys:

                varDoms[-1] = [oper]

                for t in itertools.product(*varDoms):

                    values = list(t[:-1])

                    valid = False

                    if len(values) == 1:
                        valid = (values[0] == target)

                    elif oper == "+":
                        total = 0
                        for v in values:
                            total += v
                        valid = (total == target)

                    elif oper == "*":
                        prod = 1
                        for v in values:
                            prod *= v
                        valid = (prod == target)

                    elif oper == "-":
                        for perm in itertools.permutations(values):
                            res = perm[0]
                            for x in perm[1:]:
                                res -= x
                            if res == target:
                                valid = True
                                break

                    elif oper == "/":
                        for perm in itertools.permutations(values):
                            res = perm[0]
                            good = True
                            for x in perm[1:]:
                                if x == 0 or res % x != 0:
                                    good = False
                                    break
                                res //= x
                            if good and res == target:
                                valid = True
                                break

                    elif oper == "%":
                        total = 0
                        for v in values:
                            total += v
                        valid = (total % n == target)

                    if valid:
                        sat_tuples.append(t)

            constraint.add_satisfying_tuples(sat_tuples)

        var_arr.append(cage_oper)
        csp.add_constraint(constraint)

    return csp, var_arr