import draw
import random
import cv2
import numpy as np
import json


def getTransformedPoint(pt, mat):
    pt = (pt[1], pt[0])
    px = (mat[0][0]*pt[0] + mat[0][1]*pt[1] + mat[0][2]) / (mat[2][0]*pt[0] + mat[2][1]*pt[1] + mat[2][2])
    py = (mat[1][0]*pt[0] + mat[1][1]*pt[1] + mat[1][2]) / (mat[2][0]*pt[0] + mat[2][1]*pt[1] + mat[2][2])
    return (py, px)


def pasteImage(background, sign, start=(0,0)):
    stack = np.stack([sign[:,:,3],sign[:,:,3],sign[:,:,3]], -1) / 255
    tmp = np.array(background[start[0]:start[0]+sign.shape[0], start[1]:start[1]+sign.shape[1]], dtype = float)
    signTemp = np.array(sign[:,:,0:3], dtype = float)
    tmp = np.array(tmp * (1 - stack) + signTemp * stack, dtype = np.uint8)
    background[start[0]:start[0]+sign.shape[0], start[1]:start[1]+sign.shape[1]] = tmp


class Sign:
    
    def __init__(self):
        
        self.image = None
        self.transformed = None
        self.final = None

        # Ground truths
        self.bounds = None
        self.textBounds = []
        self.hasLeftArrow = None
        self.hasRightArrow = None

        # Dimension transform information
        self.transformMatrix = None
        self.transformBounds = None
        self.transformTextBounds = []

        self.finalBounds = None
        self.finalTextBounds = []


    def getImage(self, withBounds=False, withTextBounds=False, thickBounds=True, thickTextBounds=False):
        img = self.image.copy()

        if withBounds:
            #print(self.bounds)
            for i in range(len(self.bounds)):
                draw.drawLine(img, self.bounds[i-1], self.bounds[i], (255, 200, 0, 255), thickBounds)

        if withTextBounds:
            for bbox in self.textBounds:
                for i in range(len(bbox[0])):
                    draw.drawLine(img, bbox[0][i-1], bbox[0][i], (0, 200, 255, 255), thickTextBounds)

        return img

    
    def getTransformed(self, withBounds=False, withTextBounds=False, thickBounds=True, thickTextBounds=False):
        img = self.transformed.copy()

        if withBounds:
            for i in range(len(self.transformBounds)):
                draw.drawLine(img, self.transformBounds[i-1], self.transformBounds[i], (255, 200, 0, 255), thickBounds)

        if withTextBounds:
            for bbox in self.transformTextBounds:
                for i in range(len(bbox[0])):
                    draw.drawLine(img, bbox[0][i-1], bbox[0][i], (0, 200, 255, 255), thickTextBounds)

        return img

    
    def getFinal(self, withBounds=False, withTextBounds=False, thickBounds=True, thickTextBounds=False):
        img = self.final.copy()

        if withBounds:
            for i in range(len(self.finalBounds)):
                draw.drawLine(img, self.finalBounds[i-1], self.finalBounds[i], (255, 200, 0), thickBounds)

        if withTextBounds:
            for bbox in self.finalTextBounds:
                for i in range(len(bbox[0])):
                    draw.drawLine(img, bbox[0][i-1], bbox[0][i], (0, 200, 255), thickTextBounds)

        return img


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

        # Transform bounding box coordinates TODO: check with Cavell about bounding boxes
        self.transformBounds = []
        for pt in self.bounds:
            self.transformBounds.append(getTransformedPoint(pt, self.transformMatrix))

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
        for pt in self.transformBounds:
            self.finalBounds.append((pt[0] * ratio + randx, pt[1] * ratio + randy))

        # Transform text bounding box coordinates
        for textTuple in self.transformTextBounds:
            coords = []
            for pt in textTuple[0]:
                coords.append((pt[0] * ratio + randx, pt[1] * ratio + randy))
            self.finalTextBounds.append((coords, textTuple[1]))

    def fullString(self):
        out = ""
        for bbox in self.finalTextBounds:
            if bbox[1] in ["00", "15", "30", "45"]:
                out += ":" + bbox[1]
            elif out == "":
                out += bbox[1]
            else:
                out += " " + bbox[1]
        return out

    def outputJsonHelper(self, path, signBounds, textBounds):

        out = []
        if signBounds != []:
            # Get full sign bounds
            fullCoordinates = [
                int(round(signBounds[0][1])),
                int(round(signBounds[0][0])),
                int(round(signBounds[3][1])),
                int(round(signBounds[3][0])),
                int(round(signBounds[2][1])),
                int(round(signBounds[2][0])),
                int(round(signBounds[1][1])),
                int(round(signBounds[1][0]))
            ]
            fullD = {
                "Coordinates": fullCoordinates,
                "Text": self.fullString()
            }
            out.append(fullD)

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

