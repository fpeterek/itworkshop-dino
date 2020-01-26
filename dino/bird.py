import math
import tkinter
from PIL import ImageTk, Image


class Bird:
    orig_img = None
    image_width = 0
    width = 0
    height = 0

    sprite_count = 2
    time_per_frame = 0.25

    sheet = None

    @staticmethod
    def load_spritesheet():

        width = Bird.image_width
        height = width // 2

        img = Image.open('resources/bird.png').resize((width * Bird.sprite_count, height), Image.NONE)
        count = Bird.sprite_count
        sheet = [
            img.crop((i * width, 0, width * (i + 1), height)) for i in range(0, count)
        ]
        Bird.sheet = list(map(lambda image: ImageTk.PhotoImage(image), sheet))

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        if Bird.image_width != width:
            Bird.image_width = width
            Bird.load_spritesheet()

        self.phase = 0
        self.counter = 0.0

    def draw(self, canvas: tkinter.Canvas):
        x = round(self.x)
        y = round(self.y)
        # canvas.create_rectangle(x, y, x + self.width, y + self.height, fill='#53d45f')
        canvas.create_image(x, y, image=Bird.sheet[self.phase], anchor=tkinter.NW)

    def tick(self, dt):
        self.counter += dt
        if self.counter > Bird.time_per_frame:
            self.counter -= Bird.time_per_frame
            self.phase += 1
            self.phase %= Bird.sprite_count

    def move(self, dx):
        self.x += dx

