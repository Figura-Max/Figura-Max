#earclip.py
#Polygon Triangulation via earclipping method
#Returns a list of triangles

import math

def earclip(poly):   #Polygon in the form of [(x1,y1),(x2,y2)...]
    if len(poly) < 4:
        return [poly]
    for i in range(len(poly)):
        p1 = poly[i-1]
        p2 = poly[i]
        p3 = poly[(i+1)%len(poly)]

        isEar = True
        if orient(p1,p2,p3) == 1: isEar = False
        else:
            for j in poly:
                if orient(p1,p2,j) == orient(p2,p3,j) == orient(p3,p1,j):
                    isEar = False
        
        if isEar:
            nextPoly = poly.copy()
            nextPoly.remove(p2)
            tris = earclip(nextPoly)
            tris.append([p1,p2,p3])
            return tris

def orient(p1,p2,p3):
    ang = (p2[1]-p1[1])*(p3[0]-p2[0]) - (p2[0]-p1[0])*(p3[1]-p2[1])
    if ang > 0: return 1
    if ang < 0: return -1
    return 0


if __name__ == "__main__":
    polygon = [(0,0),(0,1),(1,1),(1,0)]
    print(earclip(polygon))
