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
    t1 = random.randint(0, 24 * 4 - 1) / 4
    t2 = random.randint(0, 24 * 4 - 1) / 4
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
def checkClashes(arr, paramList=None):

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
                # Check for parameters
                if paramList is None:
                    return flat[i][1], flat[i][2], flat[j][1], flat[j][2]
                # Have parameters, so only register clash if there is a 
                # common direction
                if paramList[flat[i][1]]["left arrow"] and paramList[flat[j][1]]["left arrow"]:
                    return flat[i][1], flat[i][2], flat[j][1], flat[j][2]
                if paramList[flat[i][1]]["right arrow"] and paramList[flat[j][1]]["right arrow"]:
                    return flat[i][1], flat[i][2], flat[j][1], flat[j][2]

    return None

# times = ("9:00", "AM", "1:00", "PM")
# days = ("SAT-SUN", "PUBLIC HOLIDAYS"), (can replace e.g. "MON-FRI" 
# with e.g. "MON")
def splitDTs(dt):
    days, times = dt
    t1, t2 = times
    times = (*timeToStrs(t1), *timeToStrs(t2))
    if days is not None:
        days = daysToStr(*days)
    return days, times


def dayLines(day):
    if day is None: return 0
    return 1 # TODO: update this with special stuff


def heightDT(dt, params):
    timeHeight = params["time height"]
    timeHeight += params["time height"] * params["vertical time gap percentage"]
    dayHeight = 0
    dayHeight += params["time height"] * params["day height percentage"]
    dayHeight += params["time height"] * params["vertical time gap percentage"]
    dayHeight *= dayLines(dt[0])
    return int(round(timeHeight + dayHeight))
    

def getDirectionalDTs(paramList, hasLeft, hasRight, out=None, maxIter=100000, penalty=0):
    numLeft = sum(hasLeft)
    numRight = sum(hasRight)
    num = len(paramList)
    numTimes = [0] * num
    iters = maxIter

    if out is None:
        out = []
        for _ in range(num): out.append([])
        for i in range(num):
            paramList[i]["up_to_dt"] = paramList[i]["time top"]
            if hasLeft[i] and numLeft > 1 or hasRight[i] and numRight > 1:
                numTimes[i] += 1

    # Create time counts
    for i in range(num):
        if numTimes[i] == 0:
            if random.random() > paramList[i]["p no times"]:
                numTimes[i] += 1
            else:
                continue

        while random.random() + penalty < paramList[i]["p next"] and numTimes[i] < paramList[i]["max times"]:
            numTimes[i] += 1


    # Assign more times based on counts
    complete = False
    count = 0
    while True:

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
        issue = checkClashes(out, paramList)
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

        if complete: break

        # Check if can be broken here and if not, just try again
        count += 1
        print(f"({penalty:.02f}) " + f"{count}".ljust(7, " "), end = "\r")
        if count == iters:
            for arr, l, r in zip(out, hasLeft, hasRight):
                if l and len(arr) == 0 and numLeft > 1:
                    return getDirectionalDTs(paramList, hasLeft, hasRight, maxIter=maxIter, penalty=penalty + 0.01)
                if r and len(arr) == 0 and numRight > 1:
                    return getDirectionalDTs(paramList, hasLeft, hasRight, maxIter=maxIter, penalty=penalty + 0.01)
                if checkClashes(out, paramList) is not None:
                    return getDirectionalDTs(paramList, hasLeft, hasRight, maxIter=maxIter, penalty=penalty + 0.01)


    # TODO: add special days


    assert checkClashes(out, paramList) is None

    # Move any same days next to each other, and remove days if we can
    for arr in out:
        for i in range(len(arr)):
            for j in range(len(arr)):
                
                # Don't need to be moved
                if i == j: continue
                if arr[i][0][0] != arr[j][0][0]: continue
                if abs(i - j) <= 1: continue

                if i < j: # Swap j and i+1
                    tmpip1 = (arr[j][0], arr[i+1][1])
                    tmpj = (arr[i+1][0], arr[j][1])
                    arr[i+1] = tmpip1
                    arr[j] = tmpj
                else: # Swap i and j+1
                    tmpjp1 = (arr[i][0], arr[j+1][1])
                    tmpi = (arr[j+1][0], arr[i][1])
                    arr[j+1] = tmpjp1
                    arr[i] = tmpi
                #print("Switched", arr[i][0][0], arr[j][0][0])

        for i in range(len(arr)):
            if i == 0: continue
            if arr[i][0][0] == arr[i-1][0][0]:
                #print("Removed")
                arr[i-1] = ((None, arr[i-1][0][1]), arr[i-1][1])

    # Redo tcs for all signs
    for i in range(len(out)):
        params = paramList[i]
        params["up_to_dt"] = params["time top"]
        for j, (dt, tc) in enumerate(out[i]):
            out[i][j] = (dt, (params["up_to_dt"], tc[1]))
            params["up_to_dt"] += heightDT(dt, params)

    return out

