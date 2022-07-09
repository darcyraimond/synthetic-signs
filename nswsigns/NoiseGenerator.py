import numpy as np
from scipy.signal import fftconvolve, convolve2d
import random
from scipy.ndimage import uniform_filter

class NoiseGenerator:

    def __init__(self):

        self.maxDev = 10

    def getNoiseArea(self, dim=[1000, 500], convSize=11, numConv=3, maxDev=None):
        
        if maxDev is None: maxDev = self.maxDev

        # Create noise
        area = np.random.random((dim[0] * 2, dim[1] * 2))

        for _ in range(numConv):
            area = uniform_filter(area, convSize)

        # Transform into required range
        area = area - np.min(area)
        area *= maxDev * 2 / np.max(area)
        area -= maxDev

        return np.array(area[dim[0]//2:dim[0]//2 + dim[0], dim[1]//2:dim[1]//2 + dim[1]], dtype = int)

    def addNoiseToImage(self, img, noise, channel):

        tmp = np.array(img, dtype = int)
        tmp[:,:,channel] += noise
        tmp[:,:,channel] = np.clip(tmp[:,:,channel], 0, 255)
        tmp = np.array(tmp, np.uint8)
        img[:,:,:] = tmp[:,:,:]



    def performDilation(self, img, colour, channel, p=0.5):
        ref = img.copy()
        for i, row in enumerate(img):
            for j, cell in enumerate(row):

                # Exit if requirements not met
                if cell[3] == 0: continue
                if cell[channel] == colour[channel]: continue

                # Check how many adjacent cells are the required colour
                num = (ref[i-1][j][channel] == colour[channel]) + (ref[i+1][j][channel] == colour[channel]) + (ref[i][j-1][channel] == colour[channel]) + (ref[i][j+1][channel] == colour[channel])
                prob = num / 4 * p
                if prob == 0: continue

                # Change colour probabilistically
                if random.random() < prob:
                    for k in range(4):
                        cell[k] = colour[k]

