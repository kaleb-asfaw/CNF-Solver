Conjunctive Normal Form (CNF), is a way that boolean logic is formatted for predicates that require a conjunction of more than 1 clause (with a clause being a "disjunction of literals", an AND of ORs). The solver in this repository is meant to take a long formula that is in CNF form, and outputs a hash table mapping different statements to a True or False value. While the applications of such solvers may seem limited, converting various problems into CNF logic make the applications of this program much more broad. In the case of this project, I wrote code to convert the starting state of Sudoku into CNF logic, an example of how converting different situations into CNF logic will enable my code to solve unassuming problems. Here is a brief overview of how syntactically integrated the CNF logic into Python:

                                  CNF              CNF in Python
                                p or q -->    [ [(p, True), (q, True)] ]
                                                    
                                p and q -->   [ [(p, True)], [(q, True)] ]
    
To generalize, predicates within the same list represent "OR" statements. In the first example, p-True and q-True tuples being within the same list means that to satisfy that clause, either of them can be true (both being true is NOT required). This contrasts from the second example, where each list has only one predicate. Another way to think about it: the CNF logic is formed as a 2d array, and within every "inner" list, at least ONE of the predicates must be satisfied. For example:

                                CNF                         CNF in Python
                           c and (p or q) -->    [ [(c, True)], [(p, True), (q, True)] ]
          
     (c or not p or q) and b and (d or e) -->    [ [(c, True), (p, False), (q, True)], [(b, True)], [(d, True), (e, True)] ] 

   SCROLL for full formula

In the first example, there are 2 "inner" lists. Each inner list needs at least one of the statements to be true. Since the first "inner" list only has one statement (this is known as a unit clause), it must be true, or else there is no solution to the CNF formula. In the second inner list, either p or q must evaluate to true in order for there to be valid solutions. 

In the second example, the first inner list needs at least 1 statement to be true, so either c is True, p is False, or q is True. The second inner list is a unit clause, menaing b MUST be True for there to exist a valid solution. In the third inner list, either d is True or e is True. 

These are the general rules that this program operates under. Thank you for reading and viewing my code.
