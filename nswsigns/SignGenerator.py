import random

class Generator:

    def __init__(self):
        self.generators = []
        self.weights = []
        self.wtCount = 0

    def add(self, generator, weight):
        self.generators.append(generator)
        self.weights.append(weight)
        self.wtCount += weight

    def genFromParams(self, params, times):
        for gen in self.generators:
            if gen.typeID == params["id"]:
                return gen.drawRandom(params=params, times=times)
        
        raise Exception(f"Could not find valid generator ID, params[\"id\"] = {params['id']}")

    def getParams(self, arrows=None, orientation=None):
        # Generate random number
        rnd = random.uniform(0, self.wtCount)
        #print(rnd)
        #print(rnd, self.wtCount)
        count = 0
        for gen, w in zip(self.generators, self.weights):
            count += w
            #print(rnd, count, gen.typeID, orientation)
            if rnd <= count:
                if orientation is None:
                    params = gen.getRandomParams(arrows)
                elif orientation == "horizontal":
                    #print(gen.typeID)
                    if gen.hasHorizontal: params = gen.getRandomParams(orientation=orientation)
                    else: return self.getParams(arrows, orientation)
                elif orientation == "vertical":
                    if gen.hasVertical: params = gen.getRandomParams(orientation=orientation)
                    else: return self.getParams(arrows, orientation)

                    #print(gen.typeID, params["id"])

                break

        # Edit based in inputs TODO: horizontal signs
        if type(arrows) is tuple:
            params["left arrow"] = arrows[0]
            params["right arrow"] = arrows[1]
        if type(arrows) is str:
            params["left arrow"] = arrows == "left" or arrows == "both"
            params["right arrow"] = arrows == "right" or arrows == "both"

        #print(params["id"])

        return params

    def get(self, arrows=None, orientation=None):

        # Generate random number
        rnd = random.uniform(0, self.wtCount)
        count = 0
        for gen, w in zip(self.generators, self.weights):
            count += w
            if rnd <= count:
                if orientation is None:
                    return gen.drawRandom(arrows)
                elif orientation == "horizontal":
                    if gen.hasHorizontal: return gen.drawRandom(arrows, orientation)
                    else: return self.get(arrows, orientation)
                elif orientation == "vertical":
                    if gen.hasVertical: return gen.drawRandom(arrows, orientation)
                    else: return self.get(arrows, orientation)
            
        # If get here, failed.
        raise Exception(f"Could not find a random sign to generate for orientation \"{orientation}\"")