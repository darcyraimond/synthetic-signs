import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw

def drawRectangle(img, c, tl, br):

    # Add alpha if not provided
    if len(c) == 3: c = [c[0], c[1], c[2], 255]

    for i in range(tl[0], br[0] + 1):
        for j in range(tl[1], br[1] + 1):
            for k in range(4):
                img[i][j][k] = c[k]


def drawCircle(img, c, centre, radius):

    if len(c) == 3: c = [c[0], c[1], c[2], 255]
    for i in range(centre[0] - radius, centre[0] + radius + 1):
        for j in range(centre[1] - radius, centre[1] + radius + 1):

            if np.sqrt((centre[0] - i)**2 + (centre[1] - j)**2) > radius: continue

            img[i][j][0] = c[0]
            img[i][j][1] = c[1]
            img[i][j][2] = c[2]
            img[i][j][3] = c[3]


def drawRoundedRectangle(img, c, tl, br, roundRadius):

    if len(c) == 3: c = [c[0], c[1], c[2], 255]

    # Draw circles
    drawCircle(img, c, (tl[0] + roundRadius, tl[1] + roundRadius), roundRadius)
    drawCircle(img, c, (tl[0] + roundRadius, br[1] - roundRadius), roundRadius)
    drawCircle(img, c, (br[0] - roundRadius, tl[1] + roundRadius), roundRadius)
    drawCircle(img, c, (br[0] - roundRadius, br[1] - roundRadius), roundRadius)

    # Draw rectangles
    drawRectangle(img, c, (tl[0] + roundRadius, tl[1]), (br[0] - roundRadius, br[1]))
    drawRectangle(img, c, (tl[0], tl[1] + roundRadius), (tl[0] + roundRadius, br[1] - roundRadius))
    drawRectangle(img, c, (br[0] - roundRadius, tl[1] + roundRadius), (br[0], br[1] - roundRadius))


def textDims(text_string, font_size, font=None):
    # https://stackoverflow.com/a/46220683/9263761
    if font is None: 
        font = ImageFont.truetype("nswsigns/fonts/UniversCondensed.ttf", font_size)
    _, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_height, text_width)


def drawText(img, text, tc, size=50, c = (128, 128, 128, 255), font=None):

    # Get dimensions and find top left
    if font is None: 
        font = ImageFont.truetype("nswsigns/fonts/UniversCondensed.ttf", size)
    dims = textDims(text, size, font)
    tl = (tc[0], tc[1] - dims[1] // 2)

    # Draw text in location
    pilFrame = Image.fromarray(np.array(img, dtype = np.uint8))
    editable = ImageDraw.Draw(pilFrame)
    editable.text(tl[::-1], text, c, font = font)
    imgPIL = np.array(pilFrame)
    img *= 0
    img += imgPIL


def drawTexts(img, texts, tc, size=50, c = (128, 128, 128, 255), font=None, spacing=1.5):
    
    # Get height
    if font is None: 
        font = ImageFont.truetype("nswsigns/fonts/UniversCondensed.ttf", size)
    height = textDims(texts[0], size, font)[0]

    # Draw each line
    for i, text in enumerate(texts):
        drawText(img, text, (tc[0] + i * int(height * spacing), tc[1]), c=c, font=font, size=size)


def drawTriangle(img, tl, length, thickness, isLeft=True, c=(255,255,255,255)):

    for i in range(thickness):
        for j in range(length):
            
            # Continue if condition not met
            if isLeft:
                pcThickness = (i - thickness / 2) / (thickness / 2)
                pcLength = (j + 1) / length
            else:
                pcThickness = (i - thickness / 2) / (thickness / 2)
                pcLength = 1 - (j + 1) / length

            if abs(pcLength) < abs(pcThickness): continue

            for k in range(4):
                img[tl[0]+i][tl[1]+j][k] = c[k]



def drawArrow(img, tc, radius=150, thickness=10, left=False, right=False, headLen=None, headWidth=None, c=(255,255,255,255)):

    # Set defaults of 3x width, 15% length for heads
    if headLen is None: headLen = int(radius * 2 * 0.15)
    if headWidth is None: headWidth = 3 * thickness

    # Draw the main rectangle
    drawRectangle(img, c, (tc[0], tc[1] - radius + headLen), (tc[0] + thickness - 1, tc[1] + radius - headLen))

    # Draw arrow heads
    if left:
        drawTriangle(img, (tc[0] - int((headWidth - thickness)/2), tc[1] - radius), headLen, headWidth, isLeft=True, c=c)
    else:
        drawRectangle(img, c, (tc[0],tc[1] - radius), (tc[0] + thickness - 1, tc[1] - radius + headLen - 1))

    if right:
        drawTriangle(img, (tc[0] - int((headWidth - thickness)/2), tc[1] + radius - headLen), headLen, headWidth, isLeft=False, c=c)
    else:
        drawRectangle(img, c, (tc[0],tc[1] + radius - headLen + 1), (tc[0] + thickness - 1, tc[1] + radius))