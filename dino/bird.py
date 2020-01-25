import math
import tkinter
from PIL import ImageTk, Image


class Bird:
    orig_img = None
    image_width = 0
    width = 0
    height = 0

    @staticmethod
    def load_sprite(width, height):
        img = Image.open('resources/bird.png').resize((width, height), Image.NONE)
        Bird.orig_img = img

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # if width != Dino.image_width:
        #     Bird.load_sprite(width, height)

        # self.sprite = ImageTk.PhotoImage(Bird.orig_img)

    def draw(self, canvas: tkinter.Canvas):
        x = round(self.x)
        y = round(self.y)
        canvas.create_rectangle(x, y, x + self.width, y + self.height, fill='#53d45f')
        # canvas.create_image(self.x, self.y, image=self.sprite, anchor=tkinter.CENTER)

    def move(self, dx):
        self.x += dx

