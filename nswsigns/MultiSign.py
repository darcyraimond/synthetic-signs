from sign import getTransformedPoint, pasteImage, Sign
from SignGenerator import Generator
import numpy as np
import random
import draw
from timeLimitRandomiser import getDirectionalDTs
import cv2
import json

"""
NOTES:
    - Treats image like a grid. Maximum width is 2, maximum heigth can
      be set (default 6)
    - At each point, randomly decides whether or not to add either one
      horizontal sign (2 wide, 1 high) or two vertical signs (2 wide, 2
      high)
"""

def pasteImage4D(background, sign, start=(0,0)):
    stack = np.stack([sign[:,:,3],sign[:,:,3],sign[:,:,3],sign[:,:,3]], -1) / 255
    #print("stack", stack.shape)
    tmp = np.array(background[start[0]:start[0]+sign.shape[0], start[1]:start[1]+sign.shape[1]], dtype = float)
    """print("tmp", tmp.shape)
    print("sign", sign.shape)
    print("start", start)
    print("background", background.shape)
    print("")"""
    signTemp = np.array(sign[:,:,:], dtype = float)
    tmp = np.array(tmp * (1 - stack) + signTemp * stack, dtype = np.uint8)
    background[start[0]:start[0]+sign.shape[0], start[1]:start[1]+sign.shape[1]] = tmp

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
        self.pattern = None # Just a sequence of 1s and 2s if multisign
        self.total = 0

        self.create()

    def img(self):
        return self.image.copy()


    def paste(self, sign: Sign, tl):
        # Add to image
        pasteImage4D(self.image, sign.image, tl)

        # Add sign bounding boxes
        thisSignBounds = []
        for bound in sign.bounds:
            thisSignBounds.append((bound[0] + tl[0], bound[1] + tl[1]))
        self.bounds.append(thisSignBounds)

        # Add text bounding boxes
        for item in sign.textBounds:
            boundSet = []
            for bound in item[0]:
                boundSet.append((bound[0] + tl[0], bound[1] + tl[1]))
            self.textBounds.append([boundSet, item[1]])


    def createPattern(self, extraP=0.6, maxHeight=6):

        self.pattern = []

        while self.total < maxHeight:

            if random.random() < 1 - extraP and self.total > 1: break # Probablistically stop
            
            # If here, we want to add another sign
            val = random.choice([1, 2])
            if self.total + val > maxHeight: break # Stop if this would make the sign too high

            # Add this to pattern
            self.pattern.append(val)
            self.total += val



    def create(self, extraP=0.6, maxHeight=6):

        if self.pattern is None: self.createPattern(extraP, maxHeight)

        """# Create a standard image array to use
        if self.total > 1:
            height = self.total * 500
            width = 1000
        else:
            if random.random() < 0.8:
                height = 1000
                width = 500
            else:
                height = 500
                width = 1000
        self.image = np.zeros((height, width, 4), dtype = np.uint8)"""

        # Place signs in array
        for val in self.pattern:
            if val == 1:
                # Append horizontal sign parameters
                self.signs.append(self.generator.getParams(orientation = "horizontal"))
            elif val == 2:
                # Append two different horizontal signs # TODO: remove restriction on arrow directions
                self.signs.append(self.generator.getParams(orientation = "vertical"))
                self.signs.append(self.generator.getParams(orientation = "vertical"))

        # Create arrays for each arrow direction
        isLeft = []
        isRight = []
        for sign in self.signs:
            isLeft.append(sign["left arrow"])
            isRight.append(sign["right arrow"])

        dateTimes = getDirectionalDTs(self.signs, isLeft, isRight)

        # Create a standard image array to use
        if self.total > 1:
            height = self.total * 500
            width = 1000
        else:
            if random.random() < 0.8:
                height = 1000
                width = 500
            else:
                height = 500
                width = 1000
        maxDev = 35
        height += maxDev
        width += maxDev
        self.image = np.zeros((height, width, 4), dtype = np.uint8)

        # Go through array and paste images as necessary
        
        upTo = 0
        upToHeight = 0
        
        for val in self.pattern:
            if val == 2:
                
                xdev = random.randint(0, maxDev)
                ydev = random.randint(0, maxDev)
                sign: Sign = self.generator.genFromParams(self.signs[upTo], times=dateTimes[upTo])
                self.paste(sign, (upToHeight + ydev, 0 + xdev))
                self.signs[upTo]["full string"] = sign.fullStringPre()
                upTo += 1

                xdev = random.randint(0, maxDev)
                ydev = random.randint(0, maxDev)
                sign: Sign = self.generator.genFromParams(self.signs[upTo], times=dateTimes[upTo])
                self.paste(sign, (upToHeight + ydev, 495 + xdev))
                self.signs[upTo]["full string"] = sign.fullStringPre()
                upTo += 1

                upToHeight += 990

            elif val == 1:

                xdev = random.randint(0, maxDev)
                ydev = random.randint(0, maxDev)
                sign: Sign = self.generator.genFromParams(self.signs[upTo], dateTimes[upTo])
                self.paste(sign, (upToHeight + ydev, 0 + xdev))
                self.signs[upTo]["full string"] = sign.fullStringPre()
                upTo += 1

                upToHeight += 495

    def transform(self, transformPercentage=0.2, transformP=0.95):

        image = self.image.copy()

        height = image.shape[0]
        width = image.shape[1]

        src = np.float32([[0, 0], [0, height], [width, 0], [width, height]])

        if random.random() < transformP:
            topLeft = [random.uniform(0, width * transformPercentage), random.uniform(0, height * transformPercentage)]
            bottomLeft = [random.uniform(0, width * transformPercentage), random.uniform(height * (1 - transformPercentage), height)]
            topRight = [random.uniform(width * (1 - transformPercentage), width), random.uniform(0, height * transformPercentage)]
            bottomRight = [random.uniform(width * (1 - transformPercentage), width), random.uniform(height * (1 - transformPercentage), height)]
            dst = np.float32([topLeft, bottomLeft, topRight, bottomRight])
        else:
            dst = src

        mat = cv2.getPerspectiveTransform(src, dst)
        image = cv2.warpPerspective(image, mat, (image.shape[1] - 1, image.shape[0] - 1))
        self.transformed = image
        self.transformMatrix = mat

        # Transform bounding box coordinates
        for bound in self.bounds:
            coords = []
            for pt in bound:
                coords.append(getTransformedPoint(pt, self.transformMatrix))
            self.transformBounds.append(coords)

        # Transform text bounding box coordinates
        for textTuple in self.textBounds:
            coords = []
            for pt in textTuple[0]:
                coords.append(getTransformedPoint(pt, self.transformMatrix))
            self.transformTextBounds.append((coords, textTuple[1]))


    def addBackground(self, background, blankP=0.1):

        if random.random() < blankP:
            self.final = background
            self.finalBounds = []
            self.finalTextBounds = []
            return

        sign = self.transformed
        
        # Resize sign to fit on background
        shape0 = sign.shape[0]
        shape1 = sign.shape[1]
        if sign.shape[0] > background.shape[0]:
            shape0 = background.shape[0]
            shape1 = background.shape[0] * sign.shape[1] / sign.shape[0]
        if sign.shape[1] > background.shape[1]:
            shape1 = min(background.shape[1], shape1)
            shape0 = min(background.shape[1] * sign.shape[0] / sign.shape[1], shape0)
        ratio = shape0 / sign.shape[0]

        sign = cv2.resize(sign, (int(round(shape1)), int(round(shape0))))

        # Add the image to the background
        randx = random.randrange(0, background.shape[0] - sign.shape[0] + 1)
        randy = random.randrange(0, background.shape[1] - sign.shape[1] + 1)
        pasteImage(background, sign, (randx, randy))

        self.final = background

        # Handle bounding boxes
        # Transform bounding box coordinates
        self.finalBounds = []
        for bound in self.transformBounds:
            coords = []
            for pt in bound:
                coords.append((pt[0] * ratio + randx, pt[1] * ratio + randy))
            self.finalBounds.append(coords)

        # Transform text bounding box coordinates
        for textTuple in self.transformTextBounds:
            coords = []
            for pt in textTuple[0]:
                coords.append((pt[0] * ratio + randx, pt[1] * ratio + randy))
            self.finalTextBounds.append((coords, textTuple[1]))
                

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


    def getTransformed(self, withBounds=False, withTextBounds=False, thickBounds=True, thickTextBounds=False):
        img = self.transformed.copy()

        if withBounds:
            for bound in self.transformBounds:
                for i in range(len(bound)):
                    draw.drawLine(img, bound[i-1], bound[i], (255, 200, 0, 255), thickBounds)

        if withTextBounds:
            for bbox in self.transformTextBounds:
                for i in range(len(bbox[0])):
                    draw.drawLine(img, bbox[0][i-1], bbox[0][i], (0, 200, 255, 255), thickTextBounds)

        return img

    def getFinal(self, withBounds=False, withTextBounds=False, thickBounds=True, thickTextBounds=False):
        img = self.final.copy()

        if withBounds:
            for bound in self.finalBounds:
                for i in range(len(bound)):
                    draw.drawLine(img, bound[i-1], bound[i], (255, 200, 0), thickBounds)

        if withTextBounds:
            for bbox in self.finalTextBounds:
                for i in range(len(bbox[0])):
                    draw.drawLine(img, bbox[0][i-1], bbox[0][i], (0, 200, 255), thickTextBounds)

        return img

    def outputTxtHelper(self, path, textBounds):
        
        out = ""
        
         # Only get text bounding boxes
        for bbox in textBounds:
            out += str(int(round(bbox[0][0][1]))) + ", "
            out += str(int(round(bbox[0][0][0]))) + ", "
            out += str(int(round(bbox[0][3][1]))) + ", "
            out += str(int(round(bbox[0][3][0]))) + ", "
            out += str(int(round(bbox[0][2][1]))) + ", "
            out += str(int(round(bbox[0][2][0]))) + ", "
            out += str(int(round(bbox[0][1][1]))) + ", "
            out += str(int(round(bbox[0][1][0]))) + ", "
            out += bbox[1] + "\n"

        # Write to file
        if out != "":
            while out[-1] == "\n": out = out[:-1]
        file = open(path, "w+")
        file.write(out)
        file.close()

    def outputTxt(self, path, version="final"):

        if version == "final":
            return self.outputTxtHelper(path, self.finalTextBounds)
        elif version == "raw":
            return self.outputTxtHelper(path, self.textBounds)

        print(f"Error: no output version {version}")
        exit(1)

    def outputJsonHelper(self, path, signBounds, textBounds):

        out = []
        for bbox, param in zip(signBounds, self.signs):
            coordinates = [
                int(round(bbox[0][1])),
                int(round(bbox[0][0])),
                int(round(bbox[3][1])),
                int(round(bbox[3][0])),
                int(round(bbox[2][1])),
                int(round(bbox[2][0])),
                int(round(bbox[1][1])),
                int(round(bbox[1][0]))
            ]
            d = {
                "Coordinates": coordinates,
                "Text": param["full string"]
            }
            out.append(d)


        # Get regular bounds
        for bbox in textBounds:

            # Fix coords
            coordinates = [
                int(round(bbox[0][0][1])),
                int(round(bbox[0][0][0])),
                int(round(bbox[0][3][1])),
                int(round(bbox[0][3][0])),
                int(round(bbox[0][2][1])),
                int(round(bbox[0][2][0])),
                int(round(bbox[0][1][1])),
                int(round(bbox[0][1][0]))
            ]
            d = {
                "Coordinates": coordinates,
                "Text": bbox[1]
            }
            out.append(d)

        # Write to file
        file = open(path, "w+")
        file.write(json.dumps(out, indent = 4))
        file.close()

    def outputJson(self, path, version="final"):
        if version == "final":
            return self.outputJsonHelper(path, self.finalBounds, self.finalTextBounds)

        print(f"Error: no output version {version}")
        exit(1)