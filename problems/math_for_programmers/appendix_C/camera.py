"""


created at 2024/10/11
"""
import os
from math import ceil

from PIL import Image
from pygame.image import save
from pygame.time import Clock


class Camera:
    def __init__(self, name, shots=None, dir_='figs', comic_strip=None):
        self.dir = os.path.join(os.getcwd(), dir_)

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        self.clock = Clock()
        self.name = name

        if shots is None:
            shots = []

        try:
            self.shots = sorted(shots)
            self.remaining_shots = sorted(shots)
        except TypeError:
            self.shots = shots
            self.remaining_shots = shots

        self.total_ticks = 0
        self.made_comic_strip = False
        self.comic_strip = comic_strip
        self.window = None

    def set_window(self, window):
        self.window = window

    def is_shooting(self):
        if self.shots and not self.remaining_shots and (self.made_comic_strip or not self.comic_strip):
            return False
        else:
            return True

    def indexes(self):
        if type(self.shots) == int:
            return range(0, self.shots)
        else:
            return range(0, len(self.shots))

    def make_comic_strip(self):
        # https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python

        image_files = [
            os.path.join(self.dir, self.name + str(idx) + ".png")
            for idx in self.indexes()
        ]
        images = map(Image.open, image_files)
        width, height = images[0].size

        total_width = width * self.comic_strip
        max_height = height * int(ceil(len(images) / float(self.comic_strip)))

        new_im = Image.new('RGB', (total_width, max_height))

        for i, im in enumerate(images):
            x_offset = (i % self.comic_strip) * width
            y_offset = (i / self.comic_strip) * height
            print('offsets', (x_offset, y_offset))
            new_im.paste(im, (x_offset, y_offset))

        new_im.save(os.path.join(self.dir, self.name + '_comic_strip.png'))
        self.made_comic_strip = True

    def should_shoot(self):
        if type(self.remaining_shots) == int:
            return self.get_fps() > 0 and (self.remaining_shots > 0)
        else:
            return self.remaining_shots and self.total_ticks >= self.remaining_shots[0]

    def shoot(self):
        if type(self.remaining_shots) == int:
            idx = self.shots - self.remaining_shots
            self.remaining_shots = self.remaining_shots - 1
        else:
            idx = self.shots.index(self.remaining_shots[0])
            self.remaining_shots.pop(0)

        image_name = os.path.join(self.dir, self.name + str(idx) + ".png")
        save(self.window, image_name)

    def tick(self):
        res = self.clock.tick()
        self.total_ticks += res

        if self.should_shoot():
            self.shoot()

        elif self.comic_strip and not self.made_comic_strip and not self.remaining_shots:
            self.make_comic_strip()

        return res

    def get_fps(self):
        return self.clock.get_fps()


default_camera = Camera("default_camera", [])
