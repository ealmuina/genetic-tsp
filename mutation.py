import random


def _two_opt_swap(c, i, j):
    new_c = c[:]
    fragment = c[i:j]
    fragment.reverse()
    new_c[i:j] = fragment
    return new_c


def swap(c, p):
    if random.random() > p:
        return c
    i = random.randrange(len(c))
    j = random.randrange(len(c))
    c[i], c[j] = c[j], c[i]
    return c


def two_opt(route, costs, p):
    if random.random() > p:
        return route
    l = len(route)
    for i in range(l):
        for j in range(i + 2, l):
            new_route = _two_opt_swap(route, i, j)
            a, b = route[(i - 1) % l], route[i]
            c, d = route[j - 1], route[j]
            if costs[a][b] + costs[c][d] > costs[a][c] + costs[b][d]:
                route = new_route
    return route
