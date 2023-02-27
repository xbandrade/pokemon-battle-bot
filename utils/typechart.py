import numpy as np

type_code = {
    'Dragon': 0,
    'Ghost': 1,
    'Ground': 2,
    'Flying': 3,
    'Poison': 4,
    'Bug': 5,
    'Water': 6,
    'Electric': 7,
    'Rock': 8,
    'Grass': 9,
    'Dark': 10,
    'Ice': 11,
    'Normal': 12,
    'Fire': 13,
    'Fighting': 14,
    'Steel': 15,
    'Psychic': 16,
    'Fairy': 17,
}

# row -> attacker, column -> defender

type_chart = np.array([
    [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, .5, 1, 0],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, .5, 1, 0, 1, 1, 1, 2, 1],
    [1, 1, 1, 0, 2, .5, 1, 2, 2, .5, 1, 1, 1, 2, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 2, 1, .5, .5, 2, 1, 1, 1, 1, 2, .5, 1, 1],
    [1, .5, .5, 1, .5, 1, 1, 1, .5, 2, 1, 1, 1, 1, 1, 0, 1, 2],
    [1, .5, 1, .5, .5, 1, 1, 1, 1, 2, 2, 1, 1, .5, .5, .5, 2, .5],
    [.5, 1, 2, 1, 1, 1, .5, 1, 2, .5, 1, 1, 1, 2, 1, 1, 1, 1],
    [.5, 1, 0, 2, 1, 1, 2, .5, 1, .5, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, .5, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, .5, .5, 1, 1],
    [.5, 1, 2, .5, .5, .5, 2, 1, 2, .5, 1, 1, 1, .5, 1, .5, 1, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, .5, 1, 1, 1, .5, 1, 2, .5],
    [2, 1, 2, 2, 1, 1, .5, 1, 1, 2, 1, .5, 1, .5, 1, .5, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, .5, 1, 1, 1, 1, 1, 1, .5, 1, 1],
    [.5, 1, 1, 1, 1, 2, .5, 1, .5, 2, 1, 2, 1, .5, 1, 2, 1, 1],
    [1, 0, 1, .5, .5, .5, 1, 1, 2, 1, 2, 2, 2, 1, 1, 2, .5, .5],
    [1, 1, 1, 1, 1, 1, .5, .5, 2, 1, 1, 2, 1, .5, 1, .5, 1, 2],
    [1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 1, 2, .5, .5, 1],
    [2, 1, 1, 1, .5, 1, 1, 1, 1, 1, 2, 1, 1, .5, 2, .5, 1, 1],
])