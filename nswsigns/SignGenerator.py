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