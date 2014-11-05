import collections
import heapq
import random

"""
    Simple neighbor function which picks an index and negates the value at that
    index
"""
def rand_neighbor(solution, clauses):
    newSolution = solution
    indexToMutate = random.randint(0, len(solution)-1)

    newSolution[indexToMutate] = not newSolution[indexToMutate]

    return newSolution

"""
Selects a variable randomly from the top PERCENT of variables that are breaking the
most clauses to negate. With RAND_PERCENTPERCENT chance will call rand_neighbor instead.
With BOT_PERCENT chance with select a variable from the bottom PERCENT of
variables that are breaking the most clauses.
"""
def most_neighbor(solution, clauses):

    RAND_PERCENT = 0.05
    BOT_PERCENT = 0.05
    PERCENT = 0.2

    if random.random() < RAND_PERCENT:
        return rand_neighbor(solution, clauses)

    num_breaking = collections.defaultdict(int)
    for clause in clauses:
        clauseValue = False

        for variable in clause:
            if variable < 0 :
                clauseValue = clauseValue or (not solution[abs(variable)-1])
            else:
                clauseValue = clauseValue or solution[variable-1]

        if not clauseValue:
            for variable in clause:
                num_breaking[variable] += 1



    sortedVars = []
    for variable in num_breaking:
        heapq.heappush(sortedVars, (num_breaking[variable], variable) )

    top10 = []
    if random.random() < BOT_PERCENT:
        top10 = heapq.nsmallest(int(len(num_breaking) * PERCENT), sortedVars)
    else:
        top10 = heapq.nlargest(int(len(num_breaking) * PERCENT), sortedVars)

    indexToPick = random.randint(0, len(top10) - 1)
    maxBreakingVariable = top10[indexToPick][1]

    # Adjust for 0-index based lists
    maxBreakingVariable = abs(maxBreakingVariable) - 1

    newSolution = solution
    newSolution[maxBreakingVariable] = not solution[maxBreakingVariable]

    return newSolution

