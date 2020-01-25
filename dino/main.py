import random
import time

from cactus import Cactus
from game import Game
from dino import Dino


def time_millis():
    return time.time_ns() // 1_000_000


def main():

    game = Game()

    player = Dino(50, game.win_height - 250, 50, 50)
    game.add_player(player)

    spawn_thresholds = [1.5, 1.75, 2, 2.5, 3, 3.50]

    enemy_spawn_threshold = 3.5
    time_since_last_spawn = enemy_spawn_threshold

    last_time = time_millis()

    while game.window_is_open:
        current_time = Game.millis()
        delta = (current_time - last_time) / 1000
        game.tick(delta)
        last_time = current_time

        time_since_last_spawn += delta
        if time_since_last_spawn >= enemy_spawn_threshold:
            if random.randint(0, 2):
                game.add_enemy(Cactus(Game.win_width, Game.win_height - 227, 60, 100))
            else:
                game.add_enemy(Cactus(Game.win_width, Game.win_height - 330, 100, 50))
            time_since_last_spawn = 0
            enemy_spawn_threshold = random.choice(spawn_thresholds)

        for enemy in game.enemies:
            if player.collides_with(enemy):
                player.die()
