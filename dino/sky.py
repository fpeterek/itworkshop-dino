import random
import tkinter

from PIL import Image, ImageTk


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Sky:

    image_width = 96 * 2
    image_height = 48 * 2
    orig_img = None
    small_img = None

    min_dist = 1.5

    y_jitter = 75

    upper_v = 125
    lower_v = 225

    @staticmethod
    def random_y(base: float):
        return base + random.randint(-Sky.y_jitter, Sky.y_jitter)

    @staticmethod
    def load_sprite():
        w = Sky.image_width
        h = Sky.image_height
        img = Image.open('resources/cloud.png')
        Sky.orig_img = ImageTk.PhotoImage(img.resize((w, h), Image.NONE))
        Sky.small_img = ImageTk.PhotoImage(img.resize((w // 2, h // 2), Image.NONE))

    def __init__(self, win_width: int, win_height: int):
        self.width = win_width
        self.height = win_height

        self.first_y = win_height // 4
        self.second_y = win_height // 5 * 2

        third = win_width // 3

        self.upper_row = [
            Position(random.randint(0, third), Sky.random_y(self.first_y)),
            Position(random.randint(third, third*2), Sky.random_y(self.first_y)),
            Position(random.randint(third*2, third*3), Sky.random_y(self.first_y)),
        ]
        self.lower_row = [
            Position(random.randint(0, third), Sky.random_y(self.second_y)),
            Position(random.randint(third, third * 2), Sky.random_y(self.second_y)),
            Position(random.randint(third * 2, third * 3), Sky.random_y(self.second_y)),
        ]

        self.upper_timer = 1.0
        self.lower_timer = 1.0

        if not Sky.orig_img:
            Sky.load_sprite()

    def move(self, dt: float):
        for p in self.upper_row:
            p.x -= dt * Sky.upper_v
            if p.x + self.width < 0:
                self.upper_row.remove(p)

        for p in self.lower_row:
            p.x -= dt * Sky.lower_v
            if p.x + (self.width // 2) < 0:
                self.lower_row.remove(p)

    def spawn_clouds(self, dt: float):
        self.upper_timer += dt
        self.lower_timer += dt

        spawn_upper = self.upper_timer >= Sky.min_dist
        spawn_lower = self.lower_timer >= Sky.min_dist

        if spawn_upper and random.randint(0, 150) == 100:
            self.upper_row.append(Position(self.width + self.image_width, Sky.random_y(self.first_y)))
            self.upper_timer = 0
        if spawn_lower and random.randint(0, 150) == 100:
            self.lower_row.append(Position(self.width + self.image_width, Sky.random_y(self.second_y)))
            self.lower_timer = 0

    def tick(self, dt: float):
        self.move(dt)
        self.spawn_clouds(dt)

    def draw(self, canvas: tkinter.Canvas):
        for p in self.upper_row:
            x = round(p.x)
            y = round(p.y)
            canvas.create_image(x, y, image=Sky.small_img, anchor=tkinter.CENTER)
        for p in self.lower_row:
            x = round(p.x)
            y = round(p.y)
            canvas.create_image(x, y, image=Sky.orig_img, anchor=tkinter.CENTER)

