import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import random

def drawRectangle(img, c, tl, br):

    # Add alpha if not provided
    if len(c) == 3: c = [c[0], c[1], c[2], 255]

    for k in range(4):
        img[tl[0]:br[0], tl[1]:br[1], k] *= 0
        img[tl[0]:br[0], tl[1]:br[1], k] += c[k]


def drawCircle(img, c, centre, radius):

    if len(c) == 3: c = [c[0], c[1], c[2], 255]
    for i in range(centre[0] - radius, centre[0] + radius + 1):
        for j in range(centre[1] - radius, centre[1] + radius + 1):

            if np.sqrt((centre[0] - i)**2 + (centre[1] - j)**2) > radius: continue

            img[i][j][0] = c[0]
            img[i][j][1] = c[1]
            img[i][j][2] = c[2]
            img[i][j][3] = c[3]


def drawRoundedRectangle(sign, c, tl, br, roundRadius, giveBoundingBox):

    if len(c) == 3: c = [c[0], c[1], c[2], 255]

    img = sign.image

    # Draw circles
    drawCircle(img, c, (tl[0] + roundRadius, tl[1] + roundRadius), roundRadius)
    drawCircle(img, c, (tl[0] + roundRadius, br[1] - roundRadius), roundRadius)
    drawCircle(img, c, (br[0] - roundRadius, tl[1] + roundRadius), roundRadius)
    drawCircle(img, c, (br[0] - roundRadius, br[1] - roundRadius), roundRadius)

    # Draw rectangles
    drawRectangle(img, c, (tl[0] + roundRadius, tl[1]), (br[0] - roundRadius, br[1]))
    drawRectangle(img, c, (tl[0], tl[1] + roundRadius), (tl[0] + roundRadius, br[1] - roundRadius))
    drawRectangle(img, c, (br[0] - roundRadius, tl[1] + roundRadius), (br[0], br[1] - roundRadius))

    # Add bounding box if requested
    if giveBoundingBox:
        sign.bounds = [(tl[0], tl[1]), (tl[0], br[1]), (br[0], br[1]), (br[0], tl[1])]


def textDims(text_string, font_size, font=None):
    # https://stackoverflow.com/a/46220683/9263761
    if font is None: 
        font = ImageFont.truetype("nswsigns/fonts/UniversCondensed.ttf", font_size)
    _, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_height, text_width)


def textBBoxBuffers(text, size, font=None, dims=None):

    # Default font
    if font is None: 
        font = ImageFont.truetype("nswsigns/fonts/UniversCondensed.ttf", size)

    # Get some outer dimensions
    if dims is None: dims = textDims(text, size, font)

    # Create an array of this size to draw
    arr = np.zeros((dims[0], dims[1]))

    # Draw on array
    pilFrame = Image.fromarray(np.array(arr, dtype = np.uint8))
    editable = ImageDraw.Draw(pilFrame)
    editable.text((0,0), text, 1, font = font)
    imgPIL = np.array(pilFrame)
    arr += imgPIL

    # Get offsets
    t, l, b, r = 0, 0, 0, 0
    while np.max(arr[t]) == 0: t += 1
    while np.max(arr[dims[0] - 1 - b]) == 0: b += 1
    while np.max(arr[:,l]) == 0: l += 1
    while np.max(arr[:,dims[1] - 1 - r]) == 0: r += 1

    # Calculate real differentials
    buffer = 4
    t = t - buffer
    l = l - buffer
    b = -b + buffer - 1
    r = -r + buffer - 1

    return t, l, b, r


