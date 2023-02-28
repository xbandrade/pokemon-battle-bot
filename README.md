# Pokémon Battle Bot
## A discord bot for Pokémon battles

## Setup
* Install the requirements using `pip install -r requirements.txt`
* Rename `.env-keys` to `.env` and store your Discord bot token
* Run `python -m main` to start the Discord bot

#### Both pokémon's HP bar and your pokémon's available moves will be shown in buttons using a Discord view. A run away button is also available to end the battle before one of the pokémon is unable to battle.
#### The battle messages will be shown above the battlefield picture, displaying the moves used and the damage dealt.

#### Every move has a limited number of power points, which is the number of times a pokémon can use the move. When a move runs out of power points, its button will be grayed out and you can no longer use that move.

<img src="https://raw.githubusercontent.com/xbandrade/pokemon-battle-bot/main/img/battle.png" width=48% height=48%> <img src="https://raw.githubusercontent.com/xbandrade/pokemon-battle-bot/main/img/smart.png" width=45% height=45%>

## Slash Commands
* `/battle [pokemon1] [pokemon2]` - Challenge the bot using the selected pokémon
* `/random` - Challenge the bot to a battle with randomly selected pokémon. The bot will use moves randomly
* `/smart` - Challenge the bot to a battle with randomly selected pokémon. The bot will use the best possible moves against your pokémon
* `/moveinfo [move_name]` - Display information about a move

<img src="https://github.com/xbandrade/pokemon-battle-bot/blob/main/img/move.png" width=70% height=70%>

#### The bot edits and updates its own message and view buttons, so it won't spam messages on every used move.

#### All pokémon and moves data were obtained from Pokémon Showdown's Pokédex.
