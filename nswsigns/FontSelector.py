from PIL import ImageFont
import os
from numpy import random

class FontSelector:

    def __init__(self):

        self.fontPaths = []
        self.numFonts = 0

        for name in os.listdir("nswsigns/fonts"):
            if name[-4:] != ".ttf": continue
            self.fontPaths.append(f"nswsigns/fonts/{name}")
            self.numFonts += 1

    # Select a random font from those provided
    def getRandomFont(self, size):

        randomInt = random.randint(0, self.numFonts)
        font = ImageFont.truetype(self.fontPaths[randomInt], size)
        return font




test = FontSelector()

for i in range(100):
    test.getRandomFont(4)