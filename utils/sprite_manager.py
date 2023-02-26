from PIL import Image, ImageOps


def sprite_path(pokedex_number):
    front = f'sprites/front/{pokedex_number}.png'
    back = f'sprites/back/{pokedex_number}.png'
    return front, back

def concatenate_sprites(pokedex_number):
    front, back = sprite_path(pokedex_number)
    try:
        img1 = Image.open(front)
    except (TypeError, OSError):
        return ''
    try:
        img2 = Image.open(back)
    except (TypeError, OSError):
        return front
    concat = Image.new('RGBA', (img1.width + img2.width, img1.height))
    concat.paste(img1, (0, 0))
    concat.paste(img2, (img1.width, 0))
    path = 'tmp/tmp.png'
    concat.save(path)
    return path

def get_pokemon_sprite(pokedex_number, sprite_front=False):
    front, back = sprite_path(pokedex_number)
    if sprite_front:
        try:
            img = Image.open(front).convert('RGBA')
            if img.size == (96, 96):
                img = img.resize((144, 144), Image.Resampling.LANCZOS)
        except (TypeError, OSError):
            return None
    else:
        try:
            img = Image.open(back).convert('RGBA')
            if img.size == (96, 96):
                img = img.resize((144, 144), Image.Resampling.LANCZOS)
        except (TypeError, OSError):
            try:
                img = ImageOps.mirror(Image.open(front).convert('RGBA'))
                if img.size == (96, 96):
                    img = img.resize((144, 144), Image.Resampling.LANCZOS)
            except (TypeError, OSError):
                return None
    return img

def place_on_battlefield(pokedex_number1, pokedex_number2):
    img1 = get_pokemon_sprite(pokedex_number1, sprite_front=False)
    img2 = get_pokemon_sprite(pokedex_number2, sprite_front=True)
    if not img1 or not img2:
        return
    battlefield = Image.open('battle/battle_background.png')
    battlefield.paste(img1, (40, 85), img1)
    battlefield.paste(img2, (240, 5), img2)
    battlefield.save('tmp/tmp.png')
    return 'tmp/tmp.png'

