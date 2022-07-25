from noStopping import NoStoppingGenerator
import cv2
import cProfile
import pstats
from ImageSelector import ImageSelector
import os
from integerParking import IntegerParkingGenerator
from SignGenerator import Generator
from MultiSign import MultiSign
import random


def main():

    #random.seed(1)

    #nsg = NoStoppingGenerator()
    #ipg = IntegerParkingGenerator()
    generator = Generator()
    generator.add(NoStoppingGenerator(), 1)
    generator.add(IntegerParkingGenerator(), 2)

    imageSelector = ImageSelector(source="hd")
    
    # Remove old directories
    os.system("rm -r image_data")
    os.system("rm -r gt_cavell")
    os.system("rm -r gt_emerald")

    # Create directories
    os.system("mkdir image_data")
    os.system("mkdir gt_cavell")
    os.system("mkdir gt_emerald")

    N = 300
    for i in range(1, N+1):

        print(f"              Generating image {i}...", end = "\r")

        # Actual output
        if True:
            multiP = 0.6
            if random.random() < multiP:
                multi = MultiSign(generator)
                multi.transform()
                multi.addBackground(imageSelector.getRandomImage())
                cv2.imwrite(f"image_data/img{i}.png", multi.getFinal(withBounds=False, withTextBounds=False))
                #cv2.imwrite(f"img{i}.png", multi.getFinal(withBounds=True, withTextBounds=True))
                multi.outputTxt(f"gt_emerald/gt{i}.txt")
                multi.outputJson(f"gt_cavell/gt{i}.json")
            else:
                sign = generator.get()
                sign.transform()
                sign.addBackground(imageSelector.getRandomImage())
                cv2.imwrite(f"image_data/img{i}.png", sign.getFinal())
                #cv2.imwrite(f"img{i}.png", sign.getFinal(withBounds=True, withTextBounds=True))
                sign.outputJson(f"gt_cavell/gt{i}.json")
                sign.outputTxt(f"gt_emerald/gt{i}.txt")

        # Single sign
        if False:
            sign = generator.get()
            sign.transform()
            sign.addBackground(imageSelector.getRandomImage())
            cv2.imwrite(f"img{i}.png", sign.getFinal())

        # Emerald data
        if False:
            sign = generator.get()
            cv2.imwrite(f"image_data/img{i}.png", sign.getImage())
            sign.outputTxt(f"gt_emerald/gt{i}.txt", version="raw")

        # Multi sign
        if False:
            multi = MultiSign(generator)
            multi.transform()
            multi.addBackground(imageSelector.getRandomImage())
            #cv2.imwrite(f"img{i}.png", multi.getImage(withBounds=True, withTextBounds=True))
            #cv2.imwrite(f"img{i}.png", multi.getTransformed(withBounds=True, withTextBounds=True))
            cv2.imwrite(f"image_data/img{i}.png", multi.getFinal(withBounds=False, withTextBounds=False))
            cv2.imwrite(f"img{i}.png", multi.getFinal(withBounds=True, withTextBounds=True))
            multi.outputTxt(f"gt_emerald/gt{i}.txt")
            multi.outputJson(f"gt_cavell/gt{i}.json")


if True:
    main()
else:

    cProfile.run("main()", "profile")

    p = pstats.Stats('profile')
    p.strip_dirs().sort_stats("tottime").print_stats(5)
    p.strip_dirs().sort_stats("ncalls").print_stats(5)

print("\033[KSuccess!")