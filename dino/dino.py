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

    @staticmethod
    def load_sprite(width, height):
        img = Image.open('resources/dino.png').resize((width, height), Image.NONE)
        Dino.orig_img = img

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.force = 0
        self.can_jump = False
        self.alive = True

        # if width != Dino.image_width:
        #     Dino.load_sprite(width, height)

        # self.sprite = ImageTk.PhotoImage(Dino.orig_img)

    def draw(self, canvas: tkinter.Canvas):
        canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill='#f00000')
        # canvas.create_image(self.x, self.y, image=self.sprite, anchor=tkinter.CENTER)

    def reset_force(self):
        self.force = 0

    def bound_forces(self):
        self.force = min(self.force, Dino.terminal_velocity)

    def calc_forces(self, dt):
        self.force += dt * Dino.g
        self.bound_forces()

    def move(self, dt):
        self.y += self.force * dt

    def tick(self, timedelta):
        if not timedelta:
            return
        self.calc_forces(timedelta)
        self.move(timedelta)

    def jump(self):
        if self.can_jump:
            self.force -= Dino.jump_force
            self.can_jump = False

    def allow_jump(self):
        self.can_jump = True

    def collides_with(self, enemy) -> bool:
        x_wise_miss = self.x + self.width < enemy.x or self.x > enemy.x + enemy.width
        y_wise_miss = self.y + self.height < enemy.y or self.y > enemy.y + enemy.height
        return not (x_wise_miss or y_wise_miss)

    def die(self):
        self.alive = False
