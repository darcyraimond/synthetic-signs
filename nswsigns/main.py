from noStopping import NoStoppingGenerator
import cv2
import cProfile
import pstats
from ImageSelector import ImageSelector
import os
from integerParking import IntegerParkingGenerator
from SignGenerator import Generator


def main():

    #nsg = NoStoppingGenerator()
    #ipg = IntegerParkingGenerator()
    generator = Generator()
    generator.add(NoStoppingGenerator(), 1)
    generator.add(IntegerParkingGenerator(), 2)

    imageSelector = ImageSelector(source="sd")
    
    # Remove old directories
    os.system("rm -r image_data")
    os.system("rm -r gt_cavell")
    os.system("rm -r gt_emerald")

    # Create directories
    os.system("mkdir image_data")
    os.system("mkdir gt_cavell")
    os.system("mkdir gt_emerald")

    N = 1000
    for i in range(1, N+1):

        print(f"Generating image {i}...", end = "\r")
        sign = generator.get()
        sign.transform()
        sign.addBackground(imageSelector.getRandomImage())
        #cv2.imwrite(f"img{i}.png", sign.getFinal(withBounds=True, withTextBounds=True))
        #cv2.imwrite(f"img{i}.png", sign.getFinal())
        #cv2.imwrite(f"img{i}.png", sign.getImage(withBounds=True, withTextBounds=True))
        #cv2.imwrite(f"img{i}.png", sign.getImage())

        # Actual output
        if True:
            cv2.imwrite(f"image_data/img{i}.png", sign.getFinal())
            sign.outputJson(f"gt_cavell/gt{i}.json")
            sign.outputTxt(f"gt_emerald/gt{i}.txt")

#main()

cProfile.run("main()", "profile.txt")

p = pstats.Stats('profile.txt')
p.strip_dirs().sort_stats("tottime").print_stats(10)