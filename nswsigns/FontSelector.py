from PIL import ImageFont
import os
from numpy import random

class FontSelector:

    def __init__(self):

        self.fontPaths = []
        self.numFonts = 0

        for name in os.listdir("nswsigns/fonts"):
            self.fontPaths.append(f"nswsigns/fonts/{name}")
            self.numFonts += 1
        print("Num fonts:", self.numFonts)

    # Select a random font from those provided
    def getRandomFont(self, size):

        randomInt = random.randint(0, self.numFonts)
        font = ImageFont.truetype(self.fontPaths[randomInt], size)
        return font



test = FontSelector()

for i in range(100):
    test.getRandomFont(4)