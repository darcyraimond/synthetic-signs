from noStopping import NoStoppingGenerator
import cv2
import cProfile
import pstats
from ImageSelector import ImageSelector
import os
from integerParking import IntegerParkingGenerator
from SignGenerator import Generator
from MultiSign import MultiSign


def main():

    #nsg = NoStoppingGenerator()
    #ipg = IntegerParkingGenerator()
    generator = Generator()
    generator.add(NoStoppingGenerator(), 1)
    generator.add(IntegerParkingGenerator(), 2)

    # Multisign testing
    """multi = MultiSign(generator)
    print(multi.pattern)
    cv2.imwrite("test.png", multi.image)

    exit(1)"""

    imageSelector = ImageSelector(source="hd")
    
    # Remove old directories
    os.system("rm -r image_data")
    os.system("rm -r gt_cavell")
    os.system("rm -r gt_emerald")

    # Create directories
    os.system("mkdir image_data")
    os.system("mkdir gt_cavell")
    os.system("mkdir gt_emerald")

    N = 10
    for i in range(1, N+1):

        print(f"Generating image {i}...", end = "\r")
        #cv2.imwrite(f"img{i}.png", sign.getFinal(withBounds=True, withTextBounds=True))
        #cv2.imwrite(f"img{i}.png", sign.getFinal())
        #cv2.imwrite(f"img{i}.png", sign.getImage(withBounds=True, withTextBounds=True))
        #cv2.imwrite(f"img{i}.png", sign.getImage())

        # Actual output
        if False:
            sign = generator.get()
            sign.transform()
            sign.addBackground(imageSelector.getRandomImage())
            cv2.imwrite(f"image_data/img{i}.png", sign.getFinal())
            sign.outputJson(f"gt_cavell/gt{i}.json")
            sign.outputTxt(f"gt_emerald/gt{i}.txt")

        # Emerald data
        if False:
            sign = generator.get()
            cv2.imwrite(f"image_data/img{i}.png", sign.getImage())
            sign.outputTxt(f"gt_emerald/gt{i}.txt", version="raw")

        # Multi sign
        if True:
            multi = MultiSign(generator)
            cv2.imwrite(f"img{i}.png", multi.getImage(withBounds=False, withTextBounds=False))


if True:
    main()
else:

    cProfile.run("main()", "profile.txt")

    p = pstats.Stats('profile.txt')
    p.strip_dirs().sort_stats("tottime").print_stats(10)