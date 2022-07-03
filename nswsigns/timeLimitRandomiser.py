# Utility to randomise time limit data, returns arguments for 
# draw.drawTimeLimit calls

import random

"""
        draw.drawTimeLimit( # TODO: add randomness
            sign=sign,
            tc=(400, dimensions[1] // 2), 
            times=("1:00", "AM", "12:30", "PM"),
            days=("SAT-SUN &", "PUBLIC HOLIDAYS"),
            height=timeHeight,
            vgapPc=timeVGapPc,
            hgapPc=timeHGapPc,
            dashWidthPc=timeDashWidthPc,
            dashHeightPc=timeDashHeightPc,
            c=tuple(white),
        )
"""

# Some arrays of options for use
minuteSamples = ["00", "15", "30", "45"]
daySamples = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
fullDaySamples = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

def dayEnum(day):
    if day == "MON": return 1
    if day == "TUE": return 2
    if day == "WED": return 3
    if day == "THU": return 4
    if day == "FRI": return 5
    if day == "SAT": return 6
    if day == "SUN": return 7

    print(f"ERROR: could not find valid day enumeration for {day}. Exiting.")
    exit(1)


def daysOverlap(days1, days2):

    days1Copy = days1[0].split("-")
    days2Copy = days2[0].split("-")

    taken = [False, False, False, False, False, False, False]
    for i in range(1, 8):
        if i < dayEnum(days1Copy[0]): continue
        if i > dayEnum(days1Copy[-1]): continue
        taken[i-1] = True

    for i in range(1, 8):
        if i < dayEnum(days2Copy[0]): continue
        if i > dayEnum(days2Copy[-1]): continue

        if taken[i-1]: return True

    return False


def timeToFloat(time, m):
    time = time.split(":")
    val = int(time[0]) % 12 + float(time[1]) / 60 + 12*(m=="PM")
    return val


def timesOverlap(time1a, m1a, time1b, m1b, time2a, m2a, time2b, m2b):

    t1a = timeToFloat(time1a, m1a)
    t1b = timeToFloat(time1b, m1b)
    t2a = timeToFloat(time2a, m2a)
    t2b = timeToFloat(time2b, m2b)

    return 1 - ((t1b <= t2a) * (t1a <= t2b) + (t1b >= t2a) * (t1a >= t2b))


def dateAndTimeOverlap(times1, times2, days1, days2):

    if not daysOverlap(days1, days2): return False
    if not timesOverlap(*times1, *times2): return False # Might need to fix this if it breaks
    return True


def fullRandomTimeAndDay(pSpecial):
    # Choose two abbreviations and form a range
    day1 = random.choice(daySamples)
    day2 = random.choice(daySamples)
    d = sorted([day1, day2], key = lambda x: dayEnum(x))

    if day1 == day2:
        d = [day1]
    else:
        d = [f"{d[0]}-{d[1]}"]
    d = tuple(d)

    # Choose times
    time1, time2 = 0, 0
    while int(4 * time1) == int(4 * time2) or time1 > time2:
        time1 = random.uniform(0, 24)
        time2 = random.uniform(0, 24)
    hour1 = int(time1)
    hour2 = int(time2)
    m1 = "AM" if hour1 < 12 else "PM"
    m2 = "AM" if hour2 < 12 else "PM"
    minute1 = minuteSamples[int((time1 - hour1) * 4)]
    minute2 = minuteSamples[int((time2 - hour2) * 4)]
    hour1 = str(((hour1 - 1) % 12) + 1)
    hour2 = str(((hour2 - 1) % 12) + 1)

    return (f"{hour1}:{minute1}", m1, f"{hour2}:{minute2}", m2), d


def getRandomTimesAndDays(num, pSpecial):

    out = []
    for _ in range(num):
        out.append(fullRandomTimeAndDay(0))

    isOverlap = False
    keepGoing = True
    while keepGoing:
        isOverlap = False
        keepGoing = False
        for i in range(num):
            for j in range(num):
                if i == j: continue
                if dateAndTimeOverlap(out[i][0], out[j][0], out[i][1], out[j][1]):

                    # Randomly remove one of these
                    if random.random() < 0.1: out.pop(i)
                    else: out.pop(j)
                    isOverlap = True
                    break

            if isOverlap: break

        if isOverlap:
            out.append(fullRandomTimeAndDay(0))
            keepGoing = True

    return out



def getRandomArgs(sign, tc, bc, height, vGapPc, hGapPc, dashWidthPc, dashHeightPc, c, pEmpty, pNext, pSpecial, maxTimes):

    out = []

    # Return nothing if empty
    if random.random() < pEmpty: return out

    # If not empty, add a time, then probabilistically add more
    numTimes = 1
    while random.random() < pNext and numTimes < maxTimes: numTimes += 1

    # Determine appropriate times
    dt = getRandomTimesAndDays(numTimes, pSpecial)

    upToHeight = tc[0]

    #if numTimes == 1:
    for (times, days) in dt:

        #print("Up to", upToHeight)
        timeTC = (upToHeight, tc[1])
        
        # Check if this time will fit
        takenHeight = height * (1 + vGapPc)
        if len(days) > 0: takenHeight += height * (vGapPc + 0.35)

        #print("Taken", takenHeight)
        upToHeight += takenHeight
        #print(f"Taken height: {takenHeight}, Up to: {upToHeight}, max: {bc[0]}")
        if upToHeight > bc[0]: break

        

        out.append((
            sign,
            timeTC,
            times,
            days,
            height,
            vGapPc,
            hGapPc,
            dashWidthPc,
            dashHeightPc,
            c
        ))

    return out
        


