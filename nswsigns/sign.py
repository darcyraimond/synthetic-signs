import draw
import random
import cv2
import numpy as np


def getTransformedPoint(pt, mat):
    pt = (pt[1], pt[0])
    px = (mat[0][0]*pt[0] + mat[0][1]*pt[1] + mat[0][2]) / (mat[2][0]*pt[0] + mat[2][1]*pt[1] + mat[2][2])
    py = (mat[1][0]*pt[0] + mat[1][1]*pt[1] + mat[1][2]) / (mat[2][0]*pt[0] + mat[2][1]*pt[1] + mat[2][2])
    return (py, px)


def pasteImage(background, sign, start=(0,0)):
    """for i, row in enumerate(sign):
        for j, cell in enumerate(row):
            if cell[3] == 0: continue
            for k in range(3):
                ratio = cell[3] / 255
                if ratio == 1:
                    background[i+start[0]][j+start[1]][k] = cell[k]
                else:
                    background[i+start[0]][j+start[1]][k] = int(round(float(cell[k]) * ratio + float(background[i+start[0]][j+start[1]][k]) * float((1 - ratio))))"""

    stack = np.stack([sign[:,:,3],sign[:,:,3],sign[:,:,3]], -1) / 255
    #signInverse = np.stack([sign[:,:,2],sign[:,:,1],sign[:,:,0]], -1)
    cv2.imwrite("test.png", sign)

    #print("Mean of this sign is", np.mean(signInverse))
    #print("Mean of this stack is", np.mean(stack))
    background[start[0]:start[0]+sign.shape[0], start[1]:start[1]+sign.shape[1]] = \
        background[start[0]:start[0]+sign.shape[0], start[1]:start[1]+sign.shape[1]] * (1 - stack) \
        + sign[:,:,0:3] * stack


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

    def addBackground(self, background):

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