def drawText(sign, text, tc, size=50, c = (128, 128, 128, 255), font=None, useAsTl=False):

    img = sign.image

    # Get dimensions and find top left
    if font is None: 
        font = ImageFont.truetype("nswsigns/fonts/UniversCondensed.ttf", size)
    dims = textDims(text, size, font)
    if useAsTl:
        tl = tc
    else:
        tl = (tc[0], tc[1] - dims[1] // 2)

    text = text.split(" ")
    if len(text) > 1:
        aSpaceADim = textDims("a a", size, font)
        aADim = textDims("aa", size, font)
        spaceWidth = aSpaceADim[1] - aADim[1]
        for string in text:
            textDim = textDims(string, size, font)
            drawText(sign, string, tl, size, c, font, True)
            tl = (tl[0], tl[1] + textDim[1] + spaceWidth)
        return
    else:
        text = text[0]
        

    # Draw text in location
    pilFrame = Image.fromarray(np.array(img, dtype = np.uint8))
    editable = ImageDraw.Draw(pilFrame)
    editable.text(tl[::-1], text, c, font = font)
    imgPIL = np.array(pilFrame)
    img *= 0
    img += imgPIL

    # Give bounding box
    tBuff, lBuff, bBuff, rBuff = textBBoxBuffers(text, size, font, dims) 

    #topDiff = int(round(dims[0] * 0.2))
    bbox = [[(tl[0]+tBuff, tl[1]+lBuff), (tl[0]+dims[0]+bBuff, tl[1]+lBuff), (tl[0]+dims[0]+bBuff, tl[1]+dims[1]+rBuff), (tl[0]+tBuff, tl[1]+dims[1]+rBuff)], text]
    sign.textBounds.append(bbox)


# Examples: times = ("9:00", "AM", "1:00", "PM")
#           days = ("SAT-SUN", "PUBLIC HOLIDAYS"), (can replace e.g. "MON-FRI" with e.g. "MON")
def drawTimeLimit(sign, tc, times, days, height, vgapPc, hgapPc, dashWidthPc, dashHeightPc, c):
    
    vgap = int(round(height * vgapPc))
    hgap = int(round(height * hgapPc))
    mpc = 0.35
    minpc = 0.55
    dayPc = 0.35
    dashWidth = int(round(dashWidthPc * height))
    dashHeight = int(round(dashHeightPc * height))

    # Split all components
    startTime = times[0].split(":")
    startM = times[1]
    endTime = times[2].split(":")
    endM = times[3]

    # Determine width requirements
    startIntWidth = textDims(startTime[0], height)[1]
    startMWidth = textDims(startM, int(round(height * mpc)))[1]
    endIntWidth = textDims(endTime[0], height)[1]
    endMWidth = textDims(endM, int(round(height * mpc)))[1]

    # Extra buffer
    buffer = 2

    totalWidth = startIntWidth + startMWidth + endIntWidth + endMWidth + dashWidth + 4*hgap + 2*buffer
    radius = totalWidth // 2

    # Determine top central positions of each
    offset = 4
    topHeight = tc[0]
    centre = tc[1]
    startIntPos = (topHeight, centre - radius + startIntWidth // 2)
    startMPos = (topHeight + int(round(height * (1-mpc)) - offset), centre - radius + startIntWidth + hgap + buffer + startMWidth // 2)
    endIntPos = (topHeight, centre + radius - endMWidth - endIntWidth - hgap - buffer + endIntWidth // 2)
    endMPos = (topHeight + int(round(height * (1-mpc)) - offset), centre + radius - endMWidth + endMWidth // 2)

    # Determine dash rectangle positioning
    dashTL = (
        int(round(topHeight + height*0.6 - dashHeight//2)),
        int(round(centre - radius + startIntWidth + startMWidth + 2*hgap + height*0.08*(len(startTime)==2)))
    )
    dashBR = (
        dashTL[0] + dashHeight,
        dashTL[1] + dashWidth
    )

    # Draw text in correct positions
    drawText(sign, startTime[0], startIntPos, size=height, c=c)
    ib = sign.textBounds[-1]
    drawText(sign, startM, startMPos, size=int(round(height * mpc)), c=c)
    drawRectangle(sign.image, c, dashTL, dashBR)
    drawText(sign, endTime[0], endIntPos, size=height, c=c)
    drawText(sign, endM, endMPos, size=int(round(height * mpc)), c=c)

    # Add bounding box for dash
    bbox = [[(ib[0][0][0], dashTL[1] - 3), (ib[0][2][0], dashTL[1] - 3), (ib[0][2][0], dashBR[1] + 2), (ib[0][0][0], dashBR[1] + 2)], "-"]
    sign.textBounds.append(bbox)

    # Add minutes if present
    if len(startTime) == 2:
        if startTime[1] != "00" or random.random() < 0.5:
            startMinPos = (topHeight + height*0.1, startMPos[1])
            drawText(sign, startTime[1], startMinPos, size = int(round(height * minpc)), c=c)

    if len(endTime) == 2:
        if endTime[1] != "00" or random.random() < 0.5:
            endMinPos = (topHeight + height*0.1, endMPos[1])
            drawText(sign, endTime[1], endMinPos, size = int(round(height * minpc)), c=c)

    # Add day text
    upTo = tc[0] + height + vgap
    dayHeight = int(round(dayPc * height))
    dayGap = int(round(dayPc * hgap * 2))
    dayDashWidth = int(round(dayPc * dashWidth))
    dayDashHeight = int(round(dayPc * dashHeight))
    for dayString in days:
        dayString = dayString.split("-")

        if len(dayString) == 1:
            # Just write this in the correct position
            drawText(sign, dayString[0], (upTo, centre), size=dayHeight, c=c)

        if len(dayString) == 2:
            # Need to add in the dash
            startDayWidth = textDims(dayString[0], dayHeight)[1]
            endDayWidth = textDims(dayString[1], dayHeight)[1]
            dayWidth = startDayWidth + endDayWidth + 2*dayGap + dayDashWidth
            dayRadius = dayWidth // 2
            startDayPos = (upTo, centre - dayRadius + startDayWidth // 2)
            endDayPos = (upTo, centre + dayRadius - endDayWidth // 2)
            dayDashTL = (
                int(round(upTo + dayHeight*0.6 - dayDashHeight / 2)),
                int(round(centre - dayRadius + startDayWidth + dayGap + 1))
            )
            dayDashBR = (
                dayDashTL[0] + dayDashHeight,
                dayDashTL[1] + dayDashWidth
            )

            # Draw stuff
            drawText(sign, dayString[0], startDayPos, dayHeight, c)
            ib = sign.textBounds[-1]
            drawRectangle(sign.image, c, dayDashTL, dayDashBR)
            drawText(sign, dayString[1], endDayPos, dayHeight, c)

            # Give rectangle a bounding box
            bbox = [[(ib[0][0][0], dayDashTL[1] - 2), (ib[0][2][0], dayDashTL[1] - 2), (ib[0][2][0], dayDashBR[1] + 1), (ib[0][0][0], dayDashBR[1] + 1)], "-"]
            sign.textBounds.append(bbox)


        upTo += dayHeight + vgap


def drawTexts(sign, texts, tc, size=50, c = (128, 128, 128, 255), font=None, spacing=1.5):
    
    # Get height
    if font is None: 
        font = ImageFont.truetype("nswsigns/fonts/UniversCondensed.ttf", size)
    height = textDims(texts[0], size, font)[0]

    # Draw each line
    for i, text in enumerate(texts):
        drawText(sign, text, (tc[0] + i * int(height * spacing), tc[1]), c=c, font=font, size=size)


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



def drawArrow(sign, tc, radius=150, thickness=10, left=False, right=False, headLen=None, headWidth=None, c=(255,255,255,255)):

    img = sign.image
    sign.hasLeftArrow = left
    sign.hasRightArrow = right

    # Set defaults of 3x width, 15% length for heads
    if headLen is None: headLen = int(radius * 2 * 0.15)
    if headWidth is None: headWidth = 3 * thickness

    # Draw the main rectangle
    drawRectangle(img, c, (tc[0], tc[1] - radius + headLen), (tc[0] + thickness - 1, tc[1] + radius - headLen))

    # Draw arrow heads
    if left:
        drawTriangle(img, (tc[0] - int((headWidth - thickness)/2), tc[1] - radius), headLen, headWidth, isLeft=True, c=c)
    else:
        drawRectangle(img, c, (tc[0],tc[1] - radius), (tc[0] + thickness - 1, tc[1] - radius + headLen))

    if right:
        drawTriangle(img, (tc[0] - int((headWidth - thickness)/2), tc[1] + radius - headLen), headLen, headWidth, isLeft=False, c=c)
    else:
        drawRectangle(img, c, (tc[0],tc[1] + radius - headLen), (tc[0] + thickness - 1, tc[1] + radius))


def pointDist(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] + p2[1])**2)


def drawLine(img, start, end, c=None, thick=False):

    if c is None:
        c = (random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256), 255)

    dim0Len = abs(start[0] - end[0])
    dim1Len = abs(start[1] - end[1])

    pcInc = min(1 / (1+dim0Len), 1 / (1+dim1Len)) / 2

    pc = 0
    while pc < 1:
        xpos = int(round(start[0] * (1 - pc) + end[0] * pc))
        ypos = int(round(start[1] * (1 - pc) + end[1] * pc))

        for k in range(len(c)):
            img[xpos][ypos][k] = c[k]

            if thick:
                img[xpos-1][ypos][k] = c[k]
                img[xpos+1][ypos][k] = c[k]
                img[xpos][ypos-1][k] = c[k]
                img[xpos][ypos+1][k] = c[k]


        pc += pcInc


if __name__ == "__main__":

    for i in range(12):
        print(i, textDims(str(i), 1000))

    for x in ["-", "—", "AM", "PM", "00", "15", "30", "45"]:
        print(x, textDims(x, 1000))