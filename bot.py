import os
import random

import discord
from dotenv import load_dotenv

from custom_view import CustomView
from pokemon import Pokemon
from utils.json_reader import load_learnsets, load_moves, load_pokedex
from utils.log import setup
from utils.sprite_manager import place_on_battlefield

load_dotenv()
logger = setup(__name__)

class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self)

    
async def send_message(interaction, prompt1, prompt2, pokedex, view):
    await interaction.response.defer()
    user = interaction.user
    channel = interaction.channel
    pokemon_name1 = prompt1.lower()
    pokemon_name2 = prompt2.lower()
    if pokemon_name1 in pokedex and pokemon_name2 in pokedex:
        try:
            pokedex_number1 = pokedex[pokemon_name1]['num']
            pokedex_number2 = pokedex[pokemon_name2]['num']
            img = place_on_battlefield(pokedex_number1, pokedex_number2)
            if not img:
                message = await interaction.followup.send(f'`Something went wrong!`')
                return
            file = discord.File(img)
            message = await interaction.followup.send(
                f'`{pokemon_name1.title()} x {pokemon_name2.title()}`',
                file=file, view=view
                )
            logger.info(f'{user} - {prompt1} - {prompt2} - Pokémon Found!')
        except Exception as e:
            print(e)
            img = place_on_battlefield(0, 0)
            file = discord.File(img)
            message = await interaction.followup.send(
                '`Sprite not found!`', file=file
            )
            logger.info(f'{user} - Sprite not Found!')
    else:
        logger.warning(f'{user} - {prompt1} - {prompt2} - Pokémon not found!')
        img = place_on_battlefield(0, 0)
        file = discord.File(img)
        message = await interaction.followup.send(
            f'`Pokémon not found!`', file=file
        )


