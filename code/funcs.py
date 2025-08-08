from settings import *
from entities import *
from random import randint

def get_background(star_texture: Texture2D) -> list[Sprite]:
    STARS = []
    number_of_stars = randint(10,25)
    for i in range(number_of_stars):
        STARS.append(Sprite(star_texture, Vector2(randint(5, WINDOW_WIDTH), randint(10, WINDOW_HEIGHT - 10))))
    return STARS


def convert_to_str(int:int):
    if int < 10:
        return str(f'0{int}')
    else:
        return str(int)