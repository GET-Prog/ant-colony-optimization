import json
import pprint
import random

matrix = [
    [0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

ANTS = 20
START_ROW = 0
FINISH_ROW = 8
INTERATIONS = 4
EVAPORATION_COEF = 0.1
INITIAL_PHEROMONE = 0.1


def create_path(pheromones):
    index = START_ROW
    path = [index]

    while 1 in matrix[index]:
        ppa = [i for i, v in enumerate(matrix[index]) if v == 1]
        d = sum([pheromones[index][i] for i in ppa])
        ppa_prob = [pheromones[index][i] / d for i in ppa]
        index = random.choices(ppa, ppa_prob, k=1)[0]
        path.append(index)

    return path


def update_pheromone(pheromones, paths):
    l = len(pheromones)
    for i in range(l):
        for j in range(l):
            if matrix[i][j] == 1:
                pheromones[i][j] = pheromones[i][j] * (1 - EVAPORATION_COEF)

    for path in paths:
        if path[-1] == FINISH_ROW:
            for index in range(len(path) - 1):
                pheromones[path[index]][path[index + 1]] += 1 / len(path)


def path_count(paths):
    s = [json.dumps(p) for p in paths]
    return sorted(
        [(s.count(p), json.loads(p)) for p in set(s)], key=lambda p: p[0], reverse=True
    )


def display_result(pheromones, paths):
    print(f"\nResult in Interaction {INTERATIONS}:")
    for x, path in path_count(paths):
        print(f"{x} Ant: {path}")
    print("\nPheromone Matrix:")
    pprint.pprint(pheromones)


if __name__ == "__main__":
    pheromones = [[INITIAL_PHEROMONE if v == 1 else 0 for v in r] for r in matrix]

    for _ in range(INTERATIONS):
        paths = [create_path(pheromones) for _ in range(ANTS)]
        update_pheromone(pheromones, paths)

    display_result(pheromones, paths)
