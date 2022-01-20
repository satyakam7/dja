import time
from datetime import datetime, date, time, timedelta

import random
import string

from .models import swimmingUser

SLOT_STRENGTH = 100

slots = ["AM67","AM78","AM89","PM56","PM67","PM78"]

def random_alphaNumeric_string(lettersCount, digitsCount):
    sampleStr = ''.join((random.choice(string.ascii_letters) for i in range(lettersCount)))
    sampleStr += ''.join((random.choice(string.digits) for i in range(digitsCount)))
    
    # Convert string to list and shuffle it to mix letters and digits
    sampleList = list(sampleStr)
    random.shuffle(sampleList)
    finalString = ''.join(sampleList)
    return finalString

def getBookableSlots(currTime,currDate):
    day1 = currDate
    if(day1.weekday() == 6):        #isSunday
        day1 += timedelta(days=1)
    day2 = day1 + timedelta(days=1)
    if(day2.weekday() == 6):        #isSunday
        day2 = day2 + timedelta(days=1)
    day3 = day2 + timedelta(days=1)
    if(day3.weekday() == 6):        #isSunday
        day3 = day3 + timedelta(days=1)
    d1 = (day1.strftime("%d/%m/%Y"))
    d2 = (day2.strftime("%d/%m/%Y"))
    d3 = (day3.strftime("%d/%m/%Y"))

    # data = {}
    # data[d1] = []
    # data[d2] = slots
    # data[d3] = slots

    list1 = []
    list2 = slots
    list3 = slots

    if(currDate != day1):
        list1 = slots
        
    else:
        currHour = currTime.hour
        if(currHour < 4):
            list1 = slots
        elif(currHour == 4):
            list1 = ["AM78","AM89","PM56","PM67","PM78"]
        elif(currHour == 5):
            list1 = ["AM89","PM56","PM67","PM78"]
        elif(currHour == 6):
            list1 = ["PM56","PM67","PM78"]
        elif(currHour > 6 and currHour < 15):
            list1 = ["PM56","PM67","PM78"]
        elif(currHour == 15):
            list1 = ["PM67","PM78"]
        elif(currHour == 16):
            list1 = ["PM78"]

    slotList = []
    for elm in list1:
        slotList.append(d1 + elm)
    for elm in list2:
        slotList.append(d2 + elm)
    for elm in list3:
        slotList.append(d3 + elm)

    

    displayList = []
    for elm in list1:
        t1 = elm[2] + ":00"
        t2 = elm[3] + ":00"
        d = elm[0:2]
        f = t1 + d +" - " + t2 + d
        ff = d1 + " , " + f
        displayList.append(ff)
    for elm in list2:
        t1 = elm[2] + ":00"
        t2 = elm[3] + ":00"
        d = elm[0:2]
        f = t1 + d +" - " + t2 + d
        ff = d2 + " , " + f
        displayList.append(ff)
    for elm in list3:
        t1 = elm[2] + ":00"
        t2 = elm[3] + ":00"
        d = elm[0:2] 
        f = t1 + d +" - " + t2 + d
        ff = d3 + " , " + f 
        displayList.append(ff)

    placesLeftList = []
    adjustedSlotList = []
    for i in range(len(slotList)):
        s = slotList[i]
        adjustedSlotList.append("a"+s[0:2]+s[3:5]+s[6:15])
        date = getDate(s[0:10])
        dm = s[10:14]
        c = SLOT_STRENGTH - swimmingUser.objects.filter(date=date).filter(slot=dm).count()
        msg = str(c)+ ' place(s) left in the slot'
        if(c==0):
            msg = 'This slot is full, please try another slot'
        placesLeftList.append(msg)
    
    ans = {}
    ans['slots'] = zip(slotList,displayList)
    ans['placesLeft'] = zip(adjustedSlotList,placesLeftList)

    

    # ans['placesLeft'] = zip(adjustedSlotList,placesLeftList)
    return ans

def getDate(str):       #get Date from 10/06/202067AM
    day = int(str[0:2])
    month = int(str[3:5])
    year = int(str[6:10])

    dt = date(year, month, day)
    
    return dt

def getSlotDisplay(str):    #get Display from 10/06/202067AM
    elm = str[10:14]
    day = str[0:10]
    t1 = elm[2] + ":00"
    t2 = elm[3] + ":00"
    d = elm[0:2]
    f = t1 + d +" - " + t2 + d
    ff = day + " , " + f
    return ff