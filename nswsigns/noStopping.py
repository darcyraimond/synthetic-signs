import numpy as np
import draw
from FontSelector import FontSelector
from NoiseGenerator import NoiseGenerator
import random
from sign import Sign


class NoStoppingGenerator:

    def __init__(self):

        # Define default parameters
        self.dimensions = [1000, 500]
        self.outerPad = 10
        self.outerRedStrip = 13
        self.whiteStrip = 10
        self.red = [45, 35, 165, 255]
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
        self.wideNoise = 30
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
        self.rrDev = 60
        self.rgDev = 25
        self.rbDev = 25
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

    def drawRandom(self):

        # Only have vertical no stopping sign
        # Choose arrow directions
        arrows = random.choice([(True, True), (True, False), (False, True)])
        return self.drawNoStoppingSignVertical(arrows[0], arrows[1])


    def drawNoStoppingSignVertical(self, leftArrow, rightArrow):

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
        wideSize = self.wideSize
        narrowSize = self.narrowSize
        timeVGapPc = self.timeVGapPc
        timeHeight = self.timeHeight
        timeHGapPc = self.timeHGapPc
        timeDashWidthPc = self.timeDashWidthPc
        timeDashHeightPc = self.timeDashHeightPc

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
        wideSize += random.randrange(-self.wideSizeDev, self.wideSizeDev + 1)
        narrowSize += random.randrange(-self.narrowSizeDev, self.narrowSizeDev + 1)
        timeVGapPc += random.uniform(-self.timeVGapPcDev, self.timeVGapPcDev)
        timeHeight += random.randrange(-self.timeHeightDev, self.timeHeightDev + 1)
        timeHGapPc += random.uniform(-self.timeHGapPcDev, self.timeHGapPcDev)
        timeDashWidthPc += random.uniform(-self.timeDashWidthPcDev, self.timeDashWidthPcDev)
        timeDashHeightPc += random.uniform(-self.timeDashHeightPcDev, self.timeDashHeightPcDev)

        # Create image
        sign = Sign()

        sign.image = np.zeros((*dimensions, 4), dtype = np.uint8)
        draw.drawRoundedRectangle(
            sign, 
            tuple(red), 
            (outerPad, outerPad), 
            (dimensions[0] - outerPad, dimensions[1] - outerPad),
            cornerRadius,
            True
        )
        draw.drawRoundedRectangle(
            sign,
            tuple(white), 
            (outerPad + outerRedStrip, outerPad + outerRedStrip), 
            (dimensions[0] - outerPad - outerRedStrip, dimensions[1] - outerPad - outerRedStrip), 
            cornerRadius - outerRedStrip,
            False
        )
        draw.drawRoundedRectangle(
            sign, 
            tuple(red), 
            (outerPad + outerRedStrip + whiteStrip, outerPad + outerRedStrip + whiteStrip), 
            (dimensions[0] - outerPad - outerRedStrip - whiteStrip, dimensions[1] - outerPad - outerRedStrip - whiteStrip), 
            cornerRadius - outerRedStrip - whiteStrip,
            False
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
            left=leftArrow, 
            right=rightArrow, 
            thickness=arrowThickness, 
            radius=arrowLength // 2, 
            c=tuple(white)
        )
        draw.drawTimeLimit( # TODO: add randomness
            sign=sign,
            tc=(400, dimensions[1] // 2), 
            times=("1:00", "AM", "12:30", "PM"),
            days=("SAT-SUN &", "PUBLIC HOLIDAYS"),
            height=timeHeight,
            vgapPc=timeVGapPc,
            hgapPc=timeHGapPc,
            dashWidthPc=timeDashWidthPc,
            dashHeightPc=timeDashHeightPc,
            c=tuple(white),
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