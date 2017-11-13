"""
City j occupies position i in the chromosome if there is an edge from city i to city j in the tour.
Example: Chromosome 38526417 encodes the tour 13564287.
"""

import random

import datasets
import ga
import tsp


def decode(e):
    result = []
    current = 1
    while len(result) != len(e):
        result.append(current)
        current = e[current]
    return result


def encode(c):
    l = len(c)
    result = [0] * l
    for i in range(l):
        result[c[(i - 1) % l]] = c[i]
    return result


def er(c1, c2, p):
    if random.random() > p:
        return c1, c2

    def offspring(e1, e2):
        l = len(e1)
        edges = {i: set() for i in range(l)}
        for i in range(l):
            edges[e1[i]].add(e1[(i - 1) % l])
            edges[e1[i]].add(e1[(i + 1) % l])
            edges[e2[i]].add(e2[(i - 1) % l])
            edges[e2[i]].add(e2[(i + 1) % l])
        junior = []
        selected = set()
        current = 1
        while True:
            junior.append(current)
            selected.add(current)
            cities = edges.pop(current)
            for e in edges:
                if current in edges[e]:
                    edges[e].remove(current)
            if len(junior) == l:
                break
            if not cities:
                cities = {random.choice(list(edges.keys()))}
            current = min(cities, key=lambda x: len(edges[x]))
        return junior

    e1 = encode(c1)
    e2 = encode(c2)
    return [encode(offspring(e1, e2)), encode(offspring(e2, e1))]
