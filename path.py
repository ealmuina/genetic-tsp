import random
import time

import datasets
import ga
import mutation
import tsp


def pmx(c1, c2, p):
    if random.random() > p:
        return c1, c2

    def offspring(c1, c2):
        i = random.randrange(0, len(c1))
        j = random.randint(i + 1, len(c1))
        junior = c2[:i] + c1[i:j] + c2[j:]

        lost = [x for x in c2[i:j] if x not in set(c1[i:j])]
        extras = set(c1[i:j]) & set(c2[:i] + c2[j:])

        for p in range(len(junior)):
            if (p < i or p >= j) and junior[p] in extras:
                junior[p] = lost.pop()
        return junior

    return [offspring(c1, c2), offspring(c2, c1)]


def mx(c1, c2, p):
    if random.random() > p:
        return c1, c2

    def offspring(c1, c2):
        i = random.randint(0, len(c1))
        junior = c1[i:]
        contained = set(junior)
        for x in c2:
            if x not in contained:
                junior.append(x)
        return junior

    return [offspring(c1, c2), offspring(c2, c1)]


def ox(c1, c2, p):
    if random.random() > p:
        return c1, c2

    def offspring(c1, c2):
        i = random.randrange(0, len(c1))
        j = random.randint(i + 1, len(c1))
        junior = [0] * i + c1[i:j] + [0] * (len(c1) - j)
        contained = set(c1[i:j])
        c2 = c2[j:] + c2[:j]
        pos = j
        for x in c2:
            if x not in contained:
                pos %= len(c1)
                junior[pos] = x
                pos += 1
        return junior

    return [offspring(c1, c2), offspring(c2, c1)]


if __name__ == '__main__':
    costs, optimum = datasets.load('datasets/pr76.tsp.txt', 'datasets/pr76.opt.tour.txt')

    solver_pmx = ga.GeneticAlgorithm(100, ox, lambda pop: tsp.fitness(pop, costs),
                                     lambda c, p: mutation.two_opt(c, costs, p))

    start = time.time()
    solution = solver_pmx.solve(tsp.random_population(100, len(costs)), 100)

    print('SOLUTION\tOPTIMUM\t\tTIME')
    print('%.2f' % tsp.evaluate(solution, costs), '%.2f' % tsp.evaluate(optimum, costs),
          '%.2f' % ((time.time() - start) / 60), sep='\t')
    print(solution)
