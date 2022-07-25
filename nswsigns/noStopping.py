import numpy as np
import draw
from FontSelector import FontSelector
from NoiseGenerator import NoiseGenerator
import random
from sign import Sign
from timeLimitRandomiser import splitDTs, getDirectionalDTs

def rng(n, form=int):
    if form is int:
        return random.randrange(-n, n + 1)
    if form is float:
        return random.uniform(-n, n)
    raise Exception(f"No rng value for form {form}")


class NoStoppingGenerator:

    def __init__(self):

        self.hasHorizontal = True
        self.hasVertical = True

        self.typeID = "no stopping"

        self.fontSelector = FontSelector()
        self.noiseGenerator = NoiseGenerator()

    def getRandomParams(self, orientation=None):

        if orientation is None:
            orientation = "horizontal" if random.random() < 0.5 else "vertical"

        # Any required precalculations
        wCom = rng(25)
        if orientation == "vertical":
            leftArrow, rightArrow = random.choice([(True, True), (True, False), (False, True)])
        else:
            leftArrow, rightArrow = random.choice([(True, False), (False, True)])
        doDifferent = random.random() < 0.2

        # Parameter dictionary
        if orientation == "vertical":
            params = {
                "id": self.typeID,
                "is vertical": True,
                "is horizontal": False,
                "dimensions": (1000, 500),
                "text": ["NO", "STOPPING"],
                "outer pad": 10,
                "red strip": 13 + rng(5),
                "white strip": (10 + rng(3)) * (1 - doDifferent),            
                "red": (45 + rng(25), 35 + rng(25), 165 + rng(60), 255),
                "white": (215 + rng(15) + wCom, 215 + rng(15) + wCom, 215 + rng(15) + wCom, 255),
                "corner radius": 40 + rng(10),
                "title start": 80 + rng(25) - 25*doDifferent,
                "text size": 90 + rng(15),
                "text spacing": 1.3 + rng(0.3, float),
                "arrow start": 860 + rng(45) + 25*doDifferent,
                "arrow thickness": 18 + rng(7),
                "arrow length": 320 + rng(50) + 25*doDifferent,
                "wide noise magnitude": 30 + rng(29),
                "colour noise magnitude": 5 + rng(4),
                "narrow noise magnitude": 20 + rng(19),
                "wide noise width": 120 + rng(80),
                "narrow noise width": 35 + rng(25),
                "vertical time gap percentage": 0.1 + rng(0.15, float),
                "horizontal time gap percentage": 0.13 + rng(0.08, float),
                "time height": 110 + rng(20),
                "time dash width percentage": 0.2 + rng(0.05, float),
                "time dash height percentage": 0.06 + rng(0.015, float),
                "minimum time": random.randint(0, 2),
                "p no times": 0.4,
                "p next": 0.7,
                "max times": 5,
                "day height percentage": 0.35,
                "left arrow": leftArrow,
                "right arrow": rightArrow,
                "arrow centre": 250,
                "arrow head length": None # allow default
            }

            params["time top"] = int(round(params["title start"] + 2*params["text spacing"]*params["text size"])) - 25*(1 - doDifferent)
            params["time centre"] = params["dimensions"][1] // 2
            params["time bottom"] = int(round(params["arrow start"] - params["arrow thickness"] - params["time height"] * params["vertical time gap percentage"])) + 25*(1 - doDifferent)

        elif orientation == "horizontal":
            params = {
                "id": self.typeID,
                "is vertical": False,
                "is horizontal": True,
                "dimensions": (500, 1000),
                "text": ["NO STOPPING"],
                "outer pad": 10,
                "red strip": 13 + rng(5),
                "white strip": (10 + rng(3)) * doDifferent,            
                "red": (45 + rng(25), 35 + rng(25), 165 + rng(60), 255),
                "white": (215 + rng(15) + wCom, 215 + rng(15) + wCom, 215 + rng(15) + wCom, 255),
                "corner radius": 40 + rng(10),
                "title start": 40 + rng(15) + 25*(1 - doDifferent),
                "text size": 110 + rng(15),
                "text spacing": 1.1 + rng(0.15, float),
                "arrow start": 400 + rng(35) - 25*(1 - doDifferent),
                "arrow thickness": 18 + rng(7),
                "arrow length": 85 + rng(30),
                "wide noise magnitude": 30 + rng(29),
                "colour noise magnitude": 5 + rng(4),
                "narrow noise magnitude": 20 + rng(19),
                "wide noise width": 120 + rng(80),
                "narrow noise width": 35 + rng(25),
                "vertical time gap percentage": 0.05 + rng(0.1, float),
                "horizontal time gap percentage": 0.13 + rng(0.08, float),
                "time height": 90 + rng(20),
                "time dash width percentage": 0.2 + rng(0.05, float),
                "time dash height percentage": 0.06 + rng(0.015, float),
                "minimum time": random.randint(0, 2),
                "p no times": 0.4,
                "p next": 0.7,
                "max times": 5,
                "day height percentage": 0.35,
                "left arrow": leftArrow,
                "right arrow": rightArrow,
                "arrow centre": 500 + (350 + rng(50)) * (rightArrow - leftArrow),
                "arrow head length": 35 + rng(10)

            }

            params["time top"] = int(round(params["title start"] + params["text spacing"]*params["text size"])) + 25*doDifferent
            params["time centre"] = params["dimensions"][1] // 2
            params["time bottom"] = int(round(500 -  params["time height"] * 0.2)) - 25*doDifferent

        else:
            raise Exception(f"{orientation} is an invalid orientation.")
        return params

    def drawBasics(self, params, sign):

        # Create image
        sign.image = np.zeros((*params["dimensions"], 4), dtype = np.uint8)
        draw.drawRoundedRectangle(
            sign, 
            tuple(params["red"]), 
            (params["outer pad"], params["outer pad"]), 
            (params["dimensions"][0] - params["outer pad"], params["dimensions"][1] - params["outer pad"]),
            params["corner radius"],
            True
        )
        draw.drawRoundedRectangle(
            sign,
            tuple(params["white"]), 
            (params["outer pad"] + params["red strip"], params["outer pad"] + params["red strip"]), 
            (params["dimensions"][0] - params["outer pad"] - params["red strip"], params["dimensions"][1] - params["outer pad"] - params["red strip"]), 
            params["corner radius"] - params["red strip"],
            False
        )
        draw.drawRoundedRectangle(
            sign, 
            tuple(params["red"]), 
            (params["outer pad"] + params["red strip"] + params["white strip"], params["outer pad"] + params["red strip"] + params["white strip"]), 
            (params["dimensions"][0] - params["outer pad"] - params["red strip"] - params["white strip"], params["dimensions"][1] - params["outer pad"] - params["red strip"] - params["white strip"]), 
            params["corner radius"] - params["red strip"] - params["white strip"],
            False
        )
        draw.drawTexts(
            sign, 
            params["text"], 
            (params["title start"], params["dimensions"][1] // 2), 
            c=tuple(params["white"]), 
            spacing=params["text spacing"],
            font=self.fontSelector.getRandomFont(size=params["text size"])
        )
        draw.drawArrow(
            sign, 
            (params["arrow start"], params["arrow centre"]), 
            left=params["left arrow"], 
            right=params["right arrow"], 
            thickness=params["arrow thickness"], 
            radius=params["arrow length"] // 2, 
            c=tuple(params["white"]),
            headLen=params["arrow head length"],
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
                params["white"]
            )

    def drawNoise(self, params, sign: Sign):

        allChannelNoise = self.noiseGenerator.getNoiseArea(dim = params["dimensions"], convSize = params["wide noise width"], maxDev = params["wide noise magnitude"])
        self.noiseGenerator.addNoiseToImage(sign.image, allChannelNoise, 0)
        self.noiseGenerator.addNoiseToImage(sign.image, allChannelNoise, 1)
        self.noiseGenerator.addNoiseToImage(sign.image, allChannelNoise, 2)

        channel0Noise = self.noiseGenerator.getNoiseArea(dim = params["dimensions"], convSize = params["wide noise width"], maxDev = params["colour noise magnitude"])
        self.noiseGenerator.addNoiseToImage(sign.image, channel0Noise, 0)

        channel1Noise = self.noiseGenerator.getNoiseArea(dim = params["dimensions"], convSize = params["wide noise width"], maxDev = params["colour noise magnitude"])
        self.noiseGenerator.addNoiseToImage(sign.image, channel1Noise, 1)

        channel2Noise = self.noiseGenerator.getNoiseArea(dim = params["dimensions"], convSize = params["wide noise width"], maxDev = params["colour noise magnitude"])
        self.noiseGenerator.addNoiseToImage(sign.image, channel2Noise, 2)

        allChannelNoiseNarrow = self.noiseGenerator.getNoiseArea(dim = params["dimensions"], convSize = params["narrow noise width"], maxDev = params["narrow noise magnitude"])
        self.noiseGenerator.addNoiseToImage(sign.image, allChannelNoiseNarrow, 0)
        self.noiseGenerator.addNoiseToImage(sign.image, allChannelNoiseNarrow, 1)
        self.noiseGenerator.addNoiseToImage(sign.image, allChannelNoiseNarrow, 2)


    def drawRandom(self, arrows=None, orientation=None, params=None, times=None):

        if params is None: params = self.getRandomParams()
        if type(arrows) is tuple:
            params["left arrow"] = arrows[0]
            params["right arrow"] = arrows[1]
        if type(arrows) is str:
            params["left arrow"] = arrows == "left" or arrows == "both"
            params["right arrow"] = arrows == "right" or arrows == "both"

        if orientation is None:
            if params["is horizontal"]: orientation = "horizontal"
            if params["is vertical"]: orientation = "vertical"
    
        if orientation is None:
            return self.drawNoStoppingSignVertical(params, times)
        if orientation == "vertical":
            return self.drawNoStoppingSignVertical(params, times)
        if orientation == "horizontal":
            return self.drawNoStoppingSignHorizontal(params, times)
            #raise Exception("Error: unable to generate horizontal no stopping sign. Aborting.")
        
        raise Exception(f"Error: {orientation} is not a valid orientation for no stopping signs. Aborting.")


    def drawNoStoppingSignVertical(self, params, times=None):

        sign = Sign(self, params)
        self.drawBasics(params, sign)

        if times is None:
            times = getDirectionalDTs([params], [True], [True])
            self.drawTimes(params, sign, times[0])
        else:
            self.drawTimes(params, sign, times)

        # Add noise to image
        self.drawNoise(params, sign)

        return sign

    
    def drawNoStoppingSignHorizontal(self, params, times=None):

        sign = Sign(self, params)
        self.drawBasics(params, sign)

        if times is None:
            times = getDirectionalDTs([params], [True], [True])
            self.drawTimes(params, sign, times[0])
        else:
            self.drawTimes(params, sign, times)

        # Add noise to image
        self.drawNoise(params, sign)

        return sign