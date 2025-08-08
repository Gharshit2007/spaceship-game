from settings import *
from custom_timer import Timer
from entities import *
from funcs import *
import os

# MAKE SURE DIRECTOY IS OK
if "images" in os.listdir(os.getcwd()):
    print("OK")
else:
    os.chdir("..")


init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "My Game")
init_audio_device()
set_target_fps(60)

player_texture = load_texture(join("images", "spaceship.png"))
player = Player(player_texture,Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT - 100))

laser_texture = load_texture(join("images", "laser.png"))
laser_sound = load_sound(join("audio", "laser.wav"))
LASERS: list[Laser] = []

STARS: list[Sprite] = []
star_texture = load_texture(join("images", "star.png"))

ROCKS: list[Rock] = []
rock_texture = load_texture(join("images", "meteor.png")) 

EXPLOSIONS = []
explosion_textures = [load_texture(join("images", "explosion", f'{i+1}.png')) for i in range(28)]

explosion_sound = load_sound(join("audio", "explosion.wav"))
bg_music = load_music_stream(join("audio","music.wav"))

SCORE_POS: Vector2 = Vector2(WINDOW_WIDTH / 2 - 15,25)
font = load_font(join("font", "Stormfaze.otf"))


def main():
    STARS = get_background(star_texture)
    set_music_volume(bg_music, 1)
    play_music_stream(bg_music)
    SCORE: int = 1

    rock_timer = Timer(METEOR_TIMER_DURATION, True, True, create_rock)
    while not window_should_close():
        dt = get_frame_time()

        #TIMERS
        rock_timer.update()

        # LASERS
        if is_key_pressed(KEY_SPACE):
            LASERS.append(Laser(laser_texture, Vector2(player.pos.x + player_texture.width/2 - 5, player.pos.y - 55)))
            play_sound(laser_sound)

        #UPDATES
        update_music_stream(bg_music)
        player.update(dt)
        for laser in LASERS:
            if laser.pos.y < 0:
                LASERS.remove(laser)
                break
            for rock in ROCKS:
                if check_collision_recs(laser.rect,rock.rect):
                    rock.toBlow = True
                    LASERS.remove(laser)
                    SCORE += 1
                    play_sound(explosion_sound)
                    break
            laser.update(dt)
        for rock in ROCKS:
            if rock.pos.y > WINDOW_HEIGHT:
                ROCKS.remove(rock)
                break
            if rock.toBlow:
                ROCKS.remove(rock)
                EXPLOSIONS.append(AnimatedSprite(explosion_textures, Vector2(laser.pos.x - 10, rock.pos.y + 20)))
            rock.update(dt)
        for explosion in EXPLOSIONS:
            if explosion.anim_index > len(explosion.textures):
                EXPLOSIONS.remove(explosion)
            explosion.update(dt)
            
        # DRAWING
        begin_drawing()

        clear_background(BG_COLOR)
        for star in STARS:
            star.draw()
        for laser in LASERS:
            laser.draw()
            # draw_rectangle_rec(laser.rect, WHITE)
        for rock in ROCKS:
            rock.draw()
            # draw_rectangle_rec(rock.rect, WHITE)  
        for explosion in EXPLOSIONS: 
            explosion.draw()
        player.draw()
        draw_text_ex(font, convert_to_str(SCORE), SCORE_POS, FONT_SIZE, 1, WHITE)
        end_drawing()

    close_audio_device()
    close_window()

def create_rock():
    ROCKS.append(Rock(rock_texture, Vector2(randint(10, WINDOW_WIDTH - rock_texture.width - 10), -10)))

if __name__ == "__main__":
    main()
