from constants import *
from cost import cost
from neighbor import most_neighbor
from neighbor import rand_neighbor
from SA import SA

import pickle
import random
import time

"""
    Loads clauses from the given filepath. Returns a list of clauses in the
    form [[x y z 0], ...[a b x 0]] where the letters are numbers representing the
    1-based index into the solution. A negative number indicates a NOT. The
    trailing 0 at the end should be ignored during import.
"""
def loadClauses(filePath):
    clauses = []
    for line in open(filePath):
        line = line.strip().split()

        # Skip blank lines
        if not line:
            continue

        currentClause = []
        for num in line:
            currentClause.append(int(float(num)))

        # Drop the trailing 0
        currentClause = currentClause[:-1]

        clauses.append(currentClause)
    return clauses

def generateRandomSolution(numVariables, probabilityTrue = 0.5):
    solution = []
    for i in range(numVariables):
        if random.random() < probabilityTrue:
            solution.append(True)
        else:
            solution.append(False)
    return solution

if __name__ == '__main__':

    # Add 1 because the file names are 1-based
    allNames = [""]


    # Initialize memory
    all_SA_rand_bests = [[] for i in range(NUM_FILES+1)]
    all_SA_rand_time = [[] for i in range(NUM_FILES+1)]

    print 'Attempts to solve input SATs.'
    for problem in range(FILE_START, FILE_START + NUM_FILES):
        fileMiddlePart = "{0:0>2}".format(problem)
        fileName = FILE_PREFIX + fileMiddlePart + FILE_SUFFIX
        allNames.append(fileName)

        clauses = loadClauses(fileName)

        for trial in range(NUM_TRIALS):
            print 'Solving:', fileName, 'Trial:', trial+1, '/', NUM_TRIALS, '(SA rand)'
            initial_SA_Solution = generateRandomSolution(NUM_VARIABLES)

            # SA
            startTime = time.clock()
            SA_matrix, SA_best = SA(initial_SA_Solution, clauses, T_INITIAL,
                    ALPHA, BETA, M_INITIAL, MAX_TIME, rand_neighbor)
            elapsed = time.clock() - startTime
            all_SA_rand_time[problem].append(elapsed)
            all_SA_rand_bests[problem].append(SA_best)


            pickle.dump(SA_matrix, open('data/all-SA-rand-Matrices_' +
                str(problem) + '_' + str(trial) + '_.p', 'wb'))

    # Dump results
    pickle.dump(all_SA_rand_bests, open('data/all_SA_rand_bests.p', 'wb'))
    pickle.dump(all_SA_rand_time, open('data/all_SA_rand_time.p', 'wb'))
    # Free memory
    del all_SA_rand_bests[:]
    del all_SA_rand_time[:]
    del all_SA_rand_bests
    del all_SA_rand_time


    # Initialize memory
    all_SA_most_bests = [[] for i in range(NUM_FILES+1)]
    all_SA_most_time = [[] for i in range(NUM_FILES+1)]

    for problem in range(FILE_START, FILE_START + NUM_FILES):
        fileMiddlePart = "{0:0>2}".format(problem)
        fileName = FILE_PREFIX + fileMiddlePart + FILE_SUFFIX

        clauses = loadClauses(fileName)

        for trial in range(NUM_TRIALS):
            print 'Solving:', fileName, 'Trial:', trial+1, '/', NUM_TRIALS, '(SA most)'
            initial_SA_Solution = generateRandomSolution(NUM_VARIABLES)

            startTime = time.clock()
            SA_matrix, SA_best = SA(initial_SA_Solution, clauses, T_INITIAL,
                    ALPHA, BETA, M_INITIAL, MAX_TIME, most_neighbor)
            elapsed = time.clock() - startTime
            all_SA_most_time[problem].append(elapsed)
            all_SA_most_bests[problem].append(SA_best)

            pickle.dump(SA_matrix, open('data/all-SA-most-Matrices_' +
                str(problem) + '_' + str(trial) + '_.p', 'wb'))


    # Dump results
    pickle.dump(all_SA_most_bests, open('data/all_SA_most_bests.p', 'wb'))
    pickle.dump(all_SA_most_time, open('data/all_SA_most_time.p', 'wb'))
    #Free memory
    del all_SA_most_bests[:]
    del all_SA_most_time[:]
    del all_SA_most_bests
    del all_SA_most_time

    # Initialize memory
    rand_sat_sols = [[] for i in range(NUM_FILES+1)]
    all_rand_time = [[] for i in range(NUM_FILES+1)]

    for problem in range(FILE_START, FILE_START + NUM_FILES):
        fileMiddlePart = "{0:0>2}".format(problem)
        fileName = FILE_PREFIX + fileMiddlePart + FILE_SUFFIX

        clauses = loadClauses(fileName)

        for trial in range(NUM_TRIALS):
            print 'Solving:', fileName, 'Trial:', trial+1, '/', NUM_TRIALS, '(Monte Carlo)'

            # Try random attempts for the same amount of trials as SA would
            # have. 
            randAllCosts = []
            startTime = time.clock()
            for randAttempt in range(RAND_TRIALS):
                initial_rand_Solution = generateRandomSolution(NUM_VARIABLES, 0.5)
                randBestCost = cost(initial_rand_Solution, clauses)

                # record SAT solutions
                if randBestCost == 0:
                    rand_sat_sols[trial+1].append(initial_rand_Solution)

                randAllCosts.append(randBestCost)
            elapsed = time.clock() - startTime
            all_rand_time[problem].append(elapsed)
            pickle.dump(randAllCosts, open('data/all-rand-sols_' +
                str(problem) + '_' + str(trial) + '_.p', 'wb'))

    # Dump results
    pickle.dump(rand_sat_sols, open('data/rand_sat_sols.p', 'wb'))
    pickle.dump(all_rand_time, open('data/all_rand_time.p', 'wb'))
