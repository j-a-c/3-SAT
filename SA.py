from cost import cost
from math import exp
from random import random

"""
    Simulating annealing implementation.

    Returns a tuple of a matrix with one row per iteration with the values:
        (iteration number, current cost, best cost)
    and the best solution.
"""
def SA(sInitial, clauses, tInitial, alpha, beta, mInitial, maxTime, neighbor):
    # Set initial parameters
    temperature = tInitial
    currentSolution = sInitial
    bestSolution = currentSolution
    currentCost = cost(currentSolution, clauses)
    bestCost = currentCost
    time = 0
    M = 1.0 * mInitial
    solutionMatrix = []
    iteration = 1

    while time < maxTime:

        # Metropolis function
        mCopy = M
        while mCopy > 0:
            newSolution = neighbor(currentSolution, clauses)
            newCost = cost(newSolution, clauses)
            deltaCost = newCost - currentCost

            if deltaCost < 0:
                currentSolution = newSolution
                currentCost = newCost
                if newCost < bestCost:
                    bestSolution = newSolution
                    bestCost = newCost
            else:
                if random() < exp(-deltaCost / temperature):
                    currentSolution = newSolution
                    currentCost = newCost

            # Update solution matrix and iteration
            solutionMatrix.append((iteration, currentCost, bestCost))
            iteration = iteration + 1

            mCopy = mCopy - 1

        # Update SA parameters
        time = time + M
        temperature = alpha * temperature
        M = beta * M
    return (solutionMatrix, bestSolution)
