import random
import time

from bird import Bird
from cactus import Cactus
from game import Game
from dino import Dino


def time_millis():
    return int(time.time() * 1000)


def get_cactus():
    return Cactus(Game.win_width, Game.win_height - 221, 96, 96)


def get_bird():
    return Bird(Game.win_width, Game.win_height - 330, 96, 48)


def get_enemy():
    return get_cactus() if random.randint(0, 2) else get_bird()


def main():

    game = Game()

    player = Dino(50, game.win_height - 250, 64, 64)
    game.add_player(player)

    spawn_thresholds = [1.5, 1.75, 2, 2.5, 3, 3.50]

    enemy_spawn_threshold = 3.5
    time_since_last_spawn = enemy_spawn_threshold

    last_time = time_millis()

    max_speedups = 3
    speedups = 0
    speedup_after = 15.0
    speedup_timer = 0

    # Takto lze změnit texturu země ve hře
    # Případně lze dodat vlastní textury do složky resources a následně
    # Lze využít i vlastních textur
    # game.change_ground('resources/grass.png')
    # game.change_ground('resources/grass_alt.png')
    # game.change_ground('resources/sand.png')
    while game.window_is_open:

        # Počítání časového rozdílu
        current_time = time_millis()
        delta = (current_time - last_time) / 1000
        game.tick(delta)
        last_time = current_time

        # Logika vytváření nepřátelských entit
        time_since_last_spawn += delta
        if time_since_last_spawn >= enemy_spawn_threshold:
            game.add_enemy(get_enemy())
            time_since_last_spawn = 0
            enemy_spawn_threshold = random.choice(spawn_thresholds)

        # Kolize s nepřátelskými entitami
        for enemy in game.enemies:
            if player.collides_with(enemy):
                player.die()

        # Logika zrychlování hry
        speedup_timer += delta
        if speedups < max_speedups and speedup_timer >= speedup_after:
            speedup_timer = 0
            game.increase_speed()
