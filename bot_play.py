import random

from utils.damage_calc import type_effectiveness


def check_moves(pokemon1, pokemon2, moves):
    scores = [0, 0, 0, 0]
    for i, move in enumerate(moves):
        if move.type in pokemon2.types:
            scores[i] += 1
        eff = type_effectiveness(pokemon1, move)
        if eff > 1:
            scores[i] += 5 + eff
        elif eff < 1:
            scores[i] -= 5 + eff
        if move.power > 0:
            scores[i] += 1
        ####### change this after implementing status moves
        if move.power == 0:
            scores[i] -= 10
    return scores   


def bot_moves(my_pokemon, bot_pokemon, mode='random'):
    msg = []
    moves = [
        bot_pokemon.move1, 
        bot_pokemon.move2, 
        bot_pokemon.move3, 
        bot_pokemon.move4,
    ]
    base_weights = [92, 5, 2, 1]
    available_moves = [move for move in moves if move.current_pp > 0]
    if not available_moves:
        return 'struggle'
    by_power = sorted(available_moves, key=lambda m: m.power, reverse=True)
    if mode == 'random':
        random_move = random.choice(moves)
        return random_move
        # random_move.current_pp -= 1  # add this later
    elif mode == 'smart':
        scores = check_moves(my_pokemon, bot_pokemon, moves)
        weights = base_weights[:len(scores)]
        for i, score in enumerate(scores):
            if score < 0:
                weights[i] = 0
        if set(weights) == {0}:
            return random.choices(available_moves, weights=base_weights[:len(available_moves)], k=1)[0]
        return random.choices(available_moves, weights=weights, k=1)[0]