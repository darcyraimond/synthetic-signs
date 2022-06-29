import numpy as np
import draw
from FontSelector import FontSelector
from NoiseGenerator import NoiseGenerator
import random


class NoStoppingGenerator:

    def __init__(self):

        # Define default parameters
        self.dimensions = [1000, 500]
        self.outerPad = 10
        self.outerRedStrip = 13
        self.whiteStrip = 10
        self.red = [45, 35, 185, 255]
        self.white = [215, 215, 215, 255]
        self.cornerRadius = 40
        self.titleStart = 80
        self.textSize = 90
        self.textSpacing = 1.3
        self.arrowStart = 860
        self.arrowThickness = 18
        self.arrowLength = 320
        self.numDilations = 1
        self.dilationP = 0.25
        self.wideNoise = 6
        self.colourNoise = 4
        self.narrowNoise = 5

        # Define maximum deviations
        self.outerRedStripDev = 5
        self.whiteStripDev = 3
        self.rrDev = 40
        self.rgDev = 15
        self.rbDev = 15
        self.wCommonDev = 25
        self.wEachDev = 15
        self.radDev = 10
        self.titleStartDev = 25
        self.textSizeDev = 15
        self.textSpacingDev = 0.3
        self.arrowStartDev = 45
        self.arrowThicknessDev = 7
        self.arrowLengthDev = 50
        self.numDilationsDev = 1
        self.dilationPDev = 0.15
        self.wideNoiseDev = 5
        self.colourNoiseDev = 3
        self.narrowNoiseDev = 4

        self.fontSelector = FontSelector()
        self.noiseGenerator = NoiseGenerator()

    def drawNoStoppingSignVertical(self):

        # Setup basic parameters
        dimensions = self.dimensions.copy()
        outerPad = self.outerPad
        outerRedStrip = self.outerRedStrip
        whiteStrip = self.whiteStrip
        red = self.red.copy()
        white = self.white.copy()
        cornerRadius = self.cornerRadius
        titleStart = self.titleStart
        textSize = self.textSize
        textSpacing = self.textSpacing
        arrowStart = self.arrowStart
        arrowThickness = self.arrowThickness
        arrowLength = self.arrowLength
        numDilations = self.numDilations
        dilationP = self.dilationP
        wideNoise = self.wideNoise
        colourNoise = self.colourNoise
        narrowNoise = self.narrowNoise

        # Add noise to parameters
        outerRedStrip += random.randrange(-self.outerRedStripDev, self.outerRedStripDev + 1)
        whiteStrip += random.randrange(-self.whiteStripDev, self.whiteStripDev + 1)
        red[0] += random.randrange(-self.rbDev, self.rbDev + 1)
        red[1] += random.randrange(-self.rgDev, self.rgDev + 1)
        red[2] += random.randrange(-self.rrDev, self.rrDev + 1)
        wAll = random.randrange(-self.wCommonDev, self.wCommonDev + 1)
        white[0] += wAll + random.randrange(-self.wEachDev, self.wEachDev + 1)
        white[1] += wAll + random.randrange(-self.wEachDev, self.wEachDev + 1)
        white[2] += wAll + random.randrange(-self.wEachDev, self.wEachDev + 1)
        cornerRadius += random.randrange(-self.radDev, self.radDev + 1)
        titleStart += random.randrange(-self.titleStartDev, self.titleStartDev + 1)
        textSize += random.randrange(-self.textSizeDev, self.textSizeDev + 1)
        textSpacing += random.uniform(-self.textSpacingDev, self.textSpacingDev)
        arrowStart += random.randrange(-self.arrowStartDev, self.arrowStartDev + 1)
        arrowThickness += random.randrange(-self.arrowThicknessDev, self.arrowThicknessDev + 1)
        arrowLength += random.randrange(-self.arrowLengthDev, self.arrowLengthDev + 1)
        numDilations += random.randrange(-self.numDilationsDev, self.numDilationsDev + 1)
        dilationP += random.uniform(-self.dilationPDev, self.dilationPDev)
        wideNoise += random.randrange(-self.wideNoiseDev, self.wideNoiseDev + 1)
        colourNoise += random.randrange(-self.colourNoiseDev, self.colourNoiseDev + 1)
        narrowNoise += random.randrange(-self.narrowNoiseDev, self.narrowNoiseDev + 1)

        # Create image
        sign = np.zeros((*dimensions, 4), dtype = np.uint8)
        draw.drawRoundedRectangle(
            sign, 
            tuple(red), 
            (outerPad, outerPad), 
            (dimensions[0] - outerPad, dimensions[1] - outerPad),
            cornerRadius
        )
        draw.drawRoundedRectangle(
            sign,
            tuple(white), 
            (outerPad + outerRedStrip, outerPad + outerRedStrip), 
            (dimensions[0] - outerPad - outerRedStrip, dimensions[1] - outerPad - outerRedStrip), 
            cornerRadius - outerRedStrip
        )
        draw.drawRoundedRectangle(
            sign, 
            tuple(red), 
            (outerPad + outerRedStrip + whiteStrip, outerPad + outerRedStrip + whiteStrip), 
            (dimensions[0] - outerPad - outerRedStrip - whiteStrip, dimensions[1] - outerPad - outerRedStrip - whiteStrip), 
            cornerRadius - outerRedStrip - whiteStrip
        )
        draw.drawTexts(
            sign, 
            ["NO", "STOPPING"], 
            (titleStart, dimensions[1] // 2), 
            c=tuple(white), 
            spacing=textSpacing,
            font=self.fontSelector.getRandomFont(size=textSize)
        )
        draw.drawArrow(
            sign, 
            (arrowStart, dimensions[1] // 2), 
            left=True, 
            right=True, 
            thickness=arrowThickness, 
            radius=arrowLength // 2, 
            c=tuple(white)
        )

        # Add dilation to image
        """p = 0.2
        for i in range(numDilations):
            if random.random() < 0.5:
                self.noiseGenerator.performDilation(sign, red, 1, p=p)
                self.noiseGenerator.performDilation(sign, white, 1, p=p)
            else:
                self.noiseGenerator.performDilation(sign, white, 1, )
                self.noiseGenerator.performDilation(sign, red, 1)"""
        

        # Add noise to image
        allChannelNoise = self.noiseGenerator.getNoiseArea(convSize = 75, maxDev = wideNoise)
        self.noiseGenerator.addNoiseToImage(sign, allChannelNoise, 0)
        self.noiseGenerator.addNoiseToImage(sign, allChannelNoise, 1)
        self.noiseGenerator.addNoiseToImage(sign, allChannelNoise, 2)

        channel0Noise = self.noiseGenerator.getNoiseArea(convSize = 75, maxDev = colourNoise)
        self.noiseGenerator.addNoiseToImage(sign, channel0Noise, 0)

        channel1Noise = self.noiseGenerator.getNoiseArea(convSize = 75, maxDev = colourNoise)
        self.noiseGenerator.addNoiseToImage(sign, channel1Noise, 1)

        channel2Noise = self.noiseGenerator.getNoiseArea(convSize = 75, maxDev = colourNoise)
        self.noiseGenerator.addNoiseToImage(sign, channel2Noise, 2)

        allChannelNoiseNarrow = self.noiseGenerator.getNoiseArea(convSize = 15, maxDev = narrowNoise)
        self.noiseGenerator.addNoiseToImage(sign, allChannelNoiseNarrow, 0)
        self.noiseGenerator.addNoiseToImage(sign, allChannelNoiseNarrow, 1)
        self.noiseGenerator.addNoiseToImage(sign, allChannelNoiseNarrow, 2)

        return sign