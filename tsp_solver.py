import argparse
from math import sqrt
import time

from adjacency import er
import ga
import mutation
from path import pmx, mx, ox
import tsp


def _distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def _load(problem, optimum_path):
    positions = {}
    cities = 0

    with open(problem) as file:
        lines = file.readlines()
        for line in lines:
            line = line.split()
            if not line[0].isnumeric():
                continue
            positions[int(line[0]) - 1] = (float(line[1]), float(line[2]))
            cities += 1

    costs = []
    for i in range(cities):
        costs.append([0] * cities)

    for i in range(cities):
        for j in range(i + 1, cities):
            costs[i][j] = costs[j][i] = _distance(positions[i], positions[j])

    optimum = None
    if optimum_path:
        optimum = []
        with open(optimum_path) as file:
            lines = file.readlines()
            for line in lines:
                line = line.split()[0]
                if line.isnumeric():
                    city = int(line)
                    if city == -1:
                        break
                    optimum.append(city - 1)

    return costs, optimum


def _print_table(table):
    """
    Print a list of tuples as a pretty tabulated table.
    :param table: List of tuples, each one will be a row of the printed table
    """

    col_width = [max(len(x) for x in col) for col in zip(*table)]
    for line in table:
        print((" " * 3).join("{:{}}".format(x, col_width[i]) for i, x in enumerate(line)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('method')
    parser.add_argument('problem_path')
    parser.add_argument('--optimum_path')
    parser.add_argument('--population', type=int, default=100)
    parser.add_argument('--generations', type=int, default=100)
    parser.add_argument('--tests', type=int, default=30)
    args = parser.parse_args()

    method = {'pmx': pmx, 'mx': mx, 'ox': ox, 'er': er}[args.method.lower()]
    solutions_sum = 0.0
    costs, optimum = _load(args.problem_path, args.optimum_path)
    optimum_times = 0

    if optimum:
        optimum_cost = tsp.evaluate(optimum, costs)

    output = [('SOLUTION', 'OPTIMUM', 'TIME')]
    for i in range(args.tests):
        solver = ga.GeneticAlgorithm(
            args.population,
            method,
            lambda pop: tsp.fitness(pop, costs),
            lambda c, p: mutation.two_opt(c, costs, p)
        )
        start = time.time()
        solution = solver.solve(tsp.random_population(args.population, len(costs)), args.generations)
        solution_cost = tsp.evaluate(solution, costs)
        solutions_sum += solution_cost

        if optimum and abs(solution_cost - optimum_cost) < 1e-3:
            optimum_times += 1

        output.append((
            '%.2f' % solution_cost,
            ('%.2f' % optimum_cost) if optimum else 'UNKNOWN',
            '%.2f' % ((time.time() - start) / 60)
        ))
        print('done test %d/%d' % (i + 1, args.tests))
    print('-------------')
    _print_table(output)
    print('-------------')
    print('Average: %.2f' % (solutions_sum / args.tests))
    if optimum:
        print('Optimum found %d/%d times' % (optimum_times, args.tests))


if __name__ == '__main__':
    main()
