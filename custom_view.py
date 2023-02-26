import random

import discord
from discord.ui import Button, View


class PokemonMove(Button):
    def __init__(self, move, pp, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = kwargs.get('label', '')
        self.move = move
        self.max_pp = pp
        self.current_pp = pp
        self.update_label()

    def disable_move(self):
        self._underlying.disabled = True

    def update_label(self):
        if self.current_pp <= 0:
            self.current_pp = 0
            self.disable_move()
        curr_pp = f' [ {self.current_pp}/{self.max_pp} ]' \
            if self.name not in ('Run Away', 'Struggle') else ''
        self._underlying.label = f'{self.name}' + curr_pp

class CustomView(View):
    def __init__(self, pokemon1, pokemon2, learnsets, moves, *, timeout=180):
        super().__init__(timeout=timeout)
        self.my_hp = None
        self.opponent_hp = None
        self.my_pokemon = pokemon1
        self.move1 = None
        self.move2 = None
        self.move3 = None
        self.move4 = None
        self.struggle = None
        self.run_away = None
        self.create_health_bar(pokemon1, pokemon2)
        self.create_move_buttons()
        self.add_view_buttons()

    def lock_moves(self):
        self.move1.disable_move()
        self.move2.disable_move()
        self.move3.disable_move()
        self.move4.disable_move()
        self.run_away.disable_move()
        if self.struggle:
            self.struggle.disable_move()

    def check_power_points(self):
        if (
            self.move1.current_pp == 0 and 
            self.move2.current_pp == 0 and 
            self.move3.current_pp == 0 and
            self.move4.current_pp == 0
        ):
            self.struggle = PokemonMove(
                label='Struggle',
                emoji='👊🏽',
                row=1,
                pp=float('inf'),
                move='struggle'
            )
            self.add_item(self.struggle)
        
    def create_health_bar(self, pokemon1, pokemon2):
        self.my_hp = Button(
            label=f"{pokemon1.name}'s HP: [{pokemon1.current_hp}/{pokemon1.max_hp}] " 
                  f"[{pokemon1.current_hp // pokemon1.max_hp * 100}%]", 
            style=discord.ButtonStyle.green, emoji='🦄',
            disabled=True,
            row=0
        )
        self.opponent_hp = Button(
            label=f"{pokemon2.name}'s HP: [{pokemon2.current_hp}/{pokemon2.max_hp}] " 
                  f"[{pokemon2.current_hp // pokemon2.max_hp * 100}%]", 
            style=discord.ButtonStyle.green, emoji='🦄',
            disabled=True,
            row=0
        )

    def create_move_buttons(self):
        self.move1 = PokemonMove(
            label=self.my_pokemon.move1[0],
            emoji='➡️',
            row=1,
            pp=self.my_pokemon.move1[1],
            move=self.my_pokemon.move1[2]
        )
        self.move2 = PokemonMove(
            label=self.my_pokemon.move2[0],
            emoji='➡️',
            row=2,
            pp=self.my_pokemon.move2[1],
            move=self.my_pokemon.move2[2]
        )
        self.move3 = PokemonMove(
            label=self.my_pokemon.move3[0],
            emoji='➡️',
            row=3,
            pp=self.my_pokemon.move3[1],
            move=self.my_pokemon.move3[2]
        )
        self.move4 = PokemonMove(
            label=self.my_pokemon.move4[0],
            emoji='➡️',
            row=4,
            pp=self.my_pokemon.move4[1],
            move=self.my_pokemon.move4[2]
        )
        self.run_away = PokemonMove(
            label='Run Away',
            emoji='🚶🏽',
            row=0,
            pp=1,
            move='runaway'
        )
        
    def add_view_buttons(self):
        self.add_item(self.my_hp)
        self.add_item(self.opponent_hp)
        self.add_item(self.move1)
        self.add_item(self.move2)
        self.add_item(self.move3)
        self.add_item(self.move4)
        self.add_item(self.run_away)