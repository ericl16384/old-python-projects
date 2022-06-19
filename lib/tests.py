from math import *

def lineIntersection(line1,line2):
    xdiff = (line1[0][0] - line1[1][0],line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1],line2[0][1] - line2[1][1])

    def det(a,b):
        return a[0]*b[1]-a[1]*b[0]

    div = det(xdiff,ydiff)
    if div == 0:
        return None

    d = (det(*line1),det(*line2))
    x = det(d,xdiff)/div
    y = det(d,ydiff)/div
    return x,y

def withinCircle(circleX,circleY,circleR,x,y):
    if sqrt((x-circleX)**2+(y-circleY)**2) <= circleR:
        return True
    else:
        return False

def withinRect(x1,y1,x2,y2,x,y):
    x1 = min(x1,x2)
    x2 = max(x1,x2)
    y1 = min(y1,y2)
    y2 = max(y1,y2)
    if x >= x1 and x <= x2 and y >= y1 and y <= y2:
        return True
    else:
        return False

def outerParallelVectors(x,y,xV,yV,radius):
    a = xV / yV
    b = 1
    
    c = a**2 + b**2
    d = radius / sqrt(c)
    a *= d
    b *= d
    l = [b,a*-1]
    r = [b*-1,a]
    return l,r
