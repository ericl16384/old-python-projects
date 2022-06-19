from datetime import datetime
from getpass import getpass
import hashlib
from math import *

def append(file,content):
    file = open(file,"a")
    file.write(content)
    file.close()
    return

def read(file,split = True):
    file = open(file)
    i = file.read()
    file.close()
    if split:
        i = i.split("\n")
        if isinstance(i,str):
            i = [i]
    return i

def write(file,content):
    file = open(file,"w")
    file.write(content)
    file.close()
    return

def query(query,possibilities=[""],response=True,state=0):
    #States
    #0 Normal
    #1 Opposite
    #2 Anything
    while True:
        i = input(query + "\n>>> ")
        print()
        if state == 0:
            for x in range(len(possibilities)):
                if i == possibilities[x]:
                    return i
        if state == 1:
            doReturn = True
            for x in range(len(possibilities)):
                if i == possibilities[x]:
                    doReturn = False
                    break
            if doReturn:
                return i
        if state == 2:
            return i
        if response == True:
            print("Select one of these possiblities:")
            for x in range(len(possibilities)):
                print("  " + possibilities[x])
            print()
        else:
            print(response + "\n")

def passQuery(query,possibilities,response,state=0):
    #States
    #0 Normal
    #1 Opposite
    #2 Anything
    while True:
        i = hashlib.sha512(getpass(query + "\n>>> ").encode()).hexdigest()
        print()
        if state == 0:
            for x in range(len(possibilities)):
                if i == possibilities[x]:
                    return i
        if state == 1:
            doReturn = True
            for x in range(len(possibilities)):
                if i == possibilities[x]:
                    doReturn = False
                    break
            if doReturn:
                return i
        if state == 2:
            return i
        print(response + "\n")

def now():
    x = datetime.now()
    x = str(x)
    x = x.split()
    x[0] = x[0].split("-")
    x[len(x)- 1] = x[len(x)- 1].split(":")
    date = [x[0][0],x[0][1],x[0][2],x[1][0],x[1][1],x[1][2]]
    separator = "."
    returnDate = separator.join(date)
    return returnDate

def normalizeVector(x,y):
    c = sqrt(x**2+y**2)
    if c == 0:
        return False
    else:
        return x/c,y/c

def rad(angle):
    while angle < 0:
        angle += 360
    while angle > 360:
        angle -= 360
    return angle/360*(2*pi)

def angle(rad):
    while rad < 0:
        rad += pi
    while rad > 2*pi:
        rad -= pi
    return rad/(2*pi)*360

def matrixMultiplication(a,b,c,d,x,y):
    return a*x+b*y,c*x+d*y

def cartesianToPolar(points):
    i = []
    for point in range(len(points)):
        i.append([
            hypot(points[point][0],points[point][1]),
            angle(atan2(points[point][1],points[point][0]))
            ])
    return i

def polarToCartesain(points,rotation=0):
    i = []
    for point in range(len(points)):
        i.append([
            points[point][0]*angle(cos(points[point][1]+rotation)),
            points[point][0]*angle(sin(points[point][1]+rotation))
            ])
    return i
    
##            points[point][0]*angle(cos(points[point][1]+rotation)),
##            points[point][0]*angle(sin(points[point][1]+rotation))
