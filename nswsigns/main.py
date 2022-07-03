from noStopping import NoStoppingGenerator
import cv2
import cProfile
import pstats
from ImageSelector import ImageSelector

def main():

    nsg = NoStoppingGenerator()
    imageSelector = ImageSelector()

    for i in range(10):
        print(f"Generating image {i}...", end = "\r")
        sign = nsg.drawRandom()
        sign.transform()
        sign.addBackground(imageSelector.getRandomImage())
        #cv2.imwrite(f"img{i}.png", sign.getFinal(withBounds=True, withTextBounds=True))
        cv2.imwrite(f"img{i}.png", sign.getFinal())
        #cv2.imwrite(f"img{i}.png", sign.getImage(withBounds=True, withTextBounds=True))
        #cv2.imwrite(f"img{i}.png", sign.getImage())

#main()

cProfile.run("main()", "profile.txt")

p = pstats.Stats('profile.txt')
p.strip_dirs().sort_stats("tottime").print_stats(10)