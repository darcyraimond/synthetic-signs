import numpy as np
import draw
from FontSelector import FontSelector
from NoiseGenerator import NoiseGenerator
import random
from sign import Sign
from timeLimitRandomiser import getDTs, splitDTs


def rng(n, form=int):
    if form is int:
        return random.randrange(-n, n + 1)
    if form is float:
        return random.uniform(-n, n)
    raise Exception(f"No rng value for form {form}")

class IntegerParkingGenerator:

    def __init__(self):

        self.hasHorizontal = False
        self.hasVertical = True

        self.fontSelector = FontSelector()
        self.noiseGenerator = NoiseGenerator()

    def getRandomParams(self):

        # Any required precalculations
        wCom = rng(25)
        hours = random.randint(1, 9)

        # Parameter dictionary
        params = {
            "is vertical": True,
            "is horizontal": False,
            "dimensions": (1000, 500),
            "outer pad": 10,
            "green": (35 + rng(10), 130 + rng(50), 20 + rng(20), 255),
            "white": (210 + rng(15) + wCom, 210 + rng(15) + wCom, 210 + rng(15) + wCom, 255),
            "corner radius": 40 + rng(10),
            "title start": 80 + rng(25),
            "text size": 250 + rng(50),
            "text spacing": 1.1 + rng(0.1, float),
            "arrow start": 860 + rng(45),
            "arrow thickness": 18 + rng(7),
            "arrow length": 320 + rng(50),
            "wide noise magnitude": 40 + rng(29),
            "colour noise magnitude": 5 + rng(4),
            "narrow noise magnitude": 20 + rng(19),
            "wide noise width": 120 + rng(80),
            "narrow noise width": 35 + rng(25),
            "vertical time gap percentage": 0.1 + rng(0.15, float),
            "horizontal time gap percentage": 0.13 + rng(0.08, float),
            "time height": 110 + rng(20),
            "time dash width percentage": 0.2 + rng(0.05, float),
            "time dash height percentage": 0.06 + rng(0.015, float),
            "minimum time": 0,
            "p no times": 0,
            "p next": 1,
            "max times": 5,
            "day height percentage": 0.35,
            "number of hours": hours
        }
        
        return params

    def drawBasics(self, arrows, params, sign):

        leftArrow, rightArrow = arrows

        sign.image = np.zeros((*params["dimensions"], 4), dtype = np.uint8)
        draw.drawRoundedRectangle(
            sign, 
            tuple(params["white"]), 
            (params["outer pad"], params["outer pad"]), 
            (params["dimensions"][0] - params["outer pad"], params["dimensions"][1] - params["outer pad"]),
            params["corner radius"],
            True
        )
        numHours = params["number of hours"] # TODO update
        draw.drawTexts(
            sign, 
            [f"{numHours}P"], 
            (params["title start"], params["dimensions"][1] // 2), 
            c=tuple(params["green"]), 
            spacing=params["text spacing"],
            font=self.fontSelector.getRandomFont(size=params["text size"])
        )
        draw.drawArrow(
            sign, 
            (params["arrow start"], params["dimensions"][1] // 2), 
            left=leftArrow, 
            right=rightArrow, 
            thickness=params["arrow thickness"], 
            radius=params["arrow length"] // 2, 
            c=tuple(params["green"])
        )

    def drawTimes(self, params, sign: Sign, timeList):

        for dt, tc in timeList:
            days, times = splitDTs(dt)
            draw.drawTimeLimit(
                sign, 
                tc, 
                times, 
                days,
                params["time height"],
                params["vertical time gap percentage"],
                params["horizontal time gap percentage"],
                params["time dash width percentage"],
                params["time dash height percentage"],
                params["green"]
            )

    def drawNoise(self, params, sign: Sign):

        allChannelNoise = self.noiseGenerator.getNoiseArea(convSize = params["wide noise width"], maxDev = params["wide noise magnitude"])
        self.noiseGenerator.addNoiseToImage(sign.image, allChannelNoise, 0)
        self.noiseGenerator.addNoiseToImage(sign.image, allChannelNoise, 1)
        self.noiseGenerator.addNoiseToImage(sign.image, allChannelNoise, 2)

        channel0Noise = self.noiseGenerator.getNoiseArea(convSize = params["wide noise width"], maxDev = params["colour noise magnitude"])
        self.noiseGenerator.addNoiseToImage(sign.image, channel0Noise, 0)

        channel1Noise = self.noiseGenerator.getNoiseArea(convSize = params["wide noise width"], maxDev = params["colour noise magnitude"])
        self.noiseGenerator.addNoiseToImage(sign.image, channel1Noise, 1)

        channel2Noise = self.noiseGenerator.getNoiseArea(convSize = params["wide noise width"], maxDev = params["colour noise magnitude"])
        self.noiseGenerator.addNoiseToImage(sign.image, channel2Noise, 2)

        allChannelNoiseNarrow = self.noiseGenerator.getNoiseArea(convSize = params["narrow noise width"], maxDev = params["narrow noise magnitude"])
        self.noiseGenerator.addNoiseToImage(sign.image, allChannelNoiseNarrow, 0)
        self.noiseGenerator.addNoiseToImage(sign.image, allChannelNoiseNarrow, 1)
        self.noiseGenerator.addNoiseToImage(sign.image, allChannelNoiseNarrow, 2)

    def drawRandom(self, arrows=None, orientation=None, params=None):

        if arrows is None:
            arrows = random.choice([(True, True), (True, False), (False, True)])
        elif arrows == "left":
            arrows = (True, False)
        elif arrows == "right":
            arrows = (False, True)
        elif arrows == "both":
            arrows = (True, True)

        if params is None: params = self.getRandomParams()
            
        if orientation is None:
            return self.drawIntegerParkingSignVertical(arrows, params)
        if orientation == "vertical":
            return self.drawIntegerParkingSignVertical(arrows, params)
        if orientation == "horizontal":
            print("Error: upable to generate horizontal integer parking sign. Aborting.")
            exit(1)
        
        print(f"Error: {orientation} is not a valid orientation for integer parking signs. Aborting.")
        exit(1)


    def drawIntegerParkingSignVertical(self, arrows, params):

        sign = Sign()
        self.drawBasics(arrows, params, sign)

        params["time top"] = int(round(params["title start"] + params["text spacing"]*params["text size"]))
        params["time centre"] = params["dimensions"][1] // 2
        params["time bottom"] = int(round(params["arrow start"] - params["arrow thickness"] - params["time height"] * params["vertical time gap percentage"]))
        times = getDTs([params])
        self.drawTimes(params, sign, times[0])

        # Add noise to image
        self.drawNoise(params, sign)

        return sign