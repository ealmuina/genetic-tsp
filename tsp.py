import random


def evaluate(c, costs):
    total = 0
    l = len(c)
    for i in range(l):
        total += costs[c[i]][c[(i + 1) % l]]
    return total


def fitness(population, costs):
    fit = list(map(lambda c: evaluate(c, costs), population))
    m = max(fit)
    return list(map(lambda x: m - x, fit))


def mutate(c, p):
    if random.random() > p:
        return c
    i = random.randrange(0, len(c))
    j = random.randrange(0, len(c))
    c[i], c[j] = c[j], c[i]
    return c


def random_population(individuals, dimension):
    result = []
    for i in range(individuals):
        x = list(range(dimension))
        random.shuffle(x)
        result.append(x)
    return result
