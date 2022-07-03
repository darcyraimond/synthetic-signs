from noStopping import NoStoppingGenerator
import cv2
import cProfile
import pstats
from ImageSelector import ImageSelector
import os

def main():

    nsg = NoStoppingGenerator()
    imageSelector = ImageSelector()
    
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
        sign = nsg.drawRandom()
        sign.transform()
        sign.addBackground(imageSelector.getRandomImage())
        #cv2.imwrite(f"img{i}.png", sign.getFinal(withBounds=True, withTextBounds=True))
        cv2.imwrite(f"image_data/img{i}.png", sign.getFinal())
        #cv2.imwrite(f"img{i}.png", sign.getImage(withBounds=True, withTextBounds=True))
        #cv2.imwrite(f"img{i}.png", sign.getImage())

        # Output ground truth files
        sign.outputJson(f"gt_cavell/gt{i}.json")
        sign.outputTxt(f"gt_emerald/gt{i}.txt")

main()

#cProfile.run("main()", "profile.txt")

#p = pstats.Stats('profile.txt')
#p.strip_dirs().sort_stats("tottime").print_stats(10)