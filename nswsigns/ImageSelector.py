import os
import cv2
import random

class ImageSelector:

    def __init__(self, source="hd"):

        if source == "hd": source = "nswsigns/DIV2K_train_HR"
        if source == "sd": source = "nswsigns/backgrounds"
        
        self.fileNames = []
        self.isLoaded = []
        self.images = []
        self.numImages = 0

        self.source = source

        for name in os.listdir(source):
            if name[-4:] != ".jpg" and name[-4:] != ".png": continue

            self.fileNames.append(name)
            self.isLoaded.append(False)
            self.images.append(None)
            self.numImages += 1

        #print("Number of candidate images:", self.numImages)

    def getRandomImage(self, minDims=(500,400)):

        index = random.randrange(0, self.numImages)
        
        if self.isLoaded[index]:
            return self.images[index]
        
        # Load image if we haven't already
        image = cv2.imread(f"{self.source}/{self.fileNames[index]}")
        self.images[index] = image
        self.isLoaded[index] = True

        # Try again if the image is too small
        if image.shape[0] < minDims[0] or image.shape[1] < minDims[1]:
            self.fileNames.pop(index)
            self.isLoaded.pop(index)
            self.images.pop(index)
            self.numImages -= 1
            return self.getRandomImage(minDims=minDims)

        return self.images[index].copy()
