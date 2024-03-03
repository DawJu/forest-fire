import numpy as np
import matplotlib.pyplot as plt
from random import random, randint


def show_forest(array, title):
    plt.matshow(array)
    plt.title(title)
    plt.savefig('graphs/' + title + '.png')
    plt.show()


# Define the color for each state
states = {0: np.array([102, 51, 0]),        # 0 (brown) - burnt tree
          1: np.array([255, 0, 0]),         # 1 (red)   - burning tree
          2: np.array([0, 255, 0]),         # 2 (green) - tree
          3: np.array([135, 135, 135])}     # 3 (gray)  - rock

# Initiate the forest array
forest = np.zeros((24, 24))
for i in range(forest.shape[0]):
    for j in range(forest.shape[1]):
        # Border of the forest is made of rocks
        if (i == 0) or (i == forest.shape[0] - 1) or (j == 0) or (j == forest.shape[1] - 1):
            forest[i, j] = 3
        else:
            # Each field has a 20% chance of being a rock, otherwise it is a tree
            r = random()
            if r < 0.2:
                forest[i, j] = 3
            else:
                forest[i, j] = 2

# Assign the correct color to each field
forest_colors = np.ndarray((forest.shape[0], forest.shape[1], 3), dtype=int)
for i in range(forest.shape[0]):
    for j in range(forest.shape[1]):
        forest_colors[i, j] = states[forest[i, j]]

show_forest(forest_colors, 'Initial state')

# Initiate a forest fire
while True:
    fire_start_x = randint(0, forest.shape[0] - 1)
    fire_start_y = randint(0, forest.shape[1] - 1)
    if np.array_equal(forest_colors[fire_start_x, fire_start_y], states[2]):
        forest_colors[fire_start_x, fire_start_y] = states[1]
        break

show_forest(forest_colors, 'Generation 0')

# !!! Using Moore neighborhood !!!

p = 0.7  # probability of a tree getting ignited when it is adjacent to a burning tree
max_iterations = 28  # max number of iterations
iteration = 1
# The evolution loop
fnext = forest_colors
while max_iterations >= iteration:
    fnow = fnext.copy()
    fnext = np.ndarray((fnow.shape[0], fnow.shape[1], 3), dtype=int)
    for i in range(fnow.shape[0]):
        for j in range(fnow.shape[1]):
            # If the field is a rock - it stays a rock
            if np.array_equal(fnow[i, j], states[3]):
                fnext[i, j] = states[3]
            # If the field is a burnt tree - it stays a burnt tree
            elif np.array_equal(fnow[i, j], states[0]):
                fnext[i, j] = states[0]
            # If the field is a burning tree - it becomes a burnt tree
            elif np.array_equal(fnow[i, j], states[1]):
                fnext[i, j] = states[0]
            # If the field is a tree
            else:
                #  If it is adjacent to a burning tree
                if (np.array_equal(fnow[i - 1, j - 1], states[1]))\
                        or (np.array_equal(fnow[i - 1, j], states[1]))\
                        or (np.array_equal(fnow[i - 1, j + 1], states[1]))\
                        or (np.array_equal(fnow[i, j - 1], states[1]))\
                        or (np.array_equal(fnow[i, j + 1], states[1]))\
                        or (np.array_equal(fnow[i + 1, j - 1], states[1]))\
                        or (np.array_equal(fnow[i + 1, j], states[1]))\
                        or (np.array_equal(fnow[i + 1, j + 1], states[1])):
                    r = random()
                    # It becomes a burnt tree with the probability p
                    if r <= p:
                        fnext[i, j] = states[1]
                    # It stays a tree with the probability 1 - p
                    else:
                        fnext[i, j] = states[2]
                # Otherwise it stays a tree
                else:
                    fnext[i, j] = states[2]

    # Stop the program when the new generation is the same as the previous one
    if np.array_equal(fnow, fnext):
        break

    show_forest(fnext.astype(np.uint8), f'Generation {iteration}')

    iteration += 1
