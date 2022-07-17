# Utility to randomise time limit data, returns arguments for 
# draw.drawTimeLimit calls

import random

# Some arrays of options for use
minuteSamples = ["00", "15", "30", "45"]
daySamples = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
#fullDaySamples = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

"""def dayEnum(day):
    if day == "MON" or day == "MONDAY": return 1
    if day == "TUE" or day == "TUESDAY": return 2
    if day == "WED" or day == "WEDNESDAY": return 3
    if day == "THU" or day == "THURSDAY": return 4
    if day == "FRI" or day == "FRIDAY": return 5
    if day == "SAT" or day == "SATURDAY": return 6
    if day == "SUN" or day == "SUNDAY": return 7
    
    #if day == "SCHOOL DAYS": return 8
    #if day == "OTHER DAYS": return 9
    #if day == "PUBLIC HOLIDAYS": return 10

    print(f"ERROR: could not find valid day enumeration for {day}. Exiting.")
    exit(1)"""

def dayToStr(day):
    if day == 1: return "MON"
    if day == 2: return "TUE"
    if day == 3: return "WED"
    if day == 4: return "THU"
    if day == 5: return "FRI"
    if day == 6: return "SAT"
    if day == 7: return "SUN"

    raise Exception(f"No valid day for code {day}")


def daysToStr(d1, d2):
    if d1 == d2: return (dayToStr(d1),)
    return (f"{dayToStr(d1)}-{dayToStr(d2)}",)
    

def timeToStrs(time):
    hour = int(time)
    minute = minuteSamples[int(round((time - hour) * 4))]
    if hour < 12: m = "AM"
    else: m = "PM"
    return f"{(hour - 1) % 12 + 1}:{minute}", m


def randomTimeRange(minLength):

    # Calculate random times
    t1 = random.randint(0, 24 * 4) / 4
    t2 = random.randint(0, 24 * 4) / 4
    t1, t2 = sorted([t1, t2])

    # Return if far enough apart, otherwise try again
    if t2 - t1 >= minLength + 0.25: return t1, t2
    else: return randomTimeRange(minLength)


def randomDayRange(pNone):

    # Give no days randomly
    if random.random() < pNone: return None

    # Calculate and return random days
    d1 = random.randint(1, 7)
    d2 = random.randint(1, 7)
    d1, d2 = sorted([d1, d2])
    return d1, d2


def randomDT(minTime, pNoDays):
    days = randomDayRange(pNoDays)
    times = randomTimeRange(minTime)
    return days, times


def timesOverlap(t1, t2):
    return not (t1[1] <= t2[0] or t2[1] < t1[0])
 

def daysOverlap(d1, d2):
    return not (d1[1] < d2[0] or d2[1] < d1[0])


def isOverlap(dt1, dt2):
    d1, t1 = dt1
    d2, t2 = dt2
    if not daysOverlap(d1, d2): return False
    if not timesOverlap(t1, t2): return False
    return True


# Check for multisign clashes, return indices for the first found issue
def checkClashes(arr):

    # Flatten array but retain indices
    flat = []
    for i, a in enumerate(arr):
        for j, dt in enumerate(a):
            flat.append((dt[0], i, j))

    # Check each matchup
    for i in range(len(flat)):
        for j in range(len(flat)):
            if i == j: continue
            if isOverlap(flat[i][0], flat[j][0]):
                return flat[i][1], flat[i][2], flat[j][1], flat[j][2]

    return None

# times = ("9:00", "AM", "1:00", "PM")
# days = ("SAT-SUN", "PUBLIC HOLIDAYS"), (can replace e.g. "MON-FRI" with e.g. "MON")
def splitDTs(dt):
    days, times = dt
    t1, t2 = times
    times = (*timeToStrs(t1), *timeToStrs(t2))
    days = daysToStr(*days)
    return days, times


def dayLines(day):
    return 1 # TODO: update this with special stuff


