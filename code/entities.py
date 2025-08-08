from raylib import * 
from pyray import * 
from os.path import join
from settings import * 

class Sprite:
    def __init__(self, texture: Texture2D, pos: Vector2):
        self.texture = texture
        self.pos: Vector2 = pos
        self.dir: Vector2 = Vector2()
        self.speed: int = 0 
        self.rect = Rectangle(self.pos.x, self.pos.y, self.texture.width, self.texture.height)


    def update(self, dt):
        self.pos.x += self.speed * self.dir.x * dt
        self.pos.y += self.speed * self.dir.y * dt  
        self.rect.x, self.rect.y = self.pos.x, self.pos.y
    def draw(self):
        draw_texture_v(self.texture, self.pos, WHITE)

class AnimatedSprite:
    def __init__(self, textures: list[Texture2D], pos: Vector2):
        self.textures = textures
        self.pos = pos
        self.anim_index = 0 
    
    def update(self, dt):
       self.anim_index += 1

    def draw(self):
        draw_texture_v(self.textures[int(self.anim_index) % len(self.textures)], self.pos, WHITE)

class Player(Sprite):

    def __init__(self, texture, pos):
        super().__init__(texture, pos)
        self.speed = PLAYER_SPEED
    
    def update(self, dt):
        # Movement
        self.dir.x = int(is_key_down(KEY_D)) - int(is_key_down(KEY_A))
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > (WINDOW_WIDTH - self.texture.width):
            self.pos.x = WINDOW_WIDTH - self.texture.width
        super().update(dt) 

class Rock(Sprite):
    def __init__(self, texture, pos):
        super().__init__(texture, pos)
        self.dir.y = 1
        self.speed = randint(METEOR_SPEED_RANGE[0], METEOR_SPEED_RANGE[1])
        self.toBlow = False
    
class Laser(Sprite):
    def __init__(self,texture,pos):
        super().__init__(texture, pos) 
        self.texture = texture
        self.pos = pos
        self.dir.y = -1
        self.speed = LASER_SPEED
