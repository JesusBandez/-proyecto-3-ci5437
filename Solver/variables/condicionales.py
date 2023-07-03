import itertools
def sum_greater_or_equal(bidict, variables, k):

    subsets = list(itertools.combinations(variables, len(variables)-k+1))
    clauses = len(subsets)
    constrainsts = ''
    for subet in subsets:
        for var in subet:
            constrainsts += f'{bidict[var]} '

        constrainsts += '0\n'
    return constrainsts, clauses


def sum_less_or_equal(bidict, variables, k):
    
    subsets = list(itertools.combinations(variables, k+1))
    clauses = len(subsets)
    constrainsts = ''
    for subet in subsets:
        for var in subet:
            constrainsts += f'-{bidict[var]} '

        constrainsts += '0\n'

    return constrainsts, clauses