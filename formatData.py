from constants import *

import pickle
import pylab

OUT_PREFIX = 'clean_data/'

def formatName(name, problem):
    return OUT_PREFIX + name + '_' + str(problem) + '_.p'

if __name__ == '__main__':

    print 'Loading unused data.'

    # The actual solutions
    all_SA_rand_bests = pickle.load(open('data/all_SA_rand_bests.p', 'rb'))
    all_SA_most_bests = pickle.load(open('data/all_SA_most_bests.p', 'rb'))
    rand_sat_sols = pickle.load(open('data/rand_sat_sols.p', 'rb'))

    # Time data
    all_SA_rand_time = pickle.load(open('data/all_SA_rand_time.p', 'rb'))
    all_SA_most_time = pickle.load(open('data/all_SA_most_time.p', 'rb'))
    all_rand_time = pickle.load(open('data/all_rand_time.p', 'rb'))


   # Add 1 because the file names are 1-based
    allNames = [""]
    for problem in range(FILE_START, FILE_START + NUM_FILES):
        fileMiddlePart = "{0:0>2}".format(problem)
        fileName = FILE_PREFIX + fileMiddlePart + FILE_SUFFIX
        allNames.append(fileName)

    # Load all partial data
    for problem in range(FILE_START, FILE_START + NUM_FILES):
        print 'Calculating data for problem', problem

        all_SA_rand_Matrices = []
        all_SA_most_Matrices = []
        all_rand_sols = []

        for trial in range(NUM_TRIALS):
            print '\tLoading trial', trial+1

            all_SA_rand_Matrices.append(pickle.load(open('data/all-SA-rand-Matrices_' +
                str(problem) + '_' + str(trial) + '_.p', 'rb')))

            all_SA_most_Matrices.append(pickle.load(open('data/all-SA-most-Matrices_' +
                str(problem) + '_' + str(trial) + '_.p', 'rb')))

            all_rand_sols.append(pickle.load(open('data/all-rand-sols_' +
                str(problem) + '_' + str(trial) + '_.p', 'rb')))


        """
        See if any problems were satisfied.
        """
        satisfiable = False
        for matrix in all_SA_rand_Matrices:
            for row in matrix:
                if row[SA_BEST_COST_INDEX] == 0:
                    satisfiable = True
        #
        if satisfiable:
            print allNames[problem], 'was satisfiable by SA (rand).'
        else:
            print allNames[problem], 'was not satisfiable by SA (rand).'

        satisfiable = False
        for matrix in all_SA_most_Matrices:
            for row in matrix:
                if row[SA_BEST_COST_INDEX] == 0:
                    satisfiable = True
        #
        if satisfiable:
            print allNames[problem], 'was satisfiable by SA (most).'
        else:
            print allNames[problem], 'was not satisfiable by SA (most).'

        satisfiable = False
        for randAttempt in all_rand_sols:
            if randAttempt == 0:
                satisfiable = True
        #
        if satisfiable:
            print allNames[problem], 'was satisfiable by rand.'
        else:
            print allNames[problem], 'was not satisfiable by rand.'

        pylab.title('Avg Best Cost (Clauses Incorrect) For Problem ' + allNames[problem])
        pylab.xlabel('Iteration')
        pylab.ylabel('Avg Best Cost')


        SA_iterations = [i for i in range(MAX_TIME + 1)]
        rand_iterations = [i for i in range(MAX_TIME + 1)]

        # Empirical CDF data
        cdf_SA_rand = []
        cdf_SA_most = []
        cdf_rand = []

        # Time to best solution
        ttb_SA_rand = []
        ttb_SA_most = []
        ttb_rand = []

        # SA
        avg_SA_rand_cost = [0.0 for i in range(MAX_TIME + 1)]
        for matrix in all_SA_rand_Matrices:
            # TTB vars
            curBest = NUM_CLAUSES + 1
            ttb = NUM_FUNC_EVALS

            cdf_SA_rand.append(matrix[-1][SA_BEST_COST_INDEX])
            avg_SA_rand_cost[0] += NUM_CLAUSES
            for row in matrix:
                # Avg cost per iteration
                avg_SA_rand_cost[row[SA_ITERATION_INDEX]] += row[SA_BEST_COST_INDEX]
                # Time to best solution
                if int(row[1]) < curBest:
                    curBest = int(row[1])
                    ttb = int(row[0])
            ttb_SA_rand.append(ttb)
        avg_SA_rand_cost = [avg / NUM_TRIALS for avg in avg_SA_rand_cost]

        avg_SA_most_cost = [0.0 for i in range(MAX_TIME + 1)]
        for matrix in all_SA_most_Matrices:
            # TTB vars
            curBest = NUM_CLAUSES + 1
            ttb = NUM_FUNC_EVALS

            cdf_SA_most.append(matrix[-1][SA_BEST_COST_INDEX])
            avg_SA_most_cost[0] += NUM_CLAUSES
            for row in matrix:
                # Avg cost per iteration
                avg_SA_most_cost[row[SA_ITERATION_INDEX]] += row[SA_BEST_COST_INDEX]
                # Time to best solution
                if int(row[1]) < curBest:
                    curBest = int(row[1])
                    ttb = int(row[0])

            ttb_SA_most.append(ttb)
        avg_SA_most_cost = [avg / NUM_TRIALS for avg in avg_SA_most_cost]

        # rand      
        avg_rand_cost = [0.0 for i in range(MAX_TIME + 1)]
        for matrix in all_rand_sols:
            # TTB vars
            ttb = RAND_TRIALS
            avg_rand_cost[0] += NUM_CLAUSES
            rand_best_trial = NUM_CLAUSES

            for i in range(0, RAND_TRIALS):
                avg_rand_cost[i] += matrix[i]

                if rand_best_trial > matrix[i]:
                    rand_best_trial = matrix[i]
                    ttb = i+1

            cdf_rand.append(rand_best_trial)
            ttb_rand.append(ttb)
        avg_rand_cost = [avg / NUM_TRIALS for avg in avg_rand_cost]


        """
        Serialize data
        """
        # Avg costs
        pickle.dump(avg_SA_rand_cost, open(formatName('avg_cost_SA_rand', problem), 'wb'))
        pickle.dump(avg_SA_most_cost, open(formatName('avg_cost_SA_most', problem), 'wb'))
        pickle.dump(avg_rand_cost, open(formatName('avg_cost_rand', problem), 'wb'))

        # Empirical CDFs
        pickle.dump(cdf_SA_rand, open(formatName('cdf_SA_rand', problem), 'wb'))
        pickle.dump(cdf_SA_most, open(formatName('cdf_SA_most', problem), 'wb'))
        pickle.dump(cdf_rand, open(formatName('cdf_rand', problem), 'wb'))

        # Time to best
        pickle.dump(ttb_SA_rand, open(formatName('ttb_SA_rand', problem), 'wb'))
        pickle.dump(ttb_SA_most, open(formatName('ttb_SA_most', problem), 'wb'))
        pickle.dump(ttb_rand, open(formatName('ttb_rand', problem), 'wb'))


