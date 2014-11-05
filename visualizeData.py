import numpy
import pickle
import pylab

# Input file constants
FILE_PREFIX = 'uf200-'
FILE_SUFFIX = '.txt'
FILE_START = 1
NUM_FILES = 10

MAX_TIME = 100000

OUT_PREFIX = 'clean_data/'

def formatName(name, problem):
    return OUT_PREFIX + name + '_' + str(problem) + '_.p'

if __name__ == '__main__':

    # Generate file names for displaying in graphs.
    # Add 1 because the file names are 1-based.
    allNames = [""]
    for problem in range(FILE_START, FILE_START + NUM_FILES):
        fileMiddlePart = "{0:0>2}".format(problem)
        fileName = FILE_PREFIX + fileMiddlePart + FILE_SUFFIX
        allNames.append(fileName)


    """
    Visualize each problem separately.
    """
    for problem in range(FILE_START, FILE_START + NUM_FILES):
        print ' == Visualizing data for problem', problem, '=='

        """
        Load data for this problem.
        """
        # Avg costs
        avg_SA_rand_cost = pickle.load(open(formatName('avg_cost_SA_rand', problem), 'rb'))
        avg_SA_most_cost = pickle.load(open(formatName('avg_cost_SA_most', problem), 'rb'))
        avg_rand_cost = pickle.load(open(formatName('avg_cost_rand', problem), 'rb'))

        # Empirical CDFs
        cdf_SA_rand = pickle.load(open(formatName('cdf_SA_rand', problem), 'rb'))
        cdf_SA_most = pickle.load(open(formatName('cdf_SA_most', problem), 'rb'))
        cdf_rand  = pickle.load(open(formatName('cdf_rand', problem), 'rb'))

        # Time to best solution
        ttb_SA_rand = pickle.load(open(formatName('ttb_SA_rand', problem), 'rb'))
        ttb_SA_most = pickle.load(open(formatName('ttb_SA_most', problem), 'rb'))
        ttb_rand = pickle.load(open(formatName('ttb_rand', problem), 'rb'))

        """
        Plot data
        """
        # Plot avg cost per iteration
        # Iteration starts at 1 (index 0 is NUM_CLAUSES)
        iterations = [i for i in range(MAX_TIME + 1)]
        pylab.title('Avg Cost Per Iteration for (30 Trials, 100k Iterations): ' + allNames[problem])
        pylab.xlabel('Iteration')
        pylab.ylabel('Avg Cost')
        pylab.plot(iterations, avg_SA_rand_cost, label=allNames[problem] + 'SA (rand)')
        pylab.plot(iterations, avg_SA_most_cost, label=allNames[problem] + 'SA (most)')
        pylab.plot(iterations, avg_rand_cost, label=allNames[problem] + ' rand')
        pylab.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, borderaxespad=0.5)
        pylab.show()

        # Plot Empirical CDFs
        num_cdf= len(cdf_rand) + 1
        cdf_ys = [i/(1.0 * num_cdf) for i in range(1, num_cdf)]

        pylab.title('Empirical CDF for Best Solutions (Over 30 Trials): ' + allNames[problem])
        pylab.xlabel('Best Solution Cost')
        pylab.ylabel('CDF %')
        pylab.plot(sorted(cdf_SA_rand), cdf_ys, 'rx-', label='SA (rand)')
        pylab.plot(sorted(cdf_SA_most), cdf_ys, 'bx-', label='SA (most)')
        pylab.plot(sorted(cdf_rand), cdf_ys, 'go-', label='rand')
        pylab.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, borderaxespad=0.5)
        pylab.show()

        # Plot time to best solution
        num_ttb = len(ttb_SA_rand) + 1
        ttb_ys = [i/(1.0 * num_ttb) for i in range(1, num_ttb)]

        pylab.title('Empirical CDF for Time to Best Solution (Over 30 Trials): ' + allNames[problem])
        pylab.xlabel('Iteration for Best Solution For Trial')
        pylab.ylabel('CDF %')
        pylab.plot(sorted(ttb_SA_rand), ttb_ys, 'rx-', label='SA (rand)')
        pylab.plot(sorted(ttb_SA_most), ttb_ys, 'bx-', label='SA (most)')
        pylab.plot(sorted(ttb_rand), ttb_ys, 'go-', label='rand')
        pylab.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, borderaxespad=0.5)
        pylab.show()

        # Print stats about best solutions
        print 'Mean for Best Solutions:'
        print '\tSA_rand:', numpy.average(cdf_SA_rand)
        print '\tSA_most:', numpy.average(cdf_SA_most)
        print '\trand:', numpy.average(cdf_rand)

        print 'Std Dev for Best Solutions:'
        print '\tSA_rand:', numpy.std(cdf_SA_rand)
        print '\tSA_most:', numpy.std(cdf_SA_most)
        print '\trand:', numpy.std(cdf_rand)

        # Print Number of Solutions Found, Or Best Solution Otherwise
        print 'Number Of Best Solution Found:'
        print '\tSA_rand min:', min(cdf_SA_rand), 'Occurrences:', cdf_SA_rand.count(min(cdf_SA_rand))
        print '\tSA_most min:', min(cdf_SA_most), 'Occurrences:', cdf_SA_most.count(min(cdf_SA_most))
        print '\trand min:', min(cdf_rand), 'Occurrences:', cdf_rand.count(min(cdf_rand))

