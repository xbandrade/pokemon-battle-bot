import random
from math import floor

from utils.typechart import type_chart, type_code


def move_critical(pokemon, move):
    stages = [(1 / 24), (1 / 8), (1 / 2), 1]
    crit_ratio = max(3, pokemon.crit_base + move.crit_ratio)
    r = random.uniform(0, 1)
    return 1.5 if r <= stages[crit_ratio] else 1


def calc_stab(pokemon, move):
    if move.type in pokemon.types:
        return 2 if pokemon.ability == 'adaptability' else 1.5
    return 1


def type_effectiveness(pokemon, move):
    attack = type_code[move.type]
    defense = [type_code[t] for t in pokemon.types]
    eff = 1
    for t in defense:
        eff *= type_chart[attack, t]
    return eff


def get_stats(pokemon1, pokemon2, move):
    category = move.category
    if category == 'Physical':
        return pokemon1.atk / pokemon2.def_
    elif category == 'Special':
        return pokemon1.spa / pokemon2.spd
    return 0


def calc(pokemon1, pokemon2, move):
    messages = []
    if move.power == 0 and move.category == 'Status':
        return (0, ['[-0 HP] [-0%]'])
    targets = 1
    parental_bond = 1
    weather = 1
    glaive_rush = 1
    critical = move_critical(pokemon1, move)
    stab = calc_stab(pokemon1, move)
    rand = random.uniform(0.85, 1)
    type = type_effectiveness(pokemon2, move)
    burn = 1
    other = 1
    ad = get_stats(pokemon1, pokemon2, move)
    damage = (((((2 * pokemon1.level) / 5 + 2) * move.power * ad) / 50) + 2)
    multipliers = targets * parental_bond * weather * glaive_rush * critical * rand * stab * type * burn * other
    final_damage = max(1, floor(damage * multipliers)) if move.category != 'Status' and type > 0 else 0
    percentage_damage = f'-{min(100, round(final_damage / pokemon2.max_hp * 100, 1))}%'
    if type >= 2:
        messages.append(f"It's super effective! [-{final_damage} HP] [{percentage_damage}]")
    elif 0 < type < 1:
        messages.append(f"It's not very effective! [-{final_damage} HP] [{percentage_damage}]")
    elif type == 0:
        messages.append(f"It has no effect on {pokemon2}! [-0 HP] [-0%]")
    else:
        messages.append(
            f"[-{final_damage} HP] [-{min(100, round(final_damage / pokemon2.max_hp * 100, 1))}%]"
        )
    return (final_damage, messages)