import bisect
import itertools
import math
import random


class GeneticAlgorithm:
    def __init__(self, p, fcross, ffitness, fmutate):
        self.population = None
        self.p = p
        self.fcross = fcross
        self.ffitness = ffitness
        self.fmutate = fmutate

    def _roulette_wheel_evolve(self):
        new_population = []
        new_population_set = set()
        fitness = self.ffitness(self.population)
        accum = list(itertools.accumulate(fitness))

        while len(new_population) != self.p:
            r = random.randint(0, math.ceil(accum[-1]))
            i = bisect.bisect_left(accum, r)
            if i not in new_population_set:
                new_population_set.add(i)
                new_population.append(self.population[i])

        self.population = list(new_population)

    def _best_evolve(self):
        fitness = self.ffitness(self.population)
        population = [(self.population[i], fitness[i]) for i in range(len(fitness))]
        population.sort(key=lambda x: x[1], reverse=True)
        self.population = [x[0] for x in population[:self.p]]

    def solve(self, population, generations):
        self.population = population
        m = 1 / len(population[0])  # probability of occurrence of mutations

        for _ in range(generations):
            crossing_order = list(self.population)
            random.shuffle(crossing_order)

            while crossing_order:
                c1 = crossing_order.pop(0)
                c2 = crossing_order.pop()
                children = self.fcross(c1, c2, 0.6)
                self.population.extend(map(lambda c: self.fmutate(c, m), children))

            m += random.random() / 10
            self._best_evolve()

        fitness = self.ffitness(self.population)
        pos = max(range(self.p), key=lambda i: fitness[i])
        return self.population[pos]
