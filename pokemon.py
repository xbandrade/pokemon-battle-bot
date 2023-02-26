import random

from utils.sprite_manager import get_pokemon_sprite


class Pokemon:
    def __init__(self, slug, data, learnset, moves):
        self.slug = slug
        self.pokedex_number = data['num']
        self.name = data['name']
        self.types = data['types']
        self.level = 100
        self.learnset = learnset
        self.base_hp = data['baseStats']['hp']
        self.base_atk = data['baseStats']['atk']
        self.base_def = data['baseStats']['def']
        self.base_spa = data['baseStats']['spa']
        self.base_spd = data['baseStats']['spd']
        self.base_spe = data['baseStats']['spe']
        self.ivs = [31, 31, 31, 31, 31, 31]
        self.evs = [85, 85, 85, 85, 85, 85]
        self.nature = [1, 1, 1, 1, 1, 1]  # Assume neutral nature
        self.abilities = random.choice(list(data['abilities'].keys()))
        self.max_hp = self.calculate_max_hp()
        self.current_hp = self.calculate_max_hp()
        self.atk = ...
        self.def_ = ...
        self.spa = ...
        self.spd = ...
        self.spd = ...
        self.front_sprite = get_pokemon_sprite(self.pokedex_number, True)
        self.back_sprite = get_pokemon_sprite(self.pokedex_number, False)
        self.move1, self.move2, self.move3, self.move4 = self.create_moveset(moves)

    def create_moveset(self, moves):
        moveset = random.choices(list(self.learnset.keys()), k=4)
        return [
            [moves[moveset[i]]['name'], moves[moveset[i]]['pp'], moveset[i]] for i in range(4)
        ]

    def calculate_max_hp(self):
        hp = (((2 * self.base_hp + self.ivs[0] + (self.evs[0] // 4)) * self.level) // 100 + self.level + 10)
        return hp if self.slug != 'shedinja' else 1

    def calculate_stats(self):
        for i, base in (self.base_atk, self.base_def, self.base_spa, self.base_spd, self.base_spe):
            stat = (((((2 * base + self.ivs[i] + (self.evs[i] // 4)) * self.level) // 100) + 5) * self.nature[i])
    