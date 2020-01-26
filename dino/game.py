import tkinter

from dino import Dino
from sky import Sky
from window import Window
from platform import Platform

import time


class Game:

    win_width = 1450
    win_height = 800

    def __init__(self):
        self.win = Window((Game.win_width, Game.win_height))
        self.sky = Sky(Game.win_width, Game.win_height)
        self.platform = Platform(Game.win_width, 96, Game.win_height - 96 - 30)
        self.dino = None
        self.enemy_velocity = 250
        self.score = 0
        self.create_handlers()
        self.enemies = []

    def create_handlers(self):
        self.win.add_handler('w', lambda x: self.jump())
        self.win.add_handler('W', lambda x: self.jump())
        self.win.add_handler('<space>', lambda x: self.reset())

    def reset(self):
        if not self.dino.alive:
            self.dino.alive = True
            self.enemies = []
            self.score = 0

    def jump(self):
        if self.dino:
            self.dino.jump()

    @property
    def window_is_open(self):
        return self.win.open

    def check_collision_with_ground(self):
        if not (self.dino.y + self.dino.height >= self.platform.y):
            return
        self.dino.y = self.platform.y - self.dino.height
        self.dino.reset_force()
        self.dino.allow_jump()

    def update_dino(self, dt: float):
        if not self.dino:
            return
        self.dino.tick(dt)
        self.check_collision_with_ground()

    def remove_enemies(self):
        for enemy in self.enemies:
            if enemy.x + enemy.width < 0:
                self.enemies.remove(enemy)
            else:
                return

    def move_enemies(self, dt: float):
        delta = -dt * self.enemy_velocity
        for enemy in self.enemies:
            enemy.move(delta)

    def tick_enemies(self, dt: float):
        for enemy in self.enemies:
            enemy.tick(dt)

    def update_enemies(self, dt: float):
        self.move_enemies(dt)
        self.tick_enemies(dt)
        self.remove_enemies()

    def update_score(self, dt: float):
        self.score += dt * 10

    def update_platform(self, dt: float):
        delta = -dt * self.enemy_velocity
        self.platform.move(delta)

    def update(self, dt: float):
        self.update_dino(dt)
        self.update_enemies(dt)
        self.update_score(dt)
        self.update_platform(dt)
        self.sky.tick(dt)

    def tick(self, timedelta: float):
        if self.dino.alive:
            self.update(timedelta)
        self.draw()

    def display_score(self):
        c = self.win.canvas
        c.create_text(c.winfo_width() - 10, 20, text=f'Score: {int(self.score)}',
                      anchor=tkinter.E, font=("Purisa", 24))

    def display_game_over(self):
        c = self.win.canvas
        c.create_text(c.winfo_width() // 2, c.winfo_height() // 2,
                      text='Game Over', font=("Purisa", 80))
        c.create_text(c.winfo_width() // 2, c.winfo_height() // 2 + 60,
                      text='Press space to play again', font=("Purisa", 25))

    def draw(self):
        self.win.clear()
        self.win.draw(self.sky)
        self.win.draw(self.platform)
        for enemy in self.enemies:
            self.win.draw(enemy)
        if self.dino:
            self.win.draw(self.dino)
        if not self.dino.alive:
            self.display_game_over()
        self.display_score()
        self.win.update()

    def add_player(self, dino: Dino):
        self.dino = dino

    def add_enemy(self, enemy):
        self.enemies.append(enemy)
