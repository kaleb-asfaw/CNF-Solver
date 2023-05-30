import sys
import doctest
import helpers as f

sys.setrecursionlimit(10_000)

def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """
    # base case #1
    if formula == []:
        return {}

    # base case #2
    if [] in formula:
        return None

    soln = {}
    unit_clauses = f.unit_clause(formula)
    # while loop only executes if bool evaluates to true
    while unit_clauses:
        # this will update the formula
        for literal in unit_clauses:
            formula = f.help_update(formula, (literal[0], literal[1]))
            
            #restate base cases for updated formula
            if [] in formula:
                return None

            soln.setdefault(literal[0], literal[1])
            
            #restated base case for updated formula
            if formula == []:
                return soln
        #recheck if there are any unit clauses in the updated formula
        unit_clauses = f.unit_clause(formula)

    # the first statement of the formula
    literal = formula[0][0]

    if literal[1] is True:
        switch_bool = False
    else:
        switch_bool = True

    #checking both True and False scenarios
    nu_form = f.help_update(formula, literal)
    nu_form2 = f.help_update(formula, (literal[0], switch_bool))

    rec = satisfying_assignment(nu_form)
    if rec is not None:
        soln.update({literal[0]: literal[1]})
        return soln | rec

    rec2 = satisfying_assignment(nu_form2)
    if rec2 is not None:
        soln.update({literal[0]: switch_bool})
        return soln | rec2

    return None

def sudoku_board_to_sat_formula(sudoku_board):
    """
    Generates a SAT formula that, when solved, represents a solution to the
    given sudoku board.  The result should be a formula of the right form to be
    passed to the satisfying_assignment function above.
    """
    formula = []
    dim = len(sudoku_board)
    sub = f.first_subgrid_occ(len(sudoku_board))
    
    
    for row, vals in enumerate(sudoku_board): 
        rows = f.row_coordinates(dim, row) # all coords in row
        formula.extend(f.get_pairs(dim,rows)) 
        formula.extend(f.at_least_clause(dim,rows))

        for col, val in enumerate(vals):
            #to insert unit clauses
            if val != 0:
                formula.append([((row, col, val), True)])
            
            cols = f.col_coordinates(dim, col)
            subs = f.subgrid_coordinates(dim, (row, col))

            #to insert column logic
            if row == 0:
                formula.extend(f.at_least_clause(dim, cols))
                formula.extend(f.get_pairs(dim, cols))
            
            #to insert subgrid logic
            if (row, col) in sub:
                formula.extend(f.get_pairs(dim, subs))
                formula.extend(f.at_least_clause(dim, subs))

            formula.extend(f.get_val_pairs(row, col, dim))

    return formula

def assignments_to_sudoku_board(assignments, n = None):
    """
    Given a variable assignment as given by satisfying_assignment, as well as a
    size n, construct an n-by-n 2-d array (list-of-lists) representing the
    solution given by the provided assignment of variables.

    If the given assignments correspond to an unsolvable board, return None
    instead.
    """
    if assignments is None:
        return None

    if n is None:
        pass

    board = [[0] * n for _ in range(n)]
    for val, truth in assignments.items():
        if truth:
            row, col, num = val
            board[row][col] = num

    return board

def sudoku_solver(incomplete_board, n):
    """
    Given a 2d array representing an incomplete sudoku board and n, the
    dimensions of the array, returns a 2d array solution to that same 
    board.
    """
    #first, we will convert the board to CNF logic
    formula = sudoku_board_to_sat_formula(incomplete_board)
    
    #next, find a solution hash table for that board/CNF logic
    solution_map = satisfying_assignment(formula)

    #finally, we will convert the hash into a 2d array solution
    solution = assignments_to_sudoku_board(solution_map, n)

    return solution



if __name__ == "__main__":
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
    
    # #trial cases/examples
    # formula = [
    #     [("a", True), ("b", True), ("c", True)],
    #     [("a", False), ("f", False)],
    #     [("d", False), ("e", True), ("a", True), ("g", True)],
    #     [("h", False), ("c", True), ("a", False), ("f", True)],
    # ]

    # grid = [
    #     [0, 0, 0, 2],
    #     [0, 0, 0, 1],
    #     [4, 0, 0, 0],
    #     [2, 0, 0, 0],
    # ]
    # board = [
    # [5, 3, 0, 0, 7, 0, 0, 0, 0],
    # [6, 0, 0, 1, 9, 5, 0, 0, 0],
    # [0, 9, 8, 0, 0, 0, 0, 6, 0],
    # [8, 0, 0, 0, 6, 0, 0, 0, 3],
    # [4, 0, 0, 8, 0, 3, 0, 0, 1],
    # [7, 0, 0, 0, 2, 0, 0, 0, 6],
    # [0, 6, 0, 0, 0, 0, 2, 8, 0],
    # [0, 0, 0, 4, 1, 9, 0, 0, 5],
    # [0, 0, 0, 0, 8, 0, 0, 7, 9],
    # ]
    
    # print(sudoku_solver(board, 9))

    

