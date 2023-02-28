import random

import discord
from discord.ui import Button, View

from bot_play import bot_moves
from utils.damage_calc import calc


class PokemonMoveButton(Button):
    def __init__(self, move, pp, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = kwargs.get('label', '')
        self.move = move
        self.max_pp = pp
        self.current_pp = pp
        self.id = self._row - 1
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
    

class HealthBar(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_style(self):
        self._underlying.style = discord.ButtonStyle.danger

    def update_hp(self, pokemon):
        percentage = round(pokemon.current_hp / pokemon.max_hp * 100, 1)
        if percentage <= 25:
            self.update_style()
        self._underlying.label = (
            f"Lv. {pokemon.level} {pokemon.name}'s HP: {pokemon.current_hp}/{pokemon.max_hp} "
            f"[{percentage}%]"
        )


class CustomView(View):
    def __init__(self, pokemon1, pokemon2, *, mode='random', timeout=180):
        super().__init__(timeout=timeout)
        self.my_hp = None
        self.opponent_hp = None
        self.my_pokemon = pokemon1
        self.opponent = pokemon2
        self.move1 = None
        self.move2 = None
        self.move3 = None
        self.move4 = None
        self.mode = mode
        self.struggle = None
        self.run_away = None
        self.create_health_bar(pokemon1, pokemon2)
        self.create_move_buttons()
        self.add_view_buttons()

    def calculate_damage(self, pokemon1, pokemon2, move):
        messages = []
        if pokemon1.spe >= pokemon2.spe:
            messages += [f'{pokemon1} used {move}!']
            damage, msg = calc(pokemon1, pokemon2, move)
            messages += msg
            pokemon2.current_hp -= damage
            messages += self.update_health_bar(pokemon1, pokemon2)
            if pokemon2.current_hp > 0:
                opponent_move = bot_moves(pokemon1, pokemon2, mode=self.mode)
                messages += [f'{pokemon2} used {opponent_move}!']
                damage, msg = calc(pokemon2, pokemon1, opponent_move)
                messages += msg
                pokemon1.current_hp -= damage
                messages += self.update_health_bar(pokemon1, pokemon2)
        else:
            opponent_move = bot_moves(pokemon1, pokemon2, mode=self.mode)
            messages += [f'{pokemon2} used {opponent_move}!']
            damage, msg = calc(pokemon2, pokemon1, opponent_move)
            messages += msg
            pokemon1.current_hp -= damage
            messages += self.update_health_bar(pokemon1, pokemon2)
            if pokemon1.current_hp > 0:
                messages += [f'{pokemon1} used {move}!']
                damage, msg = calc(pokemon1, pokemon2, move)
                messages += msg
                pokemon2.current_hp -= damage
                messages += self.update_health_bar(pokemon1, pokemon2)
        return messages
    
    def update_health_bar(self, pokemon1, pokemon2):
        if pokemon1.current_hp <= 0:
            self.lock_moves()
            pokemon1.current_hp = 0
            self.my_hp.update_hp(pokemon1)
            return [f"{pokemon1} fainted!", f"You've been defeated by {pokemon2}!"]
        if pokemon2.current_hp <= 0:
            self.lock_moves()
            pokemon2.current_hp = 0
            self.opponent_hp.update_hp(pokemon2)
            return [f'{pokemon2} fainted!', 'Victory!']
        self.my_hp.update_hp(pokemon1)
        self.opponent_hp.update_hp(pokemon2)
        return []

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
            self.struggle = PokemonMoveButton(
                label='Struggle',
                emoji='👊🏽',
                row=1,
                pp=float('inf'),
                move='struggle',
                view=self,
                pokemon1=self.my_pokemon,
                pokemon2=self.opponent,
            )
            self.add_item(self.struggle)
        
    def create_health_bar(self, pokemon1, pokemon2):
        self.my_hp = HealthBar(
            label=f"Lv. {pokemon2.level} {pokemon1.name}'s HP: {pokemon1.current_hp}/{pokemon1.max_hp} " 
                  f"[{pokemon1.current_hp // pokemon1.max_hp * 100}%]", 
            style=discord.ButtonStyle.green,
            disabled=True,
            row=0
        )
        self.opponent_hp = HealthBar(
            label=f"Lv. {pokemon2.level} {pokemon2.name}'s HP: {pokemon2.current_hp}/{pokemon2.max_hp} " 
                  f"[{pokemon2.current_hp // pokemon2.max_hp * 100}%]", 
            style=discord.ButtonStyle.green,
            disabled=True,
            row=0
        )

    def create_move_buttons(self):
        self.move1 = PokemonMoveButton(
            label=self.my_pokemon.move1.name,
            emoji='➡️',
            row=1,
            pp=self.my_pokemon.move1.max_pp,
            move=self.my_pokemon.move1.slug,
        )
        self.move2 = PokemonMoveButton(
            label=self.my_pokemon.move2.name,
            emoji='➡️',
            row=2,
            pp=self.my_pokemon.move2.max_pp,
            move=self.my_pokemon.move2.slug,
        )
        self.move3 = PokemonMoveButton(
            label=self.my_pokemon.move3.name,
            emoji='➡️',
            row=3,
            pp=self.my_pokemon.move3.max_pp,
            move=self.my_pokemon.move3.slug,
        )
        self.move4 = PokemonMoveButton(
            label=self.my_pokemon.move4.name,
            emoji='➡️',
            row=4,
            pp=self.my_pokemon.move4.max_pp,
            move=self.my_pokemon.move4.slug,
        )
        self.run_away = PokemonMoveButton(
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
