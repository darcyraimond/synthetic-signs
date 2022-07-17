from sign import getTransformedPoint, pasteImage, Sign
from SignGenerator import Generator
import numpy as np
import random
import draw

"""
NOTES:
    - Treats image like a grid. Maximum width is 2, maximum heigth can
      be set (default 6)
    - At each point, randomly decides whether or not to add either one
      horizontal sign (2 wide, 1 high) or two vertical signs (2 wide, 2
      high)
"""

class MultiSign:

    def __init__(self, generator: Generator):

        # Constituent signs
        self.signs = []
        self.numSigns = 0
        self.generator = generator

        # Images at various points
        self.image = None
        self.transformed = None
        self.final = None

        # Ground truths
        self.bounds = []
        self.textBounds = []
        self.hasLeftArrow = []
        self.hasRightArrow = []

        # Dimension transform information
        self.transformMatrix = None
        self.transformBounds = []
        self.transformTextBounds = []
        self.finalBounds = []
        self.finalTextBounds = []

        # Specific multi-sign stuff
        self.pattern = [] # Just a sequence of 1s and 2s if multisign

        self.create()

    def img(self):
        return self.image.copy()

    def paste(self, sign: Sign, tl):
        # Add to image
        shape = sign.image.shape
        self.image[tl[0]:tl[0]+shape[0], tl[1]:tl[1]+shape[1]] = sign.image

        # Aadd sign bounding boxes
        thisSignBounds = []
        for bound in sign.bounds:
            thisSignBounds.append((bound[0] + tl[0], bound[1] + tl[1]))
        self.bounds.append(thisSignBounds)

        # TODO: Add text bounding boxes
        #print(sign.textBounds)
        
        for item in sign.textBounds:
            boundSet = []
            for bound in item[0]:
                boundSet.append((bound[0] + tl[0], bound[1] + tl[1]))
            self.textBounds.append([boundSet, item[1]])


    def create(self, extraP=0.6, maxHeight=6):

        # Create a pattern to use
        total = 0
        while total < maxHeight:

            if random.random() < 1 - extraP and total > 0: break # Probablistically stop
            
            # If here, we want to add another sign
            val = random.choice([2])
            if total + val > maxHeight: break # Stop if this would make the sign too high

            # Add this to pattern
            self.pattern.append(val)
            total += val

        # Create a standard image array to use
        if total > 1:
            height = total * 500
            width = 1000
        else:
            if random.random() < 0.8:
                height = 1000
                width = 500
            else:
                height = 500
                width = 1000
        self.image = np.zeros((height, width, 4), dtype = np.uint8)

        # Go through and paste signs as necessary
        upToHeight = 0
        for num in self.pattern:

            if num == 2:
                # Generate two signs
                sign1 = self.generator.get(arrows="left", orientation="vertical")
                sign2 = self.generator.get(arrows="right", orientation="vertical")

                # Paste signs on image
                self.paste(sign1, (upToHeight, 0))
                self.paste(sign2, (upToHeight, 500))

                upToHeight += 1000

            # If invalid, raise exception
            else:
                raise Exception(f"Should not have num of {num}")
                

    def getImage(self, withBounds=False, withTextBounds=False, thickBounds=True, thickTextBounds=False):
        img = self.img()

        if withBounds:
            for bound in self.bounds:
                for i in range(len(bound)):
                    draw.drawLine(img, bound[i-1], bound[i], (255, 200, 0, 255), thickBounds)

        if withTextBounds:
            for bbox in self.textBounds:
                for i in range(len(bbox[0])):
                    draw.drawLine(img, bbox[0][i-1], bbox[0][i], (0, 200, 255, 255), thickTextBounds)

        return img