def run():
    client = Client()
    pokedex = load_pokedex()
    learnsets = load_learnsets()
    moves = load_moves()

    @client.event
    async def on_ready():
        await client.tree.sync()
        logger.info(f'{client.user} is running!')

    async def view_callbacks(view, me, opponent):
        async def move1_callback(interaction):
            content = f'`{me} x {opponent}'
            view.move1.current_pp -= 1
            view.move1.update_label()
            view.check_power_points()
            messages = view.calculate_damage(me, opponent, me.move1)
            if view.struggle:
                view.struggle.callback = struggle_callback
            for msg in messages:
                content += f'\n{msg}'
            await interaction.response.edit_message(
                content=content + '`',
                view=view
            )
        async def move2_callback(interaction):
            content = f'`{me} x {opponent}'
            view.move2.current_pp -= 1
            view.move2.update_label()
            view.check_power_points()
            messages = view.calculate_damage(me, opponent, me.move2)
            if view.struggle:
                view.struggle.callback = struggle_callback
            for msg in messages:
                content += f'\n{msg}'
            await interaction.response.edit_message(
                content=content + '`',
                view=view
            )
        async def move3_callback(interaction):
            content = f'`{me} x {opponent}'
            view.move3.current_pp -= 1
            view.move3.update_label()
            view.check_power_points()
            messages = view.calculate_damage(me, opponent, me.move3)
            if view.struggle:
                view.struggle.callback = struggle_callback
            for msg in messages:
                content += f'\n{msg}'
            await interaction.response.edit_message(
                content=content + '`',
                view=view
            )
        async def move4_callback(interaction):
            content = f'`{me} x {opponent}'
            view.move4.current_pp -= 1
            view.move4.update_label()
            view.check_power_points()
            messages = view.calculate_damage(me, opponent, me.move4)
            if view.struggle:
                view.struggle.callback = struggle_callback
            for msg in messages:
                content += f'\n{msg}'
            await interaction.response.edit_message(
                content=content + '`',
                view=view
            )
        async def runaway_callback(interaction):
            view.lock_moves()
            await interaction.response.edit_message(
                content='You got away safely!',
                view=view
            )
            logger.info(
                f'\x1b[31m{interaction.user}\x1b[0m : Ran away safely!'
            )
        async def struggle_callback(interaction):
            await interaction.response.edit_message(
                content=f'{me} is struggling!',
                view=view
            )
        view.move1.callback = move1_callback
        view.move2.callback = move2_callback
        view.move3.callback = move3_callback
        view.move4.callback = move4_callback
        view.run_away.callback = runaway_callback


    @client.tree.command(
            name='battle', 
            description='Challenge the bot to a battle using selected pokémon!'
    )
    async def battle(interaction, *, pokemon1: str, pokemon2: str):
        if interaction.user == client.user:
            return
        if pokemon1 in pokedex and pokemon2 in pokedex:
            me = Pokemon(pokemon1, pokedex[pokemon1], learnsets[pokemon1]['learnset'], moves)
            opponent = Pokemon(pokemon2, pokedex[pokemon2], learnsets[pokemon2]['learnset'], moves)
            view = CustomView(me, opponent, mode='smart', timeout=360)
        else:
            logger.warning(f'Something went wrong! - CustomView Class')
            return
        await view_callbacks(view, me, opponent)
        logger.info(
            f'\x1b[31m{interaction.user}\x1b[0m : ({interaction.channel})'
        )
        await send_message(interaction, pokemon1, pokemon2, pokedex, view)

    
    @client.tree.command(
            name='random', 
            description='Challenge the bot to a random battle. The bot uses moves randomly!'
    )
    async def random_battle(interaction):
        if interaction.user == client.user:
            return
        pokemon1, pokemon2 = random.choices(list(learnsets.keys()), k=2)
        try:
            me = Pokemon(pokemon1, pokedex[pokemon1], learnsets[pokemon1]['learnset'], moves)
            opponent = Pokemon(pokemon2, pokedex[pokemon2], learnsets[pokemon2]['learnset'], moves)
            view = CustomView(me, opponent, timeout=360)
            await view_callbacks(view, me, opponent)
            logger.info(
                f'\x1b[31m{interaction.user}\x1b[0m : ({interaction.channel})'
            )
            await send_message(interaction, pokemon1, pokemon2, pokedex, view)
        except (TypeError, discord.errors.NotFound, discord.app_commands.errors.CommandInvokeError):
            logger.info(
                f'\x1b[31m{interaction.user}\x1b[0m : Error in Random Battle!'
            )
            await interaction.followup.send(
                '`Something went wrong!`'
            )
    

    @client.tree.command(
            name='smart', 
            description='Challenge the bot to a random battle. The bot uses the best possible moves!'
    )
    async def random_smart(interaction):
        if interaction.user == client.user:
            return
        pokemon1, pokemon2 = random.choices(list(learnsets.keys()), k=2)
        try:
            me = Pokemon(pokemon1, pokedex[pokemon1], learnsets[pokemon1].get('learnset', {}), moves)
            opponent = Pokemon(pokemon2, pokedex[pokemon2], learnsets[pokemon2].get('learnset', {}), moves)
            view = CustomView(me, opponent, mode='smart', timeout=360)
            await view_callbacks(view, me, opponent)
            logger.info(
                f'\x1b[31m{interaction.user}\x1b[0m : ({interaction.channel})'
            )
            await send_message(interaction, pokemon1, pokemon2, pokedex, view)
        except (TypeError, discord.errors.NotFound, discord.app_commands.errors.CommandInvokeError):
            logger.info(
                f'\x1b[31m{interaction.user}\x1b[0m : Could not find this pokémon!'
            )
            await interaction.followup.send(
                '`Something went wrong!`'
            )


    @client.tree.command(
            name='moveinfo', 
            description='Get some info about a pokémon move!'
    )
    async def move_info(interaction, *, move_name: str):
        if interaction.user == client.user:
            return
        try:
            move_name = move_name.lower().replace(' ', '').replace('-', '')
            if move_name not in moves:
                logger.info(
                    f'\x1b[31m{interaction.user}\x1b[0m : Could not find this move!'
                )
                await interaction.response.send_message(
                    f'`{move_name.title()} - Move not found!`'
                )
                return
            mv = moves[move_name]
            content = f'➡️ Move: {mv.get("name", "")}\n'
            content += f'➡️ Type: {mv.get("type", "")}\n'
            content += f'➡️ Description: {mv.get("desc", "")}\n'
            content += f'➡️ Base Power: {mv.get("basePower", 0)}\n'
            content += f'➡️ Category: {mv.get("category", "")}\n'
            content += f'➡️ PP: {mv.get("pp", 0)}\n'
            priority = mv.get("priority", 0)
            if priority != 0:
                content += f'➡️ Priority: {priority}'
            logger.info(
                f'\x1b[31m{interaction.user}\x1b[0m : {mv["name"]} found!'
            )
            await interaction.response.send_message('```' + content + '```')
        except discord.app_commands.errors.CommandInvokeError:            
            logger.warning(
                f'\x1b[31m{interaction.user}\x1b[0m : Error in move selection!'
            )
            await interaction.response.send_message(
                '`Something went wrong!`'
            )

    @client.tree.command(
            name='help', 
            description='Display a list of available commands'
    )
    async def help(interaction):
        content = '❕myuBot Help❕\n\n'
        content += '➡️ /battle [pokemon1] [pokemon2] - Challenge the bot using the selected pokémon\n\n'
        content += '➡️ /random - Challenge the bot to a battle with randomly selected pokémon.\n The bot will use moves randomly\n\n'
        content += '➡️ /smart - Challenge the bot to a battle with randomly selected pokémon.\n The bot will use the best possible moves against your pokémon\n\n'
        content += '➡️ /moveinfo [move_name] - Display information about a move\n'
        await interaction.response.send_message(
            '```' + content + '```'
        )

    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    client.run(TOKEN)


if __name__ == '__main__':
    run()