def heightDT(dt, params):
    timeHeight = params["time height"]
    timeHeight += params["time height"] * params["vertical time gap percentage"]
    dayHeight = 0
    dayHeight += params["time height"] * params["day height percentage"]
    dayHeight += params["time height"] * params["vertical time gap percentage"]
    dayHeight *= dayLines(dt[0])
    return int(round(timeHeight + dayHeight))
    

def getDTs(paramList):

    num = len(paramList)
    numTimes = [0] * num
    out = []
    for _ in range(num): out.append([])
    upToHeights = []

    # If more than one sign, add a time to each by default
    # TODO: might be able to get rid of most of this
    """complete = False
    while not complete and num > 1:
        
        # Add times, if one isn't already there
        for i in range(num):
            numTimes[i] += 1
            params = paramList[i]
            params["up_to_dt"] = params["time top"]
            if len(out[i]) > 0: continue
            dt = randomDT(paramList[i]["minimum time"], 0)
            out[i].append((dt, (params["up_to_dt"], params["time centre"])))
            params["up_to_dt"] += heightDT(dt, params)


        # Check for clashes, 
        # if one exists then remove one of the offendors
        issue = checkClashes(out)
        if issue is None: complete = True
        else:
            # Remove one
            if random.random() < 0.5:
                paramList[issue[1]]["up_to_dt"] -= out[issue[0]][issue[1]][0]
                out[issue[0]] = []
                numTimes[issue[0]] -= 1
            else:
                paramList[issue[1]]["up_to_dt"] -= out[issue[0]][issue[1]][0]
                out[issue[1]] = []
                numTimes[issue[1]] -= 1"""
    for i in range(num):
        paramList[i]["up_to_dt"] = paramList[i]["time top"]
        numTimes[i] += (num > 1)

    # Create time counts
    for i in range(num):
        if numTimes[i] == 0 and random.random() > paramList[i]["p no times"]:
            numTimes[i] += 1
        else:
            continue

        while random.random() < paramList[i]["p next"] and numTimes[i] < paramList[i]["max times"]:
            numTimes[i] += 1


    # Assign more times based on counts
    complete = False
    while not complete:

        # Assign one time to the first non-full sign
        added = False
        for i in range(num):
            if len(out[i]) < numTimes[i]:
                added = True
                params = paramList[i]
                dt = randomDT(paramList[i]["minimum time"], 0)
                #print(out[i])
                out[i].append((dt, (params["up_to_dt"], params["time centre"])))
                params["up_to_dt"] += heightDT(dt, params)

                # If this makes the time list too long, remove the 
                # element and reduce the number of times for this sign
                if params["up_to_dt"] > params["time bottom"]:
                    rm = out[i].pop()
                    params["up_to_dt"] -= heightDT(rm[0], params)
                    numTimes[i] -= 1

        if not added: complete = True

        # Check for any clashes
        #print(out)
        issue = checkClashes(out)
        if issue is not None:
            complete = False
            sign1, time1, sign2, time2 = issue
            rmSign, rmTime = random.choice([(sign1, time1), (sign2, time2)])

            # Remove specific sign
            out[rmSign].pop(rmTime)

            # Redo up_to_dt for this whole sign
            params = paramList[rmSign]
            params["up_to_dt"] = params["time top"]
            for i, (dt, tc) in enumerate(out[rmSign]):
                out[rmSign][i] = (dt, (params["up_to_dt"], tc[1]))
                params["up_to_dt"] += heightDT(dt, params)



    # TODO: add special days

    return out








"""def daysOverlap(days1, days2):

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
        

def checkMultiOverlap(times):
    pass

def getMultiSignTimes(paramList, pNext):

    numSigns = len(paramList)
    complete = False # use at various stages
    out = []
    for _ in range(numSigns): out.append([])

    # If more than one sign, add one time to each
    while numSigns > 1 and not complete:

        # Add a time to each if there isn't already one
        for i in range(numSigns):



    while not complete:


        pass
"""
