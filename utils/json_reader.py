import json

from PIL import Image

from utils.sprite_manager import place_on_battlefield


def load_pokedex():
    with open('json/pokedex.json', encoding='utf8') as f:
        pokedex = json.load(f)
    return pokedex

def load_learnsets():
    with open('json/learnsets.json', encoding='utf8') as f:
        learnset = json.load(f)
    return learnset

def load_moves():
    with open('json/moves.json', encoding='utf8') as f:
        moves = json.load(f)
    return moves


if __name__ == '__main__':
    pokedex = load_pokedex()
    n1 = pokedex['espeon']['num']
    n2 = pokedex['farigiraf']['num']
    path = place_on_battlefield(n1, n2)
    battlefield = Image.open(path)
    battlefield.show()
