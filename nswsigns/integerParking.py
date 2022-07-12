import numpy as np
import draw
from FontSelector import FontSelector
from NoiseGenerator import NoiseGenerator
import random
from sign import Sign
from timeLimitRandomiser import getRandomArgs


class IntegerParkingGenerator:

    def __init__(self):

        # Define default parameters
        self.dimensions = [1000, 500]
        self.outerPad = 10
        self.green = [35, 130, 20, 255]
        self.white = [200, 215, 220, 255]
        self.cornerRadius = 40
        self.titleStart = 80
        self.textSize = 250
        self.textSpacing = 1.1
        self.arrowStart = 860
        self.arrowThickness = 18
        self.arrowLength = 320
        #self.numDilations = 1
        #self.dilationP = 0.25
        self.wideNoise = 40
        self.colourNoise = 5
        self.narrowNoise = 20
        self.wideSize = 120
        self.narrowSize = 35
        self.timeVGapPc = 0.1
        self.timeHeight = 110
        self.timeHGapPc = 0.13
        self.timeDashWidthPc = 0.2
        self.timeDashHeightPc = 0.06

        # Define maximum deviations
        self.outerRedStripDev = 5
        self.whiteStripDev = 3
        self.grDev = 20
        self.ggDev = 50
        self.gbDev = 20
        self.wCommonDev = 25
        self.wEachDev = 15
        self.radDev = 10
        self.titleStartDev = 25
        self.textSizeDev = 50
        self.textSpacingDev = 0.1
        self.arrowStartDev = 45
        self.arrowThicknessDev = 7
        self.arrowLengthDev = 50
        self.numDilationsDev = 1
        self.dilationPDev = 0.15
        self.wideNoiseDev = 29
        self.colourNoiseDev = 4
        self.narrowNoiseDev = 19
        self.wideSizeDev = 80
        self.narrowSizeDev = 25
        self.timeVGapPcDev = 0.15
        self.timeHeightDev = 20
        self.timeHGapPcDev = 0.08
        self.timeDashWidthPcDev = 0.05
        self.timeDashHeightPcDev = 0.015
        

        self.fontSelector = FontSelector()
        self.noiseGenerator = NoiseGenerator()

    def drawRandom(self, arrows=None):

        # Only have vertical no stopping sign
        # Choose arrow directions
        if arrows is None: arrows = random.choice([(True, True), (True, False), (False, True)])
        return self.drawIntegerParkingSignVertical(arrows[0], arrows[1])


    def drawIntegerParkingSignVertical(self, leftArrow, rightArrow):

        # Setup basic parameters
        dimensions = self.dimensions.copy()
        outerPad = self.outerPad
        green = self.green.copy()
        white = self.white.copy()
        cornerRadius = self.cornerRadius
        titleStart = self.titleStart
        textSize = self.textSize
        textSpacing = self.textSpacing
        arrowStart = self.arrowStart
        arrowThickness = self.arrowThickness
        arrowLength = self.arrowLength
        #numDilations = self.numDilations
        #dilationP = self.dilationP
        wideNoise = self.wideNoise
        colourNoise = self.colourNoise
        narrowNoise = self.narrowNoise
        wideSize = self.wideSize
        narrowSize = self.narrowSize
        timeVGapPc = self.timeVGapPc
        timeHeight = self.timeHeight
        timeHGapPc = self.timeHGapPc
        timeDashWidthPc = self.timeDashWidthPc
        timeDashHeightPc = self.timeDashHeightPc

        # Add noise to parameters
        green[0] += random.randrange(-self.gbDev, self.gbDev + 1)
        green[1] += random.randrange(-self.ggDev, self.ggDev + 1)
        green[2] += random.randrange(-self.grDev, self.grDev + 1)
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
        #numDilations += random.randrange(-self.numDilationsDev, self.numDilationsDev + 1)
        #dilationP += random.uniform(-self.dilationPDev, self.dilationPDev)
        wideNoise += random.randrange(-self.wideNoiseDev, self.wideNoiseDev + 1)
        colourNoise += random.randrange(-self.colourNoiseDev, self.colourNoiseDev + 1)
        narrowNoise += random.randrange(-self.narrowNoiseDev, self.narrowNoiseDev + 1)
        wideSize += random.randrange(-self.wideSizeDev, self.wideSizeDev + 1)
        narrowSize += random.randrange(-self.narrowSizeDev, self.narrowSizeDev + 1)
        timeVGapPc += random.uniform(-self.timeVGapPcDev, self.timeVGapPcDev)
        timeHeight += random.randrange(-self.timeHeightDev, self.timeHeightDev + 1)
        timeHGapPc += random.uniform(-self.timeHGapPcDev, self.timeHGapPcDev)
        timeDashWidthPc += random.uniform(-self.timeDashWidthPcDev, self.timeDashWidthPcDev)
        timeDashHeightPc += random.uniform(-self.timeDashHeightPcDev, self.timeDashHeightPcDev)

        # Other random sign-specific data
        numHours = random.randrange(1, 10)

        # Create image
        sign = Sign()

        sign.image = np.zeros((*dimensions, 4), dtype = np.uint8)
        draw.drawRoundedRectangle(
            sign, 
            tuple(white), 
            (outerPad, outerPad), 
            (dimensions[0] - outerPad, dimensions[1] - outerPad),
            cornerRadius,
            True
        )
        draw.drawTexts(
            sign, 
            [f"{numHours}P"], 
            (titleStart, dimensions[1] // 2), 
            c=tuple(green), 
            spacing=textSpacing,
            font=self.fontSelector.getRandomFont(size=textSize)
        )
        draw.drawArrow(
            sign, 
            (arrowStart, dimensions[1] // 2), 
            left=leftArrow, 
            right=rightArrow, 
            thickness=arrowThickness, 
            radius=arrowLength // 2, 
            c=tuple(green)
        )

        # Do some calculations about how high/low times can be placed
        top = int(round(titleStart + textSpacing*textSize))
        bottom = int(round(arrowStart - arrowThickness - timeHeight * timeVGapPc))
        #print("Top:", top)
        #print("Bottom:", bottom)

        # Get arguments
        times = getRandomArgs(
            sign, 
            (top, dimensions[1] // 2),
            (bottom, dimensions[1] // 2),
            timeHeight,
            timeVGapPc,
            timeHGapPc,
            timeDashWidthPc,
            timeDashHeightPc,
            tuple(green),
            pEmpty=0.2,
            pNext=0.8,
            pSpecial=999,
            maxTimes=5
        )

        for time in times:
            draw.drawTimeLimit(*time)

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
        allChannelNoise = self.noiseGenerator.getNoiseArea(convSize = wideSize, maxDev = wideNoise)
        self.noiseGenerator.addNoiseToImage(sign.image, allChannelNoise, 0)
        self.noiseGenerator.addNoiseToImage(sign.image, allChannelNoise, 1)
        self.noiseGenerator.addNoiseToImage(sign.image, allChannelNoise, 2)

        channel0Noise = self.noiseGenerator.getNoiseArea(convSize = wideSize, maxDev = colourNoise)
        self.noiseGenerator.addNoiseToImage(sign.image, channel0Noise, 0)

        channel1Noise = self.noiseGenerator.getNoiseArea(convSize = wideSize, maxDev = colourNoise)
        self.noiseGenerator.addNoiseToImage(sign.image, channel1Noise, 1)

        channel2Noise = self.noiseGenerator.getNoiseArea(convSize = wideSize, maxDev = colourNoise)
        self.noiseGenerator.addNoiseToImage(sign.image, channel2Noise, 2)

        allChannelNoiseNarrow = self.noiseGenerator.getNoiseArea(convSize = narrowSize, maxDev = narrowNoise)
        self.noiseGenerator.addNoiseToImage(sign.image, allChannelNoiseNarrow, 0)
        self.noiseGenerator.addNoiseToImage(sign.image, allChannelNoiseNarrow, 1)
        self.noiseGenerator.addNoiseToImage(sign.image, allChannelNoiseNarrow, 2)

        return sign