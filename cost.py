"""
    Cost is the number of clauses incorrect. We want to MINIMIZE this!
"""
def cost(solution, clauses):
    numClausesCorrect = 0
    for clause in clauses:
        clauseValue = False

        for variable in clause:
            if variable < 0 :
                clauseValue = clauseValue or (not solution[abs(variable)-1])
            else:
                clauseValue = clauseValue or solution[variable-1]

        if clauseValue:
            numClausesCorrect += 1

    return len(clauses) - numClausesCorrect


if __name__ == '__main__':
    clauses = [ [1, 2, 3], [-3, -4, -2], [-1, -2, -3] ]
    solution = [True, True, True, True, True, True]
    print cost(clauses, solution)
