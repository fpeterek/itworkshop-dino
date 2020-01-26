import math
import tkinter
from PIL import ImageTk, Image


class Cactus:
    orig_img = None
    image_width = 0
    width = 0
    height = 0

    @staticmethod
    def load_sprite(width, height):
        img = Image.open('resources/cactus.png').resize((width, height), Image.NONE)
        Cactus.image_width = width
        Cactus.orig_img = img

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        if width != Cactus.image_width:
            Cactus.load_sprite(width, height)

        self.sprite = ImageTk.PhotoImage(Cactus.orig_img)

    def draw(self, canvas: tkinter.Canvas):
        x = round(self.x)
        y = round(self.y)
        # canvas.create_rectangle(x, y, x + self.width, y + self.height, fill='#53d45f')
        canvas.create_image(x, y, image=self.sprite, anchor=tkinter.NW)

    def move(self, dx):
        self.x += dx

