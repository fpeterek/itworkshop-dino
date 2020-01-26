import math
import tkinter
from PIL import ImageTk, Image


class Dino:

    jump_force = 500

    terminal_velocity = 400
    g = 600

    orig_img = None
    image_width = 0
    width = 0
    height = 0

    sprite_count = 2

    sheet = None

    @staticmethod
    def load_spritesheet():
        img: Image.Image = Image.open('resources/dino.png')
        img_dim = Dino.image_width
        img = img.resize((img_dim * Dino.sprite_count, img_dim), Image.NONE)
        count = Dino.sprite_count
        sheet = [
            img.crop((i * img_dim, 0, img_dim * (i + 1), img_dim)) for i in range(0, count)
        ]
        Dino.sheet = list(map(lambda image: ImageTk.PhotoImage(image), sheet))

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.force = 0
        self.can_jump = False
        self.alive = True

        if Dino.image_width != width:
            Dino.image_width = width
            Dino.load_spritesheet()

        self.phase = 0
        self.counter = 0.0
        self.time_per_frame = 0.15

    def draw(self, canvas: tkinter.Canvas):
        # canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill='#f00000')
        x = round(self.x)
        y = round(self.y)
        canvas.create_image(x, y, image=Dino.sheet[self.phase], anchor=tkinter.NW)

    def reset_force(self):
        self.force = 0

    def bound_forces(self):
        self.force = min(self.force, Dino.terminal_velocity)

    def calc_forces(self, dt):
        self.force += dt * Dino.g
        self.bound_forces()

    def move(self, dt):
        self.y += self.force * dt

    def update_sprite(self, dt):
        if self.can_jump:
            self.counter += dt
        if self.counter > self.time_per_frame:
            self.counter -= self.time_per_frame
            self.phase += 1
            self.phase %= Dino.sprite_count

    def tick(self, timedelta):
        self.calc_forces(timedelta)
        self.move(timedelta)
        self.update_sprite(timedelta)

    def jump(self):
        if self.can_jump:
            self.force -= Dino.jump_force
            self.can_jump = False

    def allow_jump(self):
        self.can_jump = True

    def collides_with(self, enemy) -> bool:
        hitbox_mod = self.width // 10
        x_wise_miss = self.x + self.width - hitbox_mod < enemy.x or self.x + hitbox_mod > enemy.x + enemy.width
        y_wise_miss = self.y + self.height - hitbox_mod < enemy.y or self.y > enemy.y + enemy.height
        return not (x_wise_miss or y_wise_miss)

    def die(self):
        self.alive = False
