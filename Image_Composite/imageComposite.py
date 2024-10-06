# imageComposite.py
# created 2021/07/01 by Max Figura
# input: a collection of video frames named consecutively as "frame#.png" starting with frame1.png
# output: a single image showing a vertical slice of each frame such that time passes from left to right
# for best results, the number of frames should evenly divide the horizontal resolution of each image
# NOTE: all comments added 2024/10/06

import sys
#Image manipulation library
from PIL import Image

#Open frames until running out of valid filenames
pics = []
i = 1
while True:
    infile = "frame"+str(i)+".png"
    try:
        im = Image.open(infile)
        pics.append(im)
        i+=1
    except: break

#Determine slice size
s = pics[0].size
w = s[0]//len(pics)
print(w)

#Crop each frame according to position and slice size
crops = []
wid = w
for pic in pics:
    box = (0,0,wid,s[1])
    region = pic.crop(box)
    crops.append(region)
    wid+=w

#Overlay frames backwards, largest to smallest
crops.reverse()
for crop in crops:
    print(wid)
    box = (0,0,wid,s[1])
    pics[0].paste(crop)
    wid-=w

#Save result
pics[0].save("finished.png")
