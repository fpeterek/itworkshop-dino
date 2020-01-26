import tkinter

from PIL import Image, ImageTk


class Platform:

    color = '#807d75'

    def __init__(self, width, height, y):
        self.sprite_w = 96
        img = Image.open('resources/grass.png')
        img = img.resize((self.sprite_w, self.sprite_w), Image.NONE)
        self.img = ImageTk.PhotoImage(img)
        self.x = 0
        self.begin = 0
        self.y = y
        self.width = width
        self.height = height

    def move(self, dx):
        self.begin += dx / 2
        if self.begin < -self.sprite_w:
            self.begin += self.sprite_w

    def draw(self, canvas: tkinter.Canvas):
        begin = round(self.begin)
        for i in range(begin, self.width + self.sprite_w, self.sprite_w):
            canvas.create_image(begin + i, self.y, image=self.img, anchor=tkinter.NW)
