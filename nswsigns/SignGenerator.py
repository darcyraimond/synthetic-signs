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

    def get(self, arrows=None):

        # Generate random number
        rnd = random.uniform(0, self.wtCount)
        count = 0
        for gen, w in zip(self.generators, self.weights):
            count += w
            if rnd <= count:
                return gen.drawRandom(arrows=arrows)
            
        # If get here, failed.
        print("FATAL ERROR: did not select a random sign to generate, terminating.")
        exit(1)