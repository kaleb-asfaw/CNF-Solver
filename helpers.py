import sys
sys.setrecursionlimit(10_000)

#These various functions are meant to simplify the evaluation of CNF logic

def get_variables(formula):
    """
    Given a formula, get all the variables that are used within the formula.
    Takes a formula (2D array) and returns a set of every variable.
    """
    var = set()
    # all variables
    for chain in formula:
        for literal in chain:
            var.add(literal[0])
    return var

def help_update(formula, literal):
    """
    Given a formula, and a tuple of a variable and its boolean value,
    return an updated formula that simplifies the initial formula, as well
    as a dictionary which has values that are apart of the solution.
    """
    new_formula = []
    for chain in formula:
        new_chain = []
        literal_found = False
        for statement in chain:
            # if the literal is satisfied, then chain does not need to be considered
            if literal in chain:
                literal_found = True

            # if the literal is the opposite of the existing boolean, then the boolean
            # value of the chain is dependent on every OTHER literal
            elif statement[0] == literal[0]:
                continue

            # if not related to the literal, then just add it into the new formula
            new_chain.append(statement)

        # if the literal was not found in the formula, then the chain must be considered
        if not literal_found:
            new_formula.append(new_chain)

    return new_formula

def unit_clause(formula):
    """
    Takes a formula and returns a list of unit clauses. If none exist, then
    return an empty list
    """
    if formula is None:
        return []

    unit_clauses = []
    for clause in formula:
        if len(clause) == 1:
            unit_clauses.append(clause[0])

    if not unit_clauses:
        return []

    else:
        return unit_clauses

def subgrid_coordinates(dim, coordinate):
    """
    Given a board's dimensions and the desired coordinate, returns
    a list of coordinates that make up the subgrid (which the 
    provided coordinate is located in).
    """
    row, col = coordinate
    dim_sq = int(dim ** (1 / 2))

    #subgrid row and col indices
    sr = row // dim_sq
    sc = col // dim_sq

    coordinates = []
    for r in range(dim_sq * sr, dim_sq * sr + dim_sq):
        for c in range(dim_sq * sc, dim_sq * sc + dim_sq):
            coordinates.append((r, c))

    return sorted(coordinates)

def row_coordinates(dim, row):
    """
    Given grid dimensions and a desired row, return
    a list of coordinates that occur in the row.
    """
    coordinates = []
    for c in range(dim):
        coordinates.append((row, c))
    return coordinates

def col_coordinates(dim, col):
    """
    Given grid dimensions and a desired column, return
    a list of coordinates that occur in the column.
    """
    coordiantes = []
    for r in range(dim):
        coordiantes.append((r, col))
    return coordiantes


def at_least_clause(dim, coordinates):
    """
    Given a list of coordinates, returns a formula consisiting
    of clauses that state that at least one of the coordinates
    provided has each value.
    """
    formula = []
    for c in coordinates:
        row = c[0]
        col = c[1]
        clause = []
        for val in range(1, dim+1):
            clause.append(((row, col, val), True))
        
        formula.append(clause)
    return formula
        
def get_pairs(dim, coordinates):
    """
    Given a list of coordinates, creates and returns a cnf
    formula that states each value occurs AT MOST once in the 
    provided coordinates.
    """
    formula = []
    for i, coord in enumerate(coordinates):
        for coord2 in coordinates[i+1:]:
            for val in range(1, dim+1):
                ro1, col1 = coord
                ro2, col2 = coord2
                formula.append([((ro1, col1, val), False), ((ro2, col2, val), False)])
    return formula
    
def get_val_pairs(row, col, dim):
    """
    Given a coordinate (row, col), returns a cnf formula that 
    says the coordinate has AT LEAST & AT MOST one of the values.
    """
    formula = []
    clause = []
    # At least 1 value per coordinate
    for val in range(1, dim + 1):
        clause.append(((row, col, val), True))

    formula.append(clause)

    # At most 1 value per coordinate (pairing)
    for start in range(1, dim+1):
        for end in range(start + 1, dim+1):
            if start != end:
                formula.append(
                    [((row, col, start), False), ((row, col, end), False)]
                )

    return formula

def first_subgrid_occ(n):
    """
    Given an n-dimension sudoku board, will return a set of 
    coordinates representing the first occurence of a new subgrid.
    
    *The main purpose of this function is to avoid repetitive CNF 
    logic from being inputed into the solver*
    """
    dim_s = int(n**(1/2))
    coordinates = []
    for row in range(n):
        for col in range(n):
            if col%dim_s == 0 and row%dim_s == 0:
                coordinates.append((row, col))
    
    return coordinates