#Hunt the Wumpus V2 (1.9.1)
#
#CHANGELOG:
#2020/06/15 - CLASSIC Basic graphics & movement
#2020/06/16 - Basic feature generation (& regen) and interaction
#2020/06/18 - Pathfinding algorithm (pathfind.py) - still bugs
#2020/06/21 - Fixed pathfinding? Improved generation
#2020/06/22 - Improved movement, arrows (no beastdeath or pickup)
#2020/06/23 - Shootable beast, arrow collection, unexplored & hints
#2020/06/25 - Graphics tweaks
#2020/06/27 - Start death screen
#2020/06/28 - Pit death screen, basic death control (no restart)
#2020/06/29 - Wumpus death screen (may redo)
#2020/06/30 - MENU functionality (minimal graphics), pause menu - no mem (options/high)
#2020/06/31 - NEW intra-room movement
#2020/07/03 - Start on door functionality
#2020/07/04 - Door functionality, more scaling, pitdraw
#2020/07/05 - Start on pitcollide
#2020/07/05 - Pit hitbox
#2020/07/08 - Gold render & pickup
#2020/07/09 - Start on beast
#2020/07/12 - Exit-rope draw
#2020/07/13 - Exit functionality - oneway
#2020/07/15 - AntiExit functionality
#2020/07/16 - Improved pit hitbox? MapGen
#2020/07/17 - Start on arrows - graphics
#2020/07/18 - Arrow graphics & fire
#2020/07/19 - Arrow collision, pickup, & roomswitch (complete?)
#2020/07/20 - Start on earclip.py - pit hitbox
#2020/07/21 - Earclipping works??? I'm not complaining
#2020/07/22 - Room hints & map expand
#2020/07/23 - Start on shop room
#2020/07/25 - Continue on graphics - colors!?
#2020/07/27 - Shop room - start on interact/UI
#2020/07/28 - Shop (no item) functionality
#2020/07/29 - Start on UI (inv)
#2020/07/30 - "Finished" UI graphics?
#2020/08/01 - SKeep ~rescue
#2020/08/02 - Durability graphics? Start on item functionality
#2020/08/04 - Pitfall, health
#2020/08/05 - Improved shop room & bugfixes
#2020/08/06 - Start on end bit
#2020/08/08 - Wumpus boss, sprint, fixed facing bug
#2020/08/09 - Player "sprite" - bow
#2020/08/10 - Wumpus "sprites"
#2020/08/11 - Re-establish draw order, start on points
#2020/08/12 - new finished*
#2020/08/14 - Start on mem
#2020/08/15 - Options - controls, resolution, fullscreen
#2020/08/16 - In-game options/menu, in-game scale
#2020/08/17 - Continued mem, hints (with bugs maybe)
#2020/08/19 - Classic Graphics - fixed ingame arrows, start on death screen
#2020/08/20 - Classic Graphic finished?
#2020/08/21 - Highscores
#2020/08/22 - Highscores cont - NEED TO FIX STUFF
#2020/08/23 - Highscores & Scoreboard - 1.9!!!
#2020/08/25 - Added logo, fonts!?
#2021/05/18 - Fixed keyboard issues
#2021/05/19 - Fixed more keyboard issues, packaged
#2021/06/17 - Minor hint tweak, minor resolution-change tweak

#TODO:
#Exportable
#Trebuchet? - looks bad?
#Music?? - not right now

#New Shop Items: all passive except for arrows & potion
#Extra arrows
#Health potion
#Beast repellant - disables/delays chase
#Gold magnet - larger pickup hitbox
#Umbrella - reduce pit damage

#NOTES:
#Keys: up   ,down    ,right    ,left    ,enter     ,space    ,escape    , b 
#     "K_UP","K_DOWN","K_RIGHT","K_LEFT","K_RETURN","K_SPACE","K_ESCAPE","K_b"
#
#Colors: light green , player blue , wumpus  red , weaponbrown ,  gold gold 
#       (200,255,200) (  0,200,200) (230,  0,  0) (100, 50, 50) (255,200,  0)

from pygame import *
from pygame.locals import *
import sys
import random, math
import pathfind, earclip, logo

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                            Classic Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

def cGenFeat(spaces, ID, num):
    eSpace = (4,8)
    for i in range(9):
        for j in range(9):
            if spaces[i][j]%10 == 4:
                eSpace = (i,j)
    feats = 0
    attempts = 0
    while feats < num and attempts < num*2:
        sR = (random.randrange(0,9),random.randrange(0,9))
        if spaces[sR[0]][sR[1]]%10 == 0 and sR != (4,8):
            spaces[sR[0]][sR[1]] = ID
            feats+=1
            if ID==1 and not pathfind.use(spaces,[0,2,3,4],(4,8),(eSpace[0],eSpace[1])):
                feats-=1
                spaces[sR[0]][sR[1]] = 0
        attempts+=1
    if feats == 0 and ID == 4:
        
        spaces[4][8] = 14
    return spaces

def cFullGen(spaces, nums):
    spaces = cGenFeat(spaces,4,nums[4])
    spaces = cGenFeat(spaces,1,nums[1])
    spaces = cGenFeat(spaces,2,nums[2])
    spaces = cGenFeat(spaces,3,nums[3])
    return spaces

def cTestInter(spaces, room):
    if spaces[room[0]][room[1]]//10 == 0:
        spaces[room[0]][room[1]]+=10
    if spaces[room[0]][room[1]]%10 == 1:
        return "death1"
    if spaces[room[0]][room[1]]%10 == 2:
        return "death2"
    if spaces[room[0]][room[1]] == 13:
        return 100
    if spaces[room[0]][room[1]]%10 == 4:
        return "0"
    return 0

def cDeath(death, size, score, sel, win):
    if death == "death1":
        win.fill(Color(200,255,200))
        draw.rect(win,Color(0,0,0),Rect(3*size,3*size,4*size,4*size),5*size)
        draw.circle(win,Color(0,0,0),(3*size,3*size),5*size//2-1)
        draw.circle(win,Color(0,0,0),(3*size,7*size),5*size//2-1)
        draw.circle(win,Color(0,0,0),(7*size,7*size),5*size//2-1)
        draw.circle(win,Color(0,0,0),(7*size,3*size),5*size//2-1)
        draw.polygon(win,Color(0,200,200),((5*size,17*size//2),(23*size//4,15*size//2),(123*size//20,39*size//5),(27*size//5,44*size//5)))
        draw.circle(win,Color(0,200,200),(25*size//4,30*size//4),size//4)
        draw.polygon(win,Color(100,75,50),((176*size//40,306*size//40),(180*size//40,305*size//40),(183*size//40,296*size//40),(198*size//40,290*size//40),(214*size//40,289*size//40),(220*size//40,295*size//40),(224*size//40,294*size//40),(217*size//40,284*size//40),(197*size//40,283*size//40),(178*size//40,293*size//40)))
        #draw.arc(win,Color(100,100,50),Rect(9*size//2,7*size,size,size),0.3,3.44,size//10)
        draw.polygon(win,Color(100,50,50),((217*size//80,623*size//80),(223*size//80,617*size//80),(277*size//80,671*size//80),(271*size//80,677*size//80)))
        draw.polygon(win,Color(100,100,100),((277*size//80,668*size//80),(268*size//80,677*size//80),(286*size//80,686*size//80)))
        draw.polygon(win,Color(50,50,50),((217*size//80,623*size//80),(229*size//80,635*size//80),(223*size//80,635*size//80),(211*size//80,623*size//80)))
        draw.polygon(win,Color(50,50,50),((223*size//80,617*size//80),(235*size//80,629*size//80),(235*size//80,623*size//80),(223*size//80,611*size//80)))
        #draw.line(win,Color(100,50,50),(3*size,15*size//2),(7*size//2,17*size//2),size//8)
        #draw.line(win,Color(100,100,100),(7*size//2,17*size//2),(117*size//32,8*size),size//8)
        #draw.line(win,Color(100,100,100),(7*size//2,17*size//2),(3*size,267*size//32),size//8)
        #draw.circle(win,Color(100,100,100),(7*size//2,17*size//2),size//13)
        
        big = font.SysFont("freesans", 3*size//2)
        small = font.SysFont("freesans", 5*size//8)
        text = [big.render("You Died!",1,(255,255,255)),
                small.render("You fell into a pit!",1,(255,255,255)),
                small.render("Score: "+str(score),1,(255,255,255)),
                small.render("Restart",1,(255,255,255)),
                small.render("Menu",1,(255,255,255))]
    
    elif death == "death2":
        win.fill(Color(200,255,200))
        draw.rect(win,Color(230,0,0),Rect(11*size//8,51*size//8+1,9*size//4,9*size//4))
        draw.rect(win,Color(230,0,0),Rect(11*size//8,51*size//8+1,9*size//4,9*size//4),3*size//4)
        draw.circle(win,Color(230,0,0),(11*size//8,51*size//8+1),3*size//8-1)
        draw.circle(win,Color(230,0,0),(29*size//8,51*size//8+1),3*size//8-1)
        draw.circle(win,Color(230,0,0),(29*size//8,69*size//8+1),3*size//8-1)
        draw.circle(win,Color(230,0,0),(11*size//8,69*size//8+1),3*size//8-1)
        draw.circle(win,Color(255,255,255),(14*size//8,54*size//8),3*size//8)
        draw.circle(win,Color(0,0,0),(25*size//16-1,54*size//8),3*size//16)
        draw.polygon(win,Color(200,255,200),((size,66*size//8),(size,60*size//8),(17*size//8,63*size//8)))
        draw.rect(win,Color(150,150,150),Rect(0,9*size,10*size,size))
        """draw.line(win,Color(0,200,200),(23*size//4,36*size//4),(27*size//4,34*size//4),size//4)
        draw.circle(win,Color(0,200,200),(47*size//8,73*size//8),size//8)
        draw.circle(win,Color(0,200,200),(23*size//4,71*size//8),size//8)
        draw.circle(win,Color(0,200,200),(27*size//4+1,69*size//8+1),size//8)
        draw.circle(win,Color(0,200,200),(53*size//8+1,67*size//8+1),size//8)
        draw.line(win,Color(0,200,200),(45*size//8,64*size//8),(53*size//8,72*size//8),size//4)
        draw.circle(win,Color(0,200,200),(92*size//16,127*size//16),size//8)
        draw.circle(win,Color(0,200,200),(89*size//16,130*size//16),size//8)
        draw.circle(win,Color(0,200,200),(107*size//16,142*size//16),size//8)
        draw.circle(win,Color(0,200,200),(104*size//16,145*size//16),size//8)
        draw.circle(win,Color(0,200,200),(11*size//2,34*size//4),size//3)"""
        draw.line(win,Color(0,200,200),(45*size//8,71*size//8),(55*size//8,71*size//8),size//4)
        draw.circle(win,Color(0,200,200),(45*size//8,70*size//8),size//8)
        draw.circle(win,Color(0,200,200),(45*size//8,72*size//8+1),size//8)
        draw.circle(win,Color(0,200,200),(55*size//8,70*size//8),size//8)
        draw.circle(win,Color(0,200,200),(55*size//8,72*size//8+1),size//8)
        #Skull
        draw.circle(win,Color(0,200,200),(5*size,35*size//4),size//3)
        draw.circle(win,Color(200,255,200),(83*size//16,140*size//16),size//20)
        draw.circle(win,Color(200,255,200),(80*size//16,143*size//16),size//20)
        draw.circle(win,Color(200,255,200),(41*size//8,135*size//16),size//8)
        draw.circle(win,Color(200,255,200),(75*size//16,71*size//8),size//8)
        draw.arc(win,Color(200,255,200),Rect(75*size//16,135*size//16,size,size),1.6,3,size//40)
        draw.line(win,Color(0,0,0),(318*size//40,346*size//40),(362*size//40,357*size//40),size//40)
        draw.polygon(win,Color(100,75,50),((316*size//40,344*size//40),(320*size//40,345*size//40),(323*size//40,354*size//40),(338*size//40,360*size//40),(354*size//40,361*size//40),(360*size//40,355*size//40),(364*size//40,356*size//40),(357*size//40,366*size//40),(337*size//40,367*size//40),(318*size//40,357*size//40)))
        #draw.arc(win,Color(100,100,50),Rect(8*size,33*size//4,size,size),3,6.14,size//8)
        
        big = font.SysFont("freesans", 3*size//2)
        small = font.SysFont("freesans", 5*size//8)
        text = [big.render("You Died!",1,(0,0,0)),
                small.render("You got eaten by a Wumpus!",1,(0,0,0)),
                small.render("Score: "+str(score),1,(0,0,0)),
                small.render("Restart",1,(0,0,0)),
                small.render("Menu",1,(0,0,0))]

    else:
        print("An unexpected error has occurred")
        display.quit()
        sys.exit()
    if sel == "r":
        text[4] = small.render("Menu",1,(0,200,200))
    if sel == "l":
        text[3] = small.render("Restart",1,(0,200,200))
    textpos = [text[0].get_rect(centerx=5*size,centery=9*size//4),
               text[1].get_rect(centerx=5*size,centery=7*size//2),
               text[2].get_rect(centerx=5*size,centery=17*size//4),
               text[3].get_rect(centerx=5*size//2,centery=11*size//2),
               text[4].get_rect(centerx=15*size//2,centery=11*size//2)]
    for i in range(5):
        win.blit(text[i],textpos[i])
    return sel

def pause(size, item, win):
    draw.rect(win,Color(200,200,200),Rect(4*size,7*size//2,2*size,3*size),size)
    draw.rect(win,Color(200,200,200),Rect(4*size,7*size//2,2*size,3*size))
    draw.circle(win,Color(200,200,200),(4*size,7*size//2),size//2-1)
    draw.circle(win,Color(200,200,200),(6*size,7*size//2),size//2-1)
    draw.circle(win,Color(200,200,200),(4*size,13*size//2),size//2-1)
    draw.circle(win,Color(200,200,200),(6*size,13*size//2),size//2-1)
    tColors = [[255,255,255]]*3
    tColors[item] = [0,200,200]
    face = font.SysFont("freesans",size//2)
    text = [face.render("Resume",1,(tColors[0])),
            face.render("Options",1,(tColors[1])),
            face.render("Exit",1,(tColors[2]))]
    textpos = [text[0].get_rect(centerx=5*size,centery=4*size),
               text[1].get_rect(centerx=5*size,centery=5*size),
               text[2].get_rect(centerx=5*size,centery=6*size)]
    for i in range(3):
        win.blit(text[i],textpos[i])
    display.flip()

def cTestAround(spaces, room, size, win):
    yOffset = size//4
    fon = font.SysFont("freesans",size//2)
    text = []
    textpos = []
    colors = (0,(0,0,0),(230,0,0),(255,200,0))
    ipos = (0,2,1,3)
    for i in (1,2,3):
        near = False
        if room[0] < 8 and spaces[room[0]+1][room[1]]%10 == i:
            near = True
        if room[0] > 0 and spaces[room[0]-1][room[1]]%10 == i:
            near = True
        if room[1] < 8 and spaces[room[0]][room[1]+1]%10 == i:
            near = True
        if room[1] > 0 and spaces[room[0]][room[1]-1]%10 == i:
            near = True
        if near:
            if room[0] < 8 and spaces[room[0]+1][room[1]]//10 == 0:
                text.append(fon.render("?",1,colors[i]))
                textpos.append(text[-1].get_rect(centerx=((size*(room[0]+1))+(1/4*(ipos[i]-1)*size)+(3/4*size)),centery=((size*room[1])+size+yOffset)))
            if room[0] > 0 and spaces[room[0]-1][room[1]]//10 == 0:
                text.append(fon.render("?",1,colors[i]))
                textpos.append(text[-1].get_rect(centerx=((size*(room[0]-1))+(1/4*(ipos[i]-1)*size)+(3/4*size)),centery=((size*room[1])+size+yOffset)))
            if room[1] < 8 and spaces[room[0]][room[1]+1]//10 == 0:
                text.append(fon.render("?",1,colors[i]))
                textpos.append(text[-1].get_rect(centerx=((size*room[0])+(1/4*(ipos[i]-1)*size)+(3/4*size)),centery=(((size*(room[1]+1))+size+yOffset))))
            if room[1] > 0 and spaces[room[0]][room[1]-1]//10 == 0:
                text.append(fon.render("?",1,colors[i]))
                textpos.append(text[-1].get_rect(centerx=((size*room[0])+(1/4*(ipos[i]-1)*size)+(3/4*size)),centery=(((size*(room[1]-1))+size+yOffset))))
            for j in range(len(text)):
                win.blit(text[j], textpos[j])
            

def cBg(size, spaces, win):
    yOffset = size//4
    win.fill(Color(255,255,255))
    draw.rect(win,Color(200,255,200),Rect(size/2,size/2+yOffset,size*9,size*9))
    for i in range(9):
        for j in range(9):
            if spaces[i][j]//10 == 0:
                draw.rect(win,Color(150,150,150),Rect(size*i+(size/2),size*j+(size/2)+yOffset,size,size))
            elif spaces[i][j]%10 == 1:
                draw.rect(win,Color(0,0,0),Rect(size*i+(size/2),size*j+(size/2)+yOffset,size,size))
            elif spaces[i][j]%10 == 2:
                draw.rect(win,Color(230,0,0),Rect(size*i+(size/2),size*j+(size/2)+yOffset,size,size))
            elif spaces[i][j]%10 == 3:
                spaces[i][j] -= 3
                draw.rect(win,Color(255,200,0),Rect(size*i+(size/2),size*j+(size/2)+yOffset,size,size))
            elif spaces[i][j]%10 == 4:
                for k in range(10):
                    draw.rect(win,Color(200-(k*20),255-(k*25),200-(k*20)),Rect(size*i+(size/2)+(k*size/20),size*j+(size/2)+(k*size/20)+yOffset,size-(k*size/10),size-(k*size/10)))
            draw.rect(win,Color(0,0,0),Rect(size*i+(size/2),size*j+(size/2)+yOffset,size,size),size//40)

def cDrawArrow(size, pos, d, win):
    yOffset = size//4
    if d[0]=="d":
        #draw.line(win,Color(100,50,50),(size*pos[0]+(size),size*pos[1]+(3/4*size)),(size*pos[0]+(size),size*pos[1]+(3/2*size)),size//8)
        #draw.line(win,Color(100,100,100),(size*pos[0]+(size),size*pos[1]+(3/2*size)),(size*pos[0]+(3/4*size),size*pos[1]+(5/4*size)),size//8)
        #draw.line(win,Color(100,100,100),(size*pos[0]+(size),size*pos[1]+(3/2*size)),(size*pos[0]+(5/4*size),size*pos[1]+(5/4*size)),size//8)
        draw.rect(win,Color(100,50,50),Rect(size*pos[0]+19*size//20,size*pos[1]+7*size//10+yOffset,size//10,4*size//5))
        draw.polygon(win,Color(100,100,100),((size*pos[0]+43*size//40-1,size*pos[1]+3*size//2+yOffset),(size*pos[0]+37*size//40,size*pos[1]+3*size//2+yOffset),(size*pos[0]+size,size*pos[1]+65*size//40+yOffset)))
        draw.polygon(win,Color(50,50,50),((size*pos[0]+38*size//40,size*pos[1]+7*size//10+yOffset),(size*pos[0]+38*size//40,size*pos[1]+8*size//10+yOffset),(size*pos[0]+9*size//10,size*pos[1]+15*size//20+yOffset),(size*pos[0]+9*size//10,size*pos[1]+13*size//20+yOffset)))
        draw.polygon(win,Color(50,50,50),((size*pos[0]+42*size//40,size*pos[1]+7*size//10+yOffset),(size*pos[0]+42*size//40,size*pos[1]+8*size//10+yOffset),(size*pos[0]+44*size//40,size*pos[1]+15*size//20+yOffset),(size*pos[0]+44*size//40,size*pos[1]+13*size//20+yOffset)))
    if d[0]=="u":
        #draw.line(win,Color(100,50,50),(size*pos[0]+(size),size*pos[1]+(5/4*size)),(size*pos[0]+(size),size*pos[1]+(1/2*size)),size//8)
        #draw.line(win,Color(100,100,100),(size*pos[0]+(size),size*pos[1]+(1/2*size)),(size*pos[0]+(3/4*size),size*pos[1]+(3/4*size)),size//8)
        #draw.line(win,Color(100,100,100),(size*pos[0]+(size),size*pos[1]+(1/2*size)),(size*pos[0]+(5/4*size),size*pos[1]+(3/4*size)),size//8)
        draw.rect(win,Color(100,50,50),Rect(size*pos[0]+19*size//20,size*pos[1]+size//2+yOffset,size//10,4*size//5))
        draw.polygon(win,Color(100,100,100),((size*pos[0]+37*size//40,size*pos[1]+size//2+yOffset),(size*pos[0]+43*size//40-1,size*pos[1]+size//2+yOffset),(size*pos[0]+size,size*pos[1]+3*size//8+yOffset)))
        draw.polygon(win,Color(50,50,50),((size*pos[0]+38*size//40,size*pos[1]+13*size//10+yOffset),(size*pos[0]+38*size//40,size*pos[1]+12*size//10+yOffset),(size*pos[0]+36*size//40,size*pos[1]+25*size//20+yOffset),(size*pos[0]+36*size//40,size*pos[1]+27*size//20+yOffset)))
        draw.polygon(win,Color(50,50,50),((size*pos[0]+42*size//40,size*pos[1]+13*size//10+yOffset),(size*pos[0]+42*size//40,size*pos[1]+12*size//10+yOffset),(size*pos[0]+44*size//40,size*pos[1]+25*size//20+yOffset),(size*pos[0]+44*size//40,size*pos[1]+27*size//20+yOffset)))
    if d[0]=="r":
        #draw.line(win,Color(100,50,50),(size*pos[0]+(3/4*size),size*pos[1]+(size)),(size*pos[0]+(3/2*size),size*pos[1]+(size)),size//8)
        #draw.line(win,Color(100,100,100),(size*pos[0]+(3/2*size),size*pos[1]+(size)),(size*pos[0]+(5/4*size),size*pos[1]+(3/4*size)),size//8)
        #draw.line(win,Color(100,100,100),(size*pos[0]+(3/2*size),size*pos[1]+(size)),(size*pos[0]+(5/4*size),size*pos[1]+(5/4*size)),size//8)
        draw.rect(win,Color(100,50,50),Rect(size*pos[0]+7*size//10,size*pos[1]+19*size//20+yOffset,4*size//5,size//10))
        draw.polygon(win,Color(100,100,100),((size*pos[0]+3*size//2,size*pos[1]+37*size//40+yOffset),(size*pos[0]+3*size//2,size*pos[1]+43*size//40-1+yOffset),(size*pos[0]+13*size//8,size*pos[1]+size+yOffset)))
        draw.polygon(win,Color(50,50,50),((size*pos[0]+7*size//10,size*pos[1]+38*size//40+yOffset),(size*pos[0]+8*size//10,size*pos[1]+38*size//40+yOffset),(size*pos[0]+15*size//20,size*pos[1]+36*size//40+yOffset),(size*pos[0]+13*size//20,size*pos[1]+36*size//40+yOffset)))
        draw.polygon(win,Color(50,50,50),((size*pos[0]+7*size//10,size*pos[1]+42*size//40+yOffset),(size*pos[0]+8*size//10,size*pos[1]+42*size//40+yOffset),(size*pos[0]+15*size//20,size*pos[1]+44*size//40+yOffset),(size*pos[0]+13*size//20,size*pos[1]+44*size//40+yOffset)))
    if d[0]=="l":
        #draw.line(win,Color(100,50,50),(size*pos[0]+(5/4*size),size*pos[1]+(size)),(size*pos[0]+(1/2*size),size*pos[1]+(size)),size//8)
        #draw.line(win,Color(100,100,100),(size*pos[0]+(1/2*size),size*pos[1]+(size)),(size*pos[0]+(3/4*size),size*pos[1]+(3/4*size)),size//8)
        #draw.line(win,Color(100,100,100),(size*pos[0]+(1/2*size),size*pos[1]+(size)),(size*pos[0]+(3/4*size),size*pos[1]+(5/4*size)),size//8)
        draw.rect(win,Color(100,50,50),Rect(size*pos[0]+size//2,size*pos[1]+19*size//20+yOffset,4*size//5,size//10))
        draw.polygon(win,Color(100,100,100),((size*pos[0]+size//2,size*pos[1]+37*size//40+yOffset),(size*pos[0]+size//2,size*pos[1]+43*size//40-1+yOffset),(size*pos[0]+3*size//8,size*pos[1]+size+yOffset)))
        draw.polygon(win,Color(50,50,50),((size*pos[0]+13*size//10,size*pos[1]+38*size//40+yOffset),(size*pos[0]+12*size//10,size*pos[1]+38*size//40+yOffset),(size*pos[0]+25*size//20,size*pos[1]+36*size//40+yOffset),(size*pos[0]+27*size//20,size*pos[1]+36*size//40+yOffset)))
        draw.polygon(win,Color(50,50,50),((size*pos[0]+13*size//10,size*pos[1]+42*size//40+yOffset),(size*pos[0]+12*size//10,size*pos[1]+42*size//40+yOffset),(size*pos[0]+25*size//20,size*pos[1]+44*size//40+yOffset),(size*pos[0]+27*size//20,size*pos[1]+44*size//40+yOffset)))

def cDrawFire(size, room, win):
    if room[1]<8:
        cDrawArrow(size,(room[0],room[1]+0.5),"d",win)
    if room[1]>0:
        cDrawArrow(size,(room[0],room[1]-0.5),"u",win)
    if room[0]<8:
        cDrawArrow(size,(room[0]+0.5,room[1]),"r",win)
    if room[0]>0:
        cDrawArrow(size,(room[0]-0.5,room[1]),"l",win)

def cArrowUpdate(size, arrow, win):
    if arrow[2] == "u" and arrow[1]>0:
        nArrow = (arrow[0],arrow[1]-1,arrow[2])
    elif arrow[2] == "d" and arrow[1]<8:
        nArrow = (arrow[0],arrow[1]+1,arrow[2])
    elif arrow[2] == "r" and arrow[0]<8:
        nArrow = (arrow[0]+1,arrow[1],arrow[2])
    elif arrow[2] == "l" and arrow[0]>0:
        nArrow = (arrow[0]-1,arrow[1],arrow[2])
    else:
        nArrow = (arrow[0],arrow[1],arrow[2]+" ")
    return nArrow

def cUI(size, arrows, score, level, win):
    if arrows == 1: aText = "1 arrow"
    elif arrows == 0: aText = "No arrows"
    else: aText = str(arrows)+" arrows"
    face = font.SysFont("freesans",size//3)
    text = [face.render(aText,1,(0,0,0)),
            face.render("Score: "+str(score),1,(0,0,0)),
            face.render("Level "+str(level),1,(0,0,0))]
    textpos = [text[0].get_rect(left=size//2,centery=size//2),
               text[1].get_rect(centerx=5*size,centery=size//2),
               text[2].get_rect(right=19*size//2,centery=size//2)]
    for i in range(len(text)): win.blit(text[i],textpos[i])

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                            Classic Center
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

def classic(size,win):
    yOffset = size//4
    spaces = [[0,0,0,0,0,0,0,0,0],  #NOTE flipped along diagonal
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,10],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],  #0-Empty, 1-Pit, 2-Beast, 3-Gold, 4-Exit
              [0,0,0,0,0,0,0,0,0]]  #1 in tens place - Explored
    room = (4,8)
    level = 1
    score = 0
    bPoints = 150
    firingMode = False
    arrow = False
    arrows = 1
    result = 0
    sel = "l"
    pause = False
    pItem = 0
    highScore = False
    name = ""
    shPress = False

    while True:
        try:
            infile = open("wumpusdata.txt","r")
            lines = []
            for line in infile:
                lines.append(line)
            infile.close()
            uk = eval(lines[0])
            dk = eval(lines[1])
            rk = eval(lines[2])
            lk = eval(lines[3])
            ek = eval(lines[4])
            fk = eval(lines[5])
            break
        except ValueError and IndexError: dataReset()

    pitNum = 8
    exitNum = 1
    beastNum = 0.9
    goldNum = 1
    spaces = cGenFeat(spaces,4,exitNum)
    spaces = cGenFeat(spaces,1,pitNum)
    spaces = cGenFeat(spaces,2,beastNum)
    spaces = cGenFeat(spaces,3,goldNum)

    cBg(size, spaces, win)
    cTestAround(spaces, room, size, win)
    draw.circle(win, Color(0,200,200), (size*room[0]+(size),size*room[1]+(size)+yOffset), size//5)
    cUI(size,arrows,score,level,win)
    display.flip()

    while True:
        update = False
        for item in event.get():
            if item.type == QUIT:
                display.quit()
                sys.exit()
            if item.type == KEYDOWN:
                if highScore:
                    if item.mod & KMOD_SHIFT: shPress = True
                    else: shPress = False
                    if item.key >= 48 and item.key <= 57: name+=key.name(item.key)
                    if item.key == 32: name+=" "
                    if item.key >= 97 and item.key <= 122:
                        if shPress: name+=(key.name(item.key)).capitalize()
                        else: name+=key.name(item.key)
                    if item.key == 8: name = name[:-1]
                    name = name[:8]
                    if item.key == 13:
                        for i in range(len(hLines)):
                            hLines[i] = hLines[i].replace("pholder!",name.ljust(8))
                        outfile = open("wumpusdata.txt","w")
                        for line in hLines: print(str(line),end="",file=outfile)
                    if item.key == K_ESCAPE:
                        for i in range(len(hLines)):
                            hLines[i] = hLines[i].replace("pholder!","No name ")
                        outfile = open("wumpusdata.txt","w")
                        for line in hLlines: print(str(line),end="",file=outfile)
                if result == "death1" or result == "death2": cDeath(result,size,score,sel,win)
                else: update = True
                if item.key == uk:
                    if pause:
                        pItem-=1
                        if pItem < 0: pItem=2
                    elif firingMode:
                        arrow = (room[0],room[1],"u")
                        arrows-=1
                        firingMode = False
                    elif room[1]>0: room = (room[0],room[1]-1)
                if item.key == dk:
                    if pause:
                        pItem+=1
                        if pItem > 2: pItem=0
                    elif firingMode:
                        arrow = (room[0],room[1],"d")
                        arrows-=1
                        firingMode = False
                    elif room[1]<8: room = (room[0],room[1]+1)
                if item.key == rk and not highScore:
                    if result == "death1" or result == "death2":
                        sel = cDeath(result,size,score,"r",win)
                    elif firingMode:
                        arrow = (room[0],room[1],"r")
                        arrows-=1
                        firingMode = False
                    elif not pause and room[0]<8: room = (room[0]+1,room[1])
                if item.key == lk and not highScore:
                    if result == "death1" or result == "death2":
                        sel = cDeath(result,size,score,"l",win)
                    elif firingMode:
                        arrow = (room[0],room[1],"l")
                        arrows-=1
                        firingMode = False
                    elif not pause and room[0]>0: room = (room[0]-1,room[1])
                if item.key == ek and not highScore:
                    if pause:
                        if pItem == 0:
                            pause = False
                            update = True
                        if pItem == 1:
                            newKeys = options(10*size,win)
                            uk, dk, rk, lk, ek, fk, size = eval(newKeys[0]), eval(newKeys[1]), eval(newKeys[2]), eval(newKeys[3]), eval(newKeys[4]), eval(newKeys[5]), int(newKeys[8])//10
                            yOffset = size//4
                        if pItem == 2:
                            return "menu", size, uk, dk, ek
                    elif result == "death1" or result == "death2":
                        if sel == "l":
                            return "restart", size, uk, dk, ek
                        if sel == "r":
                            return "menu", size, uk, dk, ek
                    elif cTestInter(spaces,room) == "0":
                        if pitNum < 20: pitNum*=1.1
                        beastNum*=1.05
                        goldNum*=1.075
                        arrow = 0
                        arrows = 1
                        for i in range(9):
                            for j in range(9):
                                spaces[i][j] = 0
                        spaces = cFullGen(spaces,[0,pitNum,beastNum,goldNum,exitNum])
                        spaces[4][8]+=10
                        room = (4,8)
                        level+=1
                if item.key == fk:
                    if not firingMode and arrows:
                        firingMode = True
                    else:
                        firingMode = False
                if item.key == K_ESCAPE:
                    if highScore: highScore = False
                    elif result == "death1" or result == "death2":
                        return "menu", uk, dk, ek
                    else:
                        if pause:
                            pause = False
                            update = True
                        else:
                            pItem = 0
                            pause = True
                if item.key == 13:
                    if highScore: highScore = False
                if highScore:
                    hsUI(size,name,win)
                if result == "death1" or result == "death2": display.flip()
            """if item.type == KEYUP:
                if item.key == K_RSHIFT or item.key == K_LSHIFT: shPress = False"""
        if pause and update:
            cBg(size,spaces,win)
            draw.circle(win,Color(0,200,200),(size*room[0]+(size),size*room[1]+(size)+yOffset),size//5)
            Pause(size,pItem,win)
            display.flip()
        elif update:
            if arrow:
                if spaces[arrow[0]][arrow[1]]%10 == 2:
                    spaces[arrow[0]][arrow[1]] -= 2
                    score += bPoints
                    arrow = (arrow[0],arrow[1],arrow[2]+" ")
                arrow = cArrowUpdate(size,arrow,win)
            result = cTestInter(spaces,room)
            try: score += int(result)
            except ValueError:
                if result == "death1" or result == "death2":
                    hLines = scoreTest("c",score,0)
                    if hLines: highScore = True
            cBg(size,spaces,win)
            try:
                if room[0] == arrow[0] and room[1] == arrow[1] and arrow[2][1] == " ":
                    arrow = False
                    arrows+=1
                cDrawArrow(size,(arrow[0],arrow[1]),arrow[2],win)
            except:pass
            cTestAround(spaces, room, size, win)

            if firingMode:
                cDrawFire(size,room,win)
            draw.circle(win,Color(0,200,200),(size*room[0]+(size),size*room[1]+(size)+yOffset),size//5)
            cUI(size,arrows,score,level,win)
            display.flip()

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                            New Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""    

def nPitGen(size):
    size = 400
    points = []
    for i in range(25):
        y = (random.random()*5*size//10)+(7*size//20)
        x = (random.random()*8*size//10)+(size//10)
        ang1 = math.atan2(y-(6*size//10),x-(size//2))
        if x > 6*size//10 or x < 4*size//10 or y > 7*size//10 or y < 5*size//10:
            for i in range(len(points)):
                if ang1 < math.atan2(points[i][1]-(6*size//10),points[i][0]-(size//2)):
                    points.insert(i,(x,y))
                    break
                elif i+1 == len(points):
                    points.append((x,y))
            if not points: points.append((x,y))
    triSet = earclip.earclip(points)
    return (points,triSet)

def nPitCollide(size, rm, pPos, randRec, win):
    points,triSet = randRec[rm[0]][rm[1]][rm[2]]
    for i in triSet:
        x1,y1 = i[0][0]*size//400,i[0][1]*size//400
        x2,y2 = i[1][0]*size//400,i[1][1]*size//400
        x3,y3 = i[2][0]*size//400,i[2][1]*size//400
        if earclip.orient((x1,y1),(x2,y2),pPos) == earclip.orient((x2,y2),(x3,y3),pPos) == earclip.orient((x3,y3),(x1,y1),pPos):
            return True
    """for i in range(len(points)):
        p1 = points[i]
        if i+1 == len(points): p2 = points[0]
        else: p2 = points[i+1]
        if math.fabs(p1[0]-p2[0]) < size//50 or math.fabs(p1[1]-p2[1]) < size//50:
            if ((pPos[0] > p1[0]-3 and pPos[0] < p2[0]+3) or (pPos[0] < p1[0]+3 and pPos[0] > p2[0]-3)) and ((pPos[1] > p1[1]-3 and pPos[1] < p2[1]+3) or (pPos[1] < p1[1]+3 and pPos[1] > p2[1]-3)):
                return True
        try:
            sl = (p2[1]-p1[1])/(p2[0]-p1[0])
            yInt = (p1[0]*sl*-1)+p1[1]
            if (pPos[0]*sl)+yInt+3 >= pPos[1] and (pPos[0]*sl)+yInt-3 <= pPos[1] and ((pPos[0] > p1[0]-3 and pPos[0] < p2[0]+3) or (pPos[0] < p1[0]+3 and pPos[0] > p2[0]-3)):
                return True
        except ZeroDivisionError: pass"""

def nBeastGen(size):
    y = int(random.random()*6*400//10+(3*400//10))
    x = int(random.random()*7*400//10+(3*400//20))
    d = [random.randrange(3),random.randrange(3)]
    chase = False
    return [x,y,d,chase,0]

def nBeastDraw(size, b, pPos, pFace, aCharge, aInRoom, inv, win):
    x,y = b[0]*size//400,b[1]*size//400
    if b[2][0] != "s":
        speed = size//400
        #if b[4]: speed = size//200
        if b[2][0]<1:
            b[2][0]=0
            x-=speed
        if b[2][0]>1:
            b[2][0]=2
            x+=speed
        if b[2][1]<1:
            b[2][1]=0
            y-=speed
        if b[2][1]>1:
            b[2][1]=2
            y+=speed
        rChange = random.randrange(0,100)
        if not b[3]:
            if rChange == 99 and not inv[5][0]: b[3] = True
            elif rChange == 98: b[2][0]+=1
            elif rChange == 97: b[2][0]-=1
            elif rChange == 96: b[2][1]+=1
            elif rChange == 95: b[2][1]-=1
            elif rChange == 90 or rChange == 89: inv[5][1]-=random.randrange(6)
            if inv[5][1] < 0:
                inv[5][0]-=1
                inv[5][1]=100
        else:
            if y>pPos[1]:
                b[2][1]-=1
            if y<pPos[1]:
                b[2][1]+=1
            if x>pPos[0]:
                b[2][0]-=1
            if x<pPos[0]:
                b[2][0]+=1
            if x<pPos[0]+size//10 and x>pPos[0]-size//10:
                b[2][0]=1
            if y<pPos[1]+size//16 and y>pPos[1]-size//32:
                b[2][1]=1
        if y > 7*size//8:
            b[2][1]=0
        if y < 13*size//40:
            b[2][1]=2
        if x > (y//6+(4*size//5)-size//16):
            b[2][0]=0
        if x < ((size//5+size//16)-(y//6)):
            b[2][0]=2
    b[0],b[1] = int(x*400/size),int(y*400/size)
    drawOver = []
    for a in aInRoom:
        if a[0][0] > x-size//8 and a[0][0] < x+size//8 and a[0][1] < y and a[0][1] > y - size//4: drawOver.append(a)
    if y >= pPos[1]: nPlayerDraw(size,pPos,pFace,aCharge,aInRoom,win)
    draw.circle(win,Color(230,0,0),(x-3*size//32,y-7*size//32),size//32)
    draw.circle(win,Color(230,0,0),(x+3*size//32+1,y-7*size//32),size//32)
    draw.circle(win,Color(230,0,0),(x-3*size//32,y-1*size//32+1),size//32)
    draw.circle(win,Color(230,0,0),(x+3*size//32+1,y-1*size//32+1),size//32)
    if b[2][0] == "s":
        if int(b[2][-1]) < 1: draw.polygon(win,Color(230,0,0),((x-4*size//32,y-7*size//32),(x-3*size//32,y-8*size//32),(x+3*size//32,y-8*size//32),(x+4*size//32,y-7*size//32),(x+4*size//32,y-size//32),(x+3*size//32,y),(x-3*size//32,y),(x-4*size//32,y-size//32),(x-4*size//32,y-4*size//32),(x-1*size//32,y-5*size//32),(x-4*size//32,y-6*size//32)))
        elif int(b[2][-1]) > 1: draw.polygon(win,Color(230,0,0),((x-4*size//32,y-7*size//32),(x-3*size//32,y-8*size//32),(x+3*size//32,y-8*size//32),(x+4*size//32,y-7*size//32),(x+4*size//32,y-6*size//32),(x+1*size//32,y-5*size//32),(x+4*size//32,y-4*size//32),(x+4*size//32,y-size//32),(x+3*size//32,y),(x-3*size//32,y),(x-4*size//32,y-size//32)))
        else:
            draw.polygon(win,Color(230,0,0),((x-4*size//32,y-7*size//32),(x-3*size//32,y-8*size//32),(x+3*size//32,y-8*size//32),(x+4*size//32,y-7*size//32),(x+4*size//32,y-size//32),(x+3*size//32,y),(x-3*size//32,y),(x-4*size//32,y-size//32)))
            draw.ellipse(win,Color(0,0,0),Rect(x-3*size//32,y-6*size//32,6*size//32,2*size//32))
    elif b[2][0] < 1: draw.polygon(win,Color(230,0,0),((x-4*size//32,y-7*size//32),(x-3*size//32,y-8*size//32),(x+3*size//32,y-8*size//32),(x+4*size//32,y-7*size//32),(x+4*size//32,y-size//32),(x+3*size//32,y),(x-3*size//32,y),(x-4*size//32,y-size//32),(x-4*size//32,y-2*size//32),(x-1*size//32,y-3*size//32),(x-4*size//32,y-4*size//32)))
    elif b[2][0] > 1: draw.polygon(win,Color(230,0,0),((x-4*size//32,y-7*size//32),(x-3*size//32,y-8*size//32),(x+3*size//32,y-8*size//32),(x+4*size//32,y-7*size//32),(x+4*size//32,y-4*size//32),(x+1*size//32,y-3*size//32),(x+4*size//32,y-2*size//32),(x+4*size//32,y-size//32),(x+3*size//32,y),(x-3*size//32,y),(x-4*size//32,y-size//32)))
    else:
        draw.polygon(win,Color(230,0,0),((x-4*size//32,y-7*size//32),(x-3*size//32,y-8*size//32),(x+3*size//32,y-8*size//32),(x+4*size//32,y-7*size//32),(x+4*size//32,y-size//32),(x+3*size//32,y),(x-3*size//32,y),(x-4*size//32,y-size//32)))
        if b[2][1] > 0: draw.ellipse(win,Color(0,0,0),Rect(x-3*size//32,y-4*size//32,6*size//32,2*size//32))
    if b[2][0] == "s":
        if int(b[2][-1]) < 2: draw.polygon(win,Color(0,0,0),((x-25*size//400,y-27*size//400),(x-18*size//400,y-34*size//400),(x-16*size//400,y-32*size//400),(x-23*size//400,y-25*size//400),(x-16*size//400,y-18*size//400),(x-18*size//400,y-16*size//400),(x-25*size//400,y-23*size//400),(x-32*size//400,y-16*size//400),(x-34*size//400,y-18*size//400),(x-27*size//400,y-25*size//400),(x-34*size//400,y-32*size//400),(x-32*size//400,y-34*size//400)))
    elif b[2][0] < 2:
        draw.circle(win,Color(255,255,255),(x-2*size//32,y-6*size//32),size//32)
        if b[2][0] < 1:
            if b[2][1] < 1: draw.circle(win,Color(0,0,0),(x-30*size//400,y-80*size//400),size//64)
            elif b[2][1] > 1: draw.circle(win,Color(0,0,0),(x-30*size//400,y-70*size//400),size//64)
            else: draw.circle(win,Color(0,0,0),(x-32*size//400,y-75*size//400),size//64)
        else:
            if b[2][1] < 1: draw.circle(win,Color(0,0,0),(x-25*size//400,y-82*size//400),size//64)
            elif b[2][1] > 1: draw.circle(win,Color(0,0,0),(x-25*size//400,y-68*size//400),size//64)
            else: draw.circle(win,Color(0,0,0),(x-18*size//400,y-75*size//400),size//64)
    if b[2][0] == "s":
        if int(b[2][-1]) > 0: draw.polygon(win,Color(0,0,0),((x+25*size//400,y-27*size//400),(x+18*size//400,y-34*size//400),(x+16*size//400,y-32*size//400),(x+23*size//400,y-25*size//400),(x+16*size//400,y-18*size//400),(x+18*size//400,y-16*size//400),(x+25*size//400,y-23*size//400),(x+32*size//400,y-16*size//400),(x+34*size//400,y-18*size//400),(x+27*size//400,y-25*size//400),(x+34*size//400,y-32*size//400),(x+32*size//400,y-34*size//400)))
    elif b[2][0] > 0:
        draw.circle(win,Color(255,255,255),(x+2*size//32,y-6*size//32),size//32)
        if b[2][0] > 1:
            if b[2][1] < 1: draw.circle(win,Color(0,0,0),(x+30*size//400,y-80*size//400),size//64)
            elif b[2][1] > 1: draw.circle(win,Color(0,0,0),(x+30*size//400,y-70*size//400),size//64)
            else: draw.circle(win,Color(0,0,0),(x+32*size//400,y-75*size//400),size//64)
        else:
            if b[2][1] < 1: draw.circle(win,Color(0,0,0),(x+25*size//400,y-82*size//400),size//64)
            elif b[2][1] > 1: draw.circle(win,Color(0,0,0),(x+25*size//400,y-68*size//400),size//64)
            else: draw.circle(win,Color(0,0,0),(x+18*size//400,y-75*size//400),size//64)
    if b[4]: draw.polygon(win,Color(250,200,0),((x-20*size//400,y-96*size//400),(x-20*size//400,y-110*size//400),(x-10*size//400,y-100*size//400),(x,y-110*size//400),(x+10*size//400,y-100*size//400),(x+20*size//400,y-110*size//400),(x+20*size//400,y-96*size//400)))
    for a in drawOver:
        nArrowDraw(size, a, win)
        if a in aInRoom: aInRoom.remove(a)
    if y<pPos[1]: nPlayerDraw(size,pPos,pFace,aCharge,aInRoom,win)
    for a in aInRoom: nArrowDraw(size, a, win)
    if x<pPos[0]+size//10 and x>pPos[0]-size//10 and y<pPos[1]+size//16 and y>pPos[1]-size//32 and b[2][0] != "s":
        return True

def nGoldGen(size, amount):
    #if amount > 500: amount=500
    gold = []
    while amount > 0:
        y = (random.random()*(400*amount//1500+400//6))+(-400*amount//3000+31*400//60)
        x = (random.random()*(400*amount//1500+11*400//30))+(-400*amount//3000+19*400//60)
        val = random.randrange(1,6)
        for i in range(len(gold)):
            if y < gold[i][1]:
                gold.insert(i,(x,y,val))
                break
            elif i+1 == len(gold):
                gold.append((x,y,val))
        if not gold: gold.append((x,y,val))
        amount-=val
    return gold

def nGoldDraw(size, gold, pPos, pFace, aCharge, aInRoom, inv, win):
    mGain = 0
    pDrawn = False
    for i in gold:
        x,y = i[0]*size//400,i[1]*size//400
        if pPos[1] < y and not pDrawn:
            nPlayerDraw(size,pPos,pFace,aCharge,aInRoom,win)
            pDrawn = True
        if inv[3][0] and pPos[0] >= x-size//10 and pPos[0] <= x+size//10 and pPos[1] >= y-size//20 and pPos[1] <= y+size//20:
            mGain += i[2]
            gold.insert(gold.index(i),"")
            gold.remove(i)
            if random.random() > 0.70: inv[3][1]-=1
            if inv[3][1] < 0:
                inv[3][0]-=1
                inv[3][1]=100
        elif pPos[0] >= x-size//50 and pPos[0] <= x+size//50 and pPos[1] >= y-size//80 and pPos[1] <= y+size//80:
            mGain += i[2]
            gold.insert(gold.index(i),"")
            gold.remove(i)
        else:
            for j in range(1,i[2]+1):
                draw.ellipse(win,Color(150,120,0),Rect(x-size//40,y-j*size//90,size//20,size//40),size//200)
                draw.ellipse(win,Color(225,190,0),Rect(x-size//40,y-j*size//80,size//20,size//40))
    while True:
        try: gold.remove("")
        except ValueError: break
    if not pDrawn:
        nPlayerDraw(size,pPos,pFace,aCharge,aInRoom,win)
    for a in aInRoom: nArrowDraw(size, a, win)
    if not gold: return str(mGain)
    return mGain

def nExitGen(spaces, rm, randRec, mapOffset):
    typ = 0 #random.randrange(0,2)     #0 rope, 1 ladder - no use ladder?
    mapOffset[rm[0]] = (random.randrange(0,2),random.randrange(0,2))
    dest = (rm[0]+1,rm[1]+mapOffset[rm[0]][0],rm[2]+mapOffset[rm[0]][1])
    spaces[dest[0]][dest[1]][dest[2]] = 5
    randRec[dest[0]][dest[1]][dest[2]] = [typ,rm]
    randRec[rm[0]][rm[1]][rm[2]] = [typ,dest]

def nEndGen(size, spaces, rm, randRec, mapOffset):
    randRec[rm[0]][rm[1]][rm[2]] = [0,(0,0,0)]
    orient = random.randrange(4)
    if orient == 0:
        spaces.append([[5,2,3]])
        randRec.append([[0,0,0]])
        mapOffset[-1] = (-1*rm[1],-1*rm[2])
        randRec[-1][0][0] = [0,(0,0,0)]
        randRec[-1][0][1] = [200,240,[0,1],True,5]
        randRec[-1][0][2] = nGoldGen(size,600)
    elif orient == 1:
        spaces.append([[3,2,5]])
        randRec.append([[0,0,0]])
        mapOffset[-1] = (-1*rm[1],-1*rm[2]+2)
        randRec[-1][0][2] = [0,(0,0,0)]
        randRec[-1][0][1] = [200,240,[2,1],True,5]
        randRec[-1][0][0] = nGoldGen(size,600)
    elif orient == 2:
        spaces.append([[5],[2],[3]])
        randRec.append([[0],[0],[0]])
        mapOffset[-1] = (-1*rm[1],-1*rm[2])
        randRec[-1][0][0] = [0,(0,0,0)]
        randRec[-1][1][0] = [200,240,[1,0],True,5]
        randRec[-1][2][0] = nGoldGen(size,600)
    else:
        spaces.append([[3],[2],[5]])
        randRec.append([[0],[0],[0]])
        mapOffset[-1] = (-1*rm[1]+2,-1*rm[2])
        randRec[-1][2][0] = [0,(0,0,0)]
        randRec[-1][1][0] = [200,240,[1,2],True,5]
        randRec[-1][0][0] = nGoldGen(size,600)

def nExitDraw(size, ex, pPos, pFace, aCharge, aInRoom, win):
    if pPos[1] <= 39*size//80: nPlayerDraw(size,pPos,pFace,aCharge,aInRoom,win)
    for i in range(20):
        draw.rect(win,Color(140-7*i,180-9*i,140-7*i),Rect(7*size//20,size//2+i*size//80,3*size//10,size//80))
    if ex[0] == 0:
        draw.polygon(win,Color(125,125,125),((31*size//60,35*size//80),(29*size//60,35*size//80),(79*size//160,39*size//80),(81*size//160,39*size//80)))
        draw.rect(win,Color(160,120,80),Rect(size//2,35*size//80,size//80,25*size//80))
        draw.circle(win,Color(160,120,80),(size//2,36*size//80),size//60)
        draw.circle(win,Color(125,125,125),(size//2,35*size//80),size//50)
        for i in range(12):
            draw.line(win,Color(100,75,50),(size//2,(37+2*i)*size//80),(41*size//80-1,(75+4*i)*size//160),size//400)
    if ex[0] == 1:
        draw.rect(win,Color(100,75,50),Rect(45*size//100,19*size//40,size//50,11*size//40))
        draw.rect(win,Color(100,75,50),Rect(53*size//100,19*size//40,size//50,11*size//40))
        draw.circle(win,Color(100,75,50),(46*size//100,19*size//40),size//100)
        draw.circle(win,Color(100,75,50),(54*size//100,19*size//40),size//100)
        for i in range(5):
            draw.rect(win,Color(100,75,50),Rect(47*size//100,(10+i)*size//20,3*size//50,3*size//160))
    if pPos[1] > 39*size//80: nPlayerDraw(size,pPos,pFace,aCharge,aInRoom,win)
    for a in aInRoom: nArrowDraw(size, a, win)

def nAExitDraw(size, aex, pPos, pFace, aCharge, aInRoom, win):
    if pPos[1] <= 13*size//20: nPlayerDraw(size,pPos,pFace,aCharge,aInRoom,win)
    while aInRoom:
        if aInRoom[0][0][1] < 10*size//20:
            nArrowDraw(size, aInRoom[0], win)
            aInRoom.pop(0)
        else: break
    if aex[0] == 0:
        draw.rect(win,Color(160,120,80),Rect(size//2,0,size//80,3*size//5))
        draw.circle(win,Color(160,120,80),(size//2,46*size//80),size//100)
        draw.circle(win,Color(160,120,80),(41*size//80,91*size//160),size//100)
        draw.circle(win,Color(160,120,80),(41*size//80,93*size//160),size//100)
        for i in range(23):
            draw.line(win,Color(100,75,50),(size//2,(2*i)*size//80),(41*size//80-1,(1+4*i)*size//160),size//400)
        draw.line(win,Color(140,105,70),(size//2,181*size//320),(83*size//160-1,92*size//160-1),size//400)
        draw.line(win,Color(140,105,70),(81*size//160,91*size//160-1),(41*size//80-1,89*size//160+1),size//400)
        draw.line(win,Color(140,105,70),(size//2,93*size//160+2),(41*size//80-1,94*size//160+1),size//400)
    if aex[0] == 1:
        draw.rect(win,Color(100,75,50),Rect(45*size//100,0,size//50,13*size//20))
        draw.rect(win,Color(100,75,50),Rect(53*size//100,0,size//50,13*size//20))
        draw.circle(win,Color(100,75,50),(46*size//100,13*size//20),size//100)
        draw.circle(win,Color(100,75,50),(54*size//100,13*size//20),size//100)
        for i in range(13):
            draw.rect(win,Color(100,75,50),Rect(47*size//100,(1+4*i)*size//80,3*size//50,3*size//160))
    if pPos[1] > 13*size//20: nPlayerDraw(size,pPos,pFace,aCharge,aInRoom,win)
    for a in aInRoom: nArrowDraw(size, a, win)

def nShopDraw(size, sKeep, rm, pPos, pFace, aCharge, aInRoom, win):
    if rm == (0,1,3):
        draw.polygon(win,Color(50,50,0),((17*size//20,7*size//20),(17*size//20,4*size//20),(19*size//20,9*size//20),(19*size//20,13*size//20)))
        draw.polygon(win,Color(0,0,0),((17*size//20,7*size//20),(17*size//20,4*size//20),(19*size//20,9*size//20),(19*size//20,13*size//20)),size//200)
        draw.rect(win,Color(50,50,0),Rect(7*size//10,5*size//20,3*size//20,size//10))
        draw.rect(win,Color(0,0,0),Rect(7*size//10,5*size//20,3*size//20,size//10),size//200)
        draw.polygon(win,Color(50,50,0),((7*size//10,7*size//20),(7*size//10,5*size//20),(8*size//10,11*size//20),(8*size//10,13*size//20)))
        draw.polygon(win,Color(0,0,0),((7*size//10,7*size//20),(7*size//10,5*size//20),(8*size//10,11*size//20),(8*size//10,13*size//20)),size//200)
        if sKeep == 16:
            draw.rect(win,Color(75,75,0),Rect(33*size//40,8*size//20,size//20,size//8))
            draw.circle(win,Color(75,75,0),(34*size//40,29*size//80),size//40)
        draw.rect(win,Color(50,50,0),Rect(8*size//10,11*size//20,3*size//20,size//10+1))
        draw.rect(win,Color(0,0,0),Rect(8*size//10,11*size//20,3*size//20,size//10+1),size//200)
        draw.polygon(win,Color(50,50,0),((7*size//10,5*size//20),(15*size//20,5*size//20),(17*size//20,11*size//20),(8*size//10,11*size//20)))
        draw.polygon(win,Color(0,0,0),((7*size//10,5*size//20),(15*size//20,5*size//20),(17*size//20,11*size//20),(8*size//10,11*size//20)),size//200)
        if sKeep == 16:
            draw.rect(win,Color(50,50,0),Rect(16*size//20,6*size//20,size//40,5*size//20))
            draw.rect(win,Color(0,0,0),Rect(16*size//20,6*size//20,size//40,5*size//20),size//200)
            draw.polygon(win,Color(50,50,0),((14*size//20,size//20),(36*size//50,size//10),(36*size//50,5*size//20),(14*size//20,5*size//20)))
            draw.polygon(win,Color(0,0,0),((14*size//20,size//20),(36*size//50,size//10),(36*size//50,5*size//20),(14*size//20,5*size//20)),size//200)
            draw.polygon(win,Color(50,50,0),((14*size//20,size//20),(17*size//20,4*size//20),(19*size//20,9*size//20),(16*size//20,6*size//20)))
            draw.polygon(win,Color(0,0,0),((14*size//20,size//20),(17*size//20,4*size//20),(19*size//20,9*size//20),(16*size//20,6*size//20)),size//200)
        else:
            draw.polygon(win,Color(50,50,0),((14*size//20,size//10),(17*size//20,size//10),(18*size//20,8*size//20),(37*size//50,8*size//20)))
            draw.polygon(win,Color(0,0,0),((14*size//20,size//10),(17*size//20,size//10),(18*size//20,8*size//20),(37*size//50,8*size//20)),size//200)
            draw.polygon(win,Color(50,50,0),((38*size//50,5*size//20),(39*size//50,5*size//20),(40*size//50,9*size//20),(39*size//50,9*size//20)))
            draw.polygon(win,Color(0,0,0),((38*size//50,5*size//20),(39*size//50,5*size//20),(40*size//50,9*size//20),(39*size//50,9*size//20)),size//200)
            draw.polygon(win,Color(50,50,0),((17*size//20,10*size//20),(69*size//80,21*size//40),(73*size//80,13*size//40),(18*size//20,6*size//20)))
            draw.polygon(win,Color(0,0,0),((17*size//20,10*size//20),(69*size//80,21*size//40),(73*size//80,13*size//40),(18*size//20,6*size//20)),size//200)
    else:
        x,y = sKeep[0]*size//400,sKeep[1]*size//400
        if pPos[1] <= y: nPlayerDraw(size,pPos,pFace,aCharge,aInRoom,win)
        if sKeep[2] == 0:
            draw.rect(win,Color(75,75,0),Rect(x-9*size//80,y-size//20,size//8,size//20))
            draw.circle(win,Color(75,75,0),(x-12*size//80,y-size//40),size//40)
        if sKeep[2] == 1:
            draw.rect(win,Color(75,75,0),Rect(x-size//40,y-size//8,size//20,size//8))
            draw.circle(win,Color(75,75,0),(x,y-13*size//80),size//40)
        if pPos[1] > y: nPlayerDraw(size,pPos,pFace,aCharge,aInRoom,win)
        for a in aInRoom: nArrowDraw(size, a, win)

def nRoomDraw(size, spaces, rm, randRec, win):
    adjTypes = []
    floorCs = (Color(100,100,100),Color(150,150,150),Color(0,0,0),Color(230,0,0),Color(255,200,0),Color(140,175,140),Color(140,175,140),Color(150,150,150))    #5-Using exit color for antiExit?
    floorC = floorCs[1]
    win.fill(Color(180,225,180))
    draw.polygon(win,floorC,((0,9*size//10),(size-2,9*size//10),(9*size//10,3*size//10),(size//10,3*size//10)))
    draw.polygon(win,Color(0,0,0),((0,9*size//10),(size-2,9*size//10),(9*size//10,3*size//10),(size//10,3*size//10)),size//200)
    draw.line(win,Color(0,0,0),(0,0),(size//10,3*size//10),size//200)
    draw.line(win,Color(0,0,0),(size-2,0),(9*size//10,3*size//10),size//200)
    
    if rm == (0,1,3):               #Shop room - Add more? (bushes/trees)
        win.fill(Color(0,100,0))
        draw.rect(win,Color(200,200,200),Rect(0,0,size,3*size//10))
        draw.line(win,Color(0,0,0),(0,3*size//10),(size,3*size//10),size//200)
        draw.polygon(win,Color(100,100,0),((0,9*size//10),(size-2,9*size//10),(9*size//10,3*size//10),(size//10,3*size//10)))
        draw.polygon(win,Color(0,0,0),((0,9*size//10),(size-2,9*size//10),(9*size//10,3*size//10),(size//10,3*size//10)),size//200)
        draw.polygon(win,floorC,((11*size//20,3*size//10),(9*size//20,3*size//10),(5*size//12,size//10),(7*size//12,size//10)))
        draw.polygon(win,Color(0,0,0),((11*size//20,3*size//10),(9*size//20-1,3*size//10),(5*size//12,size//10),(7*size//12,size//10)),size//200)
        nShopDraw(size,spaces[0][1][3],rm,(200,200),"u",0,[],win)
        return
    
    if rm[2] > 0:
        if spaces[rm[0]][rm[1]][rm[2]-1] < 10: floorC = floorCs[0]
        else: floorC = floorCs[spaces[rm[0]][rm[1]][rm[2]-1]-9]
        draw.polygon(win,floorC,((11*size//20,3*size//10),(9*size//20,3*size//10),(5*size//12,size//10),(7*size//12,size//10)))
        draw.polygon(win,Color(0,0,0),((11*size//20,3*size//10),(9*size//20-1,3*size//10),(5*size//12,size//10),(7*size//12,size//10)),size//200)
        adjTypes.append(spaces[rm[0]][rm[1]][rm[2]-1]%10)
    if rm[2] < len(spaces[rm[0]][rm[1]])-1:
        if spaces[rm[0]][rm[1]][rm[2]+1] < 10: floorC = floorCs[0]
        else: floorC = floorCs[spaces[rm[0]][rm[1]][rm[2]+1]-9]
        if rm == (0,1,2): floorC = Color(100,100,0)
        draw.polygon(win,floorC,((13*size//30,9*size//10),(17*size//30,9*size//10),(3*size//5,31*size//30),(2*size//5,31*size//30)))
        draw.polygon(win,Color(0,0,0),((13*size//30,9*size//10),(17*size//30,9*size//10),(3*size//5-1,31*size//30),(2*size//5,31*size//30)),size//200)
        adjTypes.append(spaces[rm[0]][rm[1]][rm[2]+1]%10)
    if rm[1] > 0:
        if spaces[rm[0]][rm[1]-1][rm[2]] < 10: floorC = floorCs[0]
        else: floorC = floorCs[spaces[rm[0]][rm[1]-1][rm[2]]-9]
        draw.polygon(win,floorC,((size//15+1,5*size//10),(size//24+1,13*size//20),(-1*size//20,6*size//10),(-1*size//20,3*size//10)))
        draw.polygon(win,Color(0,0,0),((size//15+1,5*size//10),(size//24+1,13*size//20),(-1*size//20,6*size//10),(-1*size//20,3*size//10)),size//200)
        adjTypes.append(spaces[rm[0]][rm[1]-1][rm[2]]%10)
    if rm[1] < len(spaces[rm[0]])-1:
        if spaces[rm[0]][rm[1]+1][rm[2]] < 10: floorC = floorCs[0]
        else: floorC = floorCs[spaces[rm[0]][rm[1]+1][rm[2]]-9]
        draw.polygon(win,floorC,((14*size//15+1,5*size//10),(23*size//24,13*size//20),(21*size//20,6*size//10),(21*size//20,3*size//10)))
        draw.polygon(win,Color(0,0,0),((14*size//15,5*size//10),(23*size//24-1,13*size//20),(21*size//20,6*size//10),(21*size//20,3*size//10)),size//200)
        adjTypes.append(spaces[rm[0]][rm[1]+1][rm[2]]%10)
    if spaces[rm[0]][rm[1]][rm[2]]%10 == 1:
        if not randRec[rm[0]][rm[1]][rm[2]]:
            randRec[rm[0]][rm[1]][rm[2]] = nPitGen(size)
        pitPoints = []
        for i in randRec[rm[0]][rm[1]][rm[2]][0]:
            pitPoints.append((i[0]*size//400,i[1]*size//400))
        draw.polygon(win,Color(0,0,0),pitPoints)
    if spaces[rm[0]][rm[1]][rm[2]]%10 == 2:
        if not randRec[rm[0]][rm[1]][rm[2]]:
            randRec[rm[0]][rm[1]][rm[2]] = nBeastGen(size)
    if spaces[rm[0]][rm[1]][rm[2]]%10 == 3:
        if not randRec[rm[0]][rm[1]][rm[2]]:
            randRec[rm[0]][rm[1]][rm[2]] = nGoldGen(size,50+(20*rm[0]))
    
    face = font.SysFont("freesans",size//30)
    text = []
    if 1 in adjTypes: text.append(face.render("A cold breeze blows through the room",1,(0,0,0)))
    if 2 in adjTypes: text.append(face.render("A foul stench permeates the air",1,(230,0,0)))
    if 3 in adjTypes: text.append(face.render("A bright glittering is visible from the corner of your eye",1,(255,200,0)))
    textpos = []
    for i in range(len(text)):
        textpos.append(text[i].get_rect(centerx=size//2,centery=(size//80+1+i*size//30)))
        win.blit(text[i],textpos[i])

def nRoomSwitch(d, size, spaces, rm, pPos, mapOffset):
    if d == "u":
        if rm[2] > 0 and pPos[1] < 27*size//80 and pPos[0] > 9*size//20 and pPos[0] < 11*size//20:
            if spaces[rm[0]][rm[1]][rm[2]] < 10: spaces[rm[0]][rm[1]][rm[2]]+=10
            rm = (rm[0],rm[1],rm[2]-1)
            pPos = (pPos[0],69*size//80)
    if rm == (0,1,3):
        return rm, pPos
    elif d == "d":
        if rm[2] < len(spaces[rm[0]][rm[1]])-1 and pPos[1] > 69*size//80 and pPos[0] > 13*size//30 and pPos[0] < 17*size//30:
            if spaces[rm[0]][rm[1]][rm[2]] < 10: spaces[rm[0]][rm[1]][rm[2]]+=10
            rm = (rm[0],rm[1],rm[2]+1)
            pPos = (pPos[0],27*size//80)
    elif d == "l":
        if rm[1] > 0 and pPos[0] < ((17*size//80)-(pPos[1]//6)) and pPos[1] > 5*size//10 and pPos[1] < 13*size//20:
            if spaces[rm[0]][rm[1]][rm[2]] < 10: spaces[rm[0]][rm[1]][rm[2]]+=10
            rm = (rm[0],rm[1]-1,rm[2])
            pPos = (size-pPos[0],pPos[1])
    elif d == "r":
        if rm[1] < len(spaces[rm[0]])-1 and pPos[0] > ((63*size//80)+(pPos[1]//6)) and pPos[1] > 5*size//10 and pPos[1] < 13*size//20:
            if spaces[rm[0]][rm[1]][rm[2]] < 10: spaces[rm[0]][rm[1]][rm[2]]+=10
            rm = (rm[0],rm[1]+1,rm[2])
            pPos = (size-pPos[0],pPos[1])
    elif d == "f":
        if rm[0] < len(spaces)-2 or spaces[rm[0]][rm[1]][rm[2]]%10 == 4:
            if spaces[rm[0]][rm[1]][rm[2]] < 10: spaces[rm[0]][rm[1]][rm[2]]+=10
            rm = (rm[0]+1,rm[1]+mapOffset[rm[0]][0],rm[2]+mapOffset[rm[0]][1])
    elif d == "ae":
        if rm[0] > 0:
            if spaces[rm[0]][rm[1]][rm[2]] < 10: spaces[rm[0]][rm[1]][rm[2]]+=10
            rm = (rm[0]-1,rm[1]-mapOffset[rm[0]-1][0],rm[2]-mapOffset[rm[0]-1][1])
    return rm, pPos

def nPlayerDraw(size,pPos,pFace,aCharge,aInRoom,win):   #plus charging arrows
    while aInRoom:
        if aInRoom[0][0][1] < pPos[1]-size//10:
            nArrowDraw(size, aInRoom[0], win)
            aInRoom.pop(0)
        else: break
    if pFace == "fatal":
        if pPos[0] <= size//2:
            draw.rect(win,Color(0,200,200),Rect(pPos[0]-size//40,pPos[1]-size//20,size//8,size//20))
            draw.circle(win,Color(0,200,200),(pPos[0]+11*size//80,pPos[1]-size//40),size//40)
        else:
            draw.rect(win,Color(0,200,200),Rect(pPos[0]-4*size//40,pPos[1]-size//20,size//8,size//20))
            draw.circle(win,Color(0,200,200),(pPos[0]-11*size//80,pPos[1]-size//40),size//40)
        return
    if pFace == "u":
        if aCharge:
            draw.rect(win,Color(100,50,50),Rect(pPos[0]+4*size//400,pPos[1]-70*size//400+aCharge*size//4000,size//100,4*size//50))
            draw.polygon(win,Color(100,100,100),((pPos[0]+3*size//400,pPos[1]-70*size//400+aCharge*size//4000),(pPos[0]+9*size//400-1,pPos[1]-70*size//400+aCharge*size//4000),(pPos[0]+6*size//400,pPos[1]-15*size//80+aCharge*size//4000)))
            draw.polygon(win,Color(50,50,50),((pPos[0]+4*size//400,pPos[1]+aCharge*size//4000-38*size//400),(pPos[0]+4*size//400,pPos[1]+aCharge*size//4000-42*size//400),(pPos[0]+2*size//400,pPos[1]+aCharge*size//4000-40*size//400),(pPos[0]+2*size//400,pPos[1]+aCharge*size//4000-36*size//400)))
            draw.polygon(win,Color(50,50,50),((pPos[0]+8*size//400,pPos[1]+aCharge*size//4000-38*size//400),(pPos[0]+2*size//100,pPos[1]+aCharge*size//4000-42*size//400),(pPos[0]+10*size//400,pPos[1]+aCharge*size//4000-40*size//400),(pPos[0]+10*size//400,pPos[1]+aCharge*size//4000-36*size//400)))
            draw.rect(win,Color(100,75,50),Rect(pPos[0]+2*size//400,pPos[1]-60*size//400,3*size//400,10*size//400))
            draw.line(win,Color(0,0,0),(pPos[0]+3*size//400,pPos[1]-59*size//400),(pPos[0]+6*size//400,pPos[1]-38*size//400+aCharge*size//4000),size//400)
        else:
            draw.line(win,Color(0,0,0),(pPos[0]+20*size//400-1,pPos[1]-5*size//80),(pPos[0]-1,pPos[1]-9*size//80),size//400)
            draw.polygon(win,Color(100,75,50),((pPos[0]+21*size//400,pPos[1]-23*size//400),(pPos[0]+19*size//400,pPos[1]-27*size//400),(pPos[0]+10*size//400,pPos[1]-27*size//400),(pPos[0]+2*size//400,pPos[1]-35*size//400),(pPos[0]+2*size//400,pPos[1]-44*size//400),(pPos[0]-2*size//400,pPos[1]-46*size//400),(pPos[0]-2*size//400,pPos[1]-33*size//400),(pPos[0]+8*size//400,pPos[1]-23*size//400)))
    if pFace == "l":
        if aCharge:
            draw.line(win,Color(0,0,0),(pPos[0],pPos[1]-12*size//80+size//200),(pPos[0]+aCharge*size//4000,pPos[1]-9*size//80+size//200),size//400)
            draw.line(win,Color(0,0,0),(pPos[0],pPos[1]-6*size//80+size//200),(pPos[0]+aCharge*size//4000,pPos[1]-9*size//80+size//200),size//400)
            draw.polygon(win,Color(100,75,50),((pPos[0]+size//400,pPos[1]-56*size//400),(pPos[0]+size//400,pPos[1]-60*size//400),(pPos[0]-9*size//400,pPos[1]-54*size//400),(pPos[0]-12*size//400,pPos[1]-44*size//400),(pPos[0]-9*size//400,pPos[1]-32*size//400),(pPos[0]+size//400,pPos[1]-26*size//400),(pPos[0]+size//400,pPos[1]-30*size//400),(pPos[0]-6*size//400,pPos[1]-35*size//400),(pPos[0]-8*size//400,pPos[1]-44*size//400),(pPos[0]-6*size//400,pPos[1]-51*size//400)))
            draw.rect(win,Color(100,50,50),Rect(pPos[0]-size//10+aCharge*size//4000,pPos[1]-9*size//80,size//10,size//100))
            draw.polygon(win,Color(100,100,100),((pPos[0]+aCharge*size//4000-size//10,pPos[1]-46*size//400),(pPos[0]+aCharge*size//4000-size//10,pPos[1]-40*size//400-1),(pPos[0]+aCharge*size//4000-9*size//80,pPos[1]-43*size//400)))
            draw.polygon(win,Color(50,50,50),((pPos[0]+aCharge*size//4000,pPos[1]-9*size//80),(pPos[0]+aCharge*size//4000-size//100,pPos[1]-9*size//80),(pPos[0]+aCharge*size//4000-size//200,pPos[1]-47*size//400),(pPos[0]+aCharge*size//4000+size//200,pPos[1]-47*size//400)))
            draw.polygon(win,Color(50,50,50),((pPos[0]+aCharge*size//4000,pPos[1]-41*size//400),(pPos[0]+aCharge*size//4000-size//100,pPos[1]-41*size//400),(pPos[0]+aCharge*size//4000-size//200,pPos[1]-39*size//400),(pPos[0]+aCharge*size//4000+size//200,pPos[1]-39*size//400)))
        else:
            draw.line(win,Color(0,0,0),(pPos[0]-1,pPos[1]-5*size//80),(pPos[0]-20*size//400-1,pPos[1]-9*size//80),size//400)
            draw.polygon(win,Color(100,75,50),((pPos[0]+size//400,pPos[1]-23*size//400),(pPos[0]-size//400,pPos[1]-27*size//400),(pPos[0]-10*size//400,pPos[1]-27*size//400),(pPos[0]-18*size//400,pPos[1]-35*size//400),(pPos[0]-18*size//400,pPos[1]-44*size//400),(pPos[0]-22*size//400,pPos[1]-46*size//400),(pPos[0]-22*size//400,pPos[1]-33*size//400),(pPos[0]-12*size//400,pPos[1]-23*size//400)))
    draw.rect(win,Color(0,200,200),Rect(pPos[0]-size//40,pPos[1]-size//8,size//20,size//8))
    draw.circle(win,Color(0,200,200),(pPos[0],pPos[1]-13*size//80),size//40)
    if pFace == "d":
        if aCharge:
            draw.rect(win,Color(100,75,50),Rect(pPos[0]-5*size//400,pPos[1]-20*size//400,3*size//400,10*size//400))
            draw.rect(win,Color(100,50,50),Rect(pPos[0]-size//50,pPos[1]-aCharge*size//4000-size//10,size//100,4*size//50))
            draw.polygon(win,Color(100,100,100),((pPos[0]-3*size//400-1,pPos[1]-aCharge*size//4000-size//50),(pPos[0]-9*size//400,pPos[1]-aCharge*size//4000-size//50),(pPos[0]-6*size//400,pPos[1]-aCharge*size//4000-3*size//400)))
            draw.polygon(win,Color(50,50,50),((pPos[0]-size//50,pPos[1]-aCharge*size//4000-size//10),(pPos[0]-size//50,pPos[1]-aCharge*size//4000-9*size//100),(pPos[0]-size//40,pPos[1]-aCharge*size//4000-19*size//200),(pPos[0]-size//40,pPos[1]-aCharge*size//4000-21*size//200)))
            draw.polygon(win,Color(50,50,50),((pPos[0]-size//100,pPos[1]-aCharge*size//4000-size//10),(pPos[0]-size//100,pPos[1]-aCharge*size//4000-9*size//100),(pPos[0]-size//200,pPos[1]-aCharge*size//4000-19*size//200),(pPos[0]-size//200,pPos[1]-aCharge*size//4000-21*size//200)))
            draw.line(win,Color(0,0,0),(pPos[0]-4*size//400,pPos[1]-39*size//400),(pPos[0]-6*size//400,pPos[1]-aCharge*size//4000-40*size//400),size//400)
            draw.rect(win,Color(100,75,50),Rect(pPos[0]-5*size//400,pPos[1]-40*size//400,3*size//400,20*size//400))
        else:
            draw.line(win,Color(0,0,0),(pPos[0]-4*size//80,pPos[1]-5*size//80),(pPos[0],pPos[1]-9*size//80),size//400)
            draw.polygon(win,Color(100,75,50),((pPos[0]-21*size//400,pPos[1]-23*size//400),(pPos[0]-19*size//400,pPos[1]-27*size//400),(pPos[0]-10*size//400,pPos[1]-27*size//400),(pPos[0]-2*size//400,pPos[1]-35*size//400),(pPos[0]-2*size//400,pPos[1]-44*size//400),(pPos[0]+2*size//400,pPos[1]-46*size//400),(pPos[0]+2*size//400,pPos[1]-33*size//400),(pPos[0]-8*size//400,pPos[1]-23*size//400)))
    if pFace == "r":
        if aCharge:
            draw.line(win,Color(0,0,0),(pPos[0],pPos[1]-10*size//80+size//200),(pPos[0]-aCharge*size//4000,pPos[1]-7*size//80+size//200),size//400)
            draw.line(win,Color(0,0,0),(pPos[0],pPos[1]-4*size//80+size//200),(pPos[0]-aCharge*size//4000,pPos[1]-7*size//80+size//200),size//400)
            draw.polygon(win,Color(100,75,50),((pPos[0]-size//400,pPos[1]-46*size//400),(pPos[0]-size//400,pPos[1]-50*size//400),(pPos[0]+9*size//400,pPos[1]-44*size//400),(pPos[0]+12*size//400,pPos[1]-34*size//400),(pPos[0]+9*size//400,pPos[1]-22*size//400),(pPos[0]-size//400,pPos[1]-16*size//400),(pPos[0]-size//400,pPos[1]-20*size//400),(pPos[0]+6*size//400,pPos[1]-25*size//400),(pPos[0]+8*size//400,pPos[1]-34*size//400),(pPos[0]+6*size//400,pPos[1]-41*size//400)))
            draw.rect(win,Color(100,50,50),Rect(pPos[0]-aCharge*size//4000,pPos[1]-7*size//80,size//10,size//100))
            draw.polygon(win,Color(100,100,100),((pPos[0]-aCharge*size//4000+size//10,pPos[1]-9*size//100),(pPos[0]-aCharge*size//4000+size//10,pPos[1]-3*size//40-1),(pPos[0]-aCharge*size//4000+9*size//80,pPos[1]-33*size//400)))
            draw.polygon(win,Color(50,50,50),((pPos[0]-aCharge*size//4000,pPos[1]-7*size//80),(pPos[0]-aCharge*size//4000+size//100,pPos[1]-7*size//80),(pPos[0]-aCharge*size//4000+size//200,pPos[1]-37*size//400),(pPos[0]-aCharge*size//4000-size//200,pPos[1]-37*size//400)))
            draw.polygon(win,Color(50,50,50),((pPos[0]-aCharge*size//4000,pPos[1]-31*size//400),(pPos[0]-aCharge*size//4000+size//100,pPos[1]-31*size//400),(pPos[0]-aCharge*size//4000+size//200,pPos[1]-29*size//400),(pPos[0]-aCharge*size//4000-size//200,pPos[1]-29*size//400)))
        else:
            draw.line(win,Color(0,0,0),(pPos[0],pPos[1]-5*size//80),(pPos[0]+size//20,pPos[1]-9*size//80),size//400)
            draw.polygon(win,Color(100,75,50),((pPos[0]-size//400,pPos[1]-23*size//400),(pPos[0]+size//400,pPos[1]-27*size//400),(pPos[0]+10*size//400,pPos[1]-27*size//400),(pPos[0]+18*size//400,pPos[1]-35*size//400),(pPos[0]+18*size//400,pPos[1]-44*size//400),(pPos[0]+22*size//400,pPos[1]-46*size//400),(pPos[0]+22*size//400,pPos[1]-33*size//400),(pPos[0]+12*size//400,pPos[1]-23*size//400)))

def nArrowUpdate(spaces,randRec,aTracker,pPos,rm,size,pause,win):
    inRoom = []
    pickup = []
    spoils = [0,0]
    speed = 4*size//400
    for a in aTracker:  #each a is (pos, dir, rm)
        if a[1] == "u" and not pause:
            a[0][1]-=speed
            if a[0][1] < 2*size//10 or a[0][1] < 6*((4*size//40)-pPos[0]) or a[0][1] < 6*(a[0][0]-(35*size//40)):
                if a[0][0] > 13*size//30 and a[0][0] < 17*size//30 and a[2][2]>0:
                    a[2] = (a[2][0],a[2][1],a[2][2]-1)
                    a[0][1] = 9*size//10
                else: a[1]+=" "
        if a[1] == "d" and not pause:
            a[0][1]+=speed
            if a[2] == (0,1,2) and a[0][1] > 9*size//10:
                a[0][1] = 73*size//80
                a[1]+=" "
            if a[0][1] > 37*size//40:
                if a[0][0] > 13*size//30 and a[0][0] < 17*size//30 and a[2][2]<len(spaces[a[2][0]][a[2][1]])-1 and a[2] != (0,1,2):
                    a[2] = (a[2][0],a[2][1],a[2][2]+1)
                    a[0][1] = 3*size//10
                else: a[1]+=" "
        if a[1] == "l" and not pause:
            a[0][0]-=speed
            if a[0][0] < ((size//10)-(a[0][1]//6)):
                if a[0][1] > 17*size//40 and a[0][1] < 25*size//40 and a[2][1]>0:
                    a[2] = (a[2][0],a[2][1]-1,a[2][2])
                    a[0][0] = size-a[0][0]
                else: a[1]+=" "
        if a[1] == "r" and not pause:
            a[0][0]+=speed
            if a[0][0] > (a[0][1]//6+(9*size//10)):
                if a[0][1] > 17*size//40 and a[0][1] < 25*size//40 and a[2][1]<len(spaces[a[2][0]])-1:
                    a[2] = (a[2][0],a[2][1]+1,a[2][2])
                    a[0][0] = size-a[0][0]
                else: a[1]+=" "
        if rm == a[2]:
            if len(a[1]) > 1 and (a[1][0] == "u" or a[1][0] == "d") and pPos[0]>a[0][0]-4*size//80 and pPos[0]<a[0][0]+4*size//80 and pPos[1]>a[0][1]-3*size//40 and pPos[1]<a[0][1]+7*size//40:
                pickup.append(a)
            elif len(a[1]) > 1 and (a[1][0] == "l" or a[1][0] == "r") and pPos[0]>a[0][0]-5*size//40 and pPos[0]<a[0][0]+5*size//40 and pPos[1]>a[0][1]+5*size//80 and pPos[1]<a[0][1]+7*size//80:
                pickup.append(a)
            elif len(a[1]) > 1 and a[1][0] == "u" and (a[0][0] > 9*size//10 or a[0][0] < size//10) and pPos[0]>a[0][0]-6*size//80 and pPos[0]<a[0][0]+6*size//80 and pPos[1]>a[0][1]-3*size//40 and pPos[1]<a[0][1]+7*size//40:
                pickup.append(a)
            for i in range(len(inRoom)):
                if a[0][1] < inRoom[i][0][1]:
                    inRoom.insert(i,a)
                    break
                if i+1 == len(inRoom): inRoom.append(a)
            if not inRoom: inRoom.append(a)
            #nArrowDraw(size, a, win)
        if spaces[a[2][0]][a[2][1]][a[2][2]]%10 == 2:
            if not randRec[a[2][0]][a[2][1]][a[2][2]]:
                randRec[a[2][0]][a[2][1]][a[2][2]] = nBeastGen(size)
            b = randRec[a[2][0]][a[2][1]][a[2][2]]
            bx = b[0]*size//400
            by = b[1]*size//400
            if "b" in a[1] and b[4] and rm == a[2]:
                if b[2][0] > 1:
                    a[0][0]+=size//400
                if b[2][0] < 1:
                    a[0][0]-=size//400
                if b[2][1] > 1:
                    a[0][1]+=size//400
                if b[2][1] < 1:
                    a[0][1]-=size//400
            if a[0][0] < bx+size//8 and a[0][0] > bx-size//8 and a[0][1] < by and a[0][1] > by-size//4 and b[2][0] != "s" and b[4] <= 0:
                if b[2][0] < 1: b[2] = "stopped0"
                elif b[2][0] > 1: b[2] = "stopped2"
                else: b[2] = "stopped1"
                spoils[0] += 1
            if ((a[1] == "l" or a[1] == "r") and a[0][0] < bx+size//32 and a[0][0] > bx-size//32 and a[0][1] < by and a[0][1] > by-size//4) or ((a[1] == "u" or a[1] == "d") and a[0][1] < by-3*size//32 and a[0][1] > by-5*size//32 and a[0][0] < bx+size//8 and a[0][0] > bx-size//8):
                a[1]+=" "
                if b[4] > 0:
                    if b[4] == 1: spoils[1]+=250
                    b[4]-=1
                    a[1]+="b"
    aPickedup = 0    
    while pickup:
        aTracker.remove(pickup[0])
        pickup.remove(pickup[0])
        aPickedup+=1
    return aPickedup, inRoom, spoils

def nArrowDraw(size, a, win):
    if a[1][0] == "u":
        draw.rect(win,Color(100,50,50),Rect(a[0][0]-size//200,a[0][1],size//100,4*size//50))
        draw.polygon(win,Color(100,100,100),((a[0][0]-3*size//400,a[0][1]),(a[0][0]+3*size//400-1,a[0][1]),(a[0][0],a[0][1]-size//80)))
        draw.polygon(win,Color(50,50,50),((a[0][0]-2*size//400,a[0][1]+8*size//100),(a[0][0]-2*size//400,a[0][1]+7*size//100),(a[0][0]-4*size//400,a[0][1]+15*size//200),(a[0][0]-4*size//400,a[0][1]+17*size//200)))
        draw.polygon(win,Color(50,50,50),((a[0][0]+2*size//400,a[0][1]+8*size//100),(a[0][0]+2*size//400,a[0][1]+7*size//100),(a[0][0]+4*size//400,a[0][1]+15*size//200),(a[0][0]+4*size//400,a[0][1]+17*size//200)))
    if a[1][0] == "d":
        draw.rect(win,Color(100,50,50),Rect(a[0][0]-size//200,a[0][1]-4*size//50,size//100,4*size//50))
        draw.polygon(win,Color(100,100,100),((a[0][0]+3*size//400-1,a[0][1]),(a[0][0]-3*size//400,a[0][1]),(a[0][0],a[0][1]+5*size//400)))
        draw.polygon(win,Color(50,50,50),((a[0][0]-2*size//400,a[0][1]-4*size//50),(a[0][0]-2*size//400,a[0][1]-7*size//100),(a[0][0]-size//100,a[0][1]-15*size//200),(a[0][0]-size//100,a[0][1]-17*size//200)))
        draw.polygon(win,Color(50,50,50),((a[0][0]+2*size//400,a[0][1]-4*size//50),(a[0][0]+2*size//400,a[0][1]-7*size//100),(a[0][0]+4*size//400,a[0][1]-15*size//200),(a[0][0]+4*size//400,a[0][1]-17*size//200)))
    if a[1][0] == "l":
        draw.rect(win,Color(100,50,50),Rect(a[0][0],a[0][1]-size//200,size//10,size//100))
        draw.polygon(win,Color(100,100,100),((a[0][0],a[0][1]-3*size//400),(a[0][0],a[0][1]+3*size//400-1),(a[0][0]-size//80,a[0][1])))
        draw.polygon(win,Color(50,50,50),((a[0][0]+size//10,a[0][1]-2*size//400),(a[0][0]+9*size//100,a[0][1]-2*size//400),(a[0][0]+19*size//200,a[0][1]-4*size//400),(a[0][0]+21*size//200,a[0][1]-4*size//400)))
        draw.polygon(win,Color(50,50,50),((a[0][0]+size//10,a[0][1]+2*size//400),(a[0][0]+9*size//100,a[0][1]+2*size//400),(a[0][0]+19*size//200,a[0][1]+4*size//400),(a[0][0]+21*size//200,a[0][1]+4*size//400)))
    if a[1][0] == "r":
        draw.rect(win,Color(100,50,50),Rect(a[0][0]-size//10,a[0][1]-size//200,size//10,size//100))
        draw.polygon(win,Color(100,100,100),((a[0][0],a[0][1]-3*size//400),(a[0][0],a[0][1]+3*size//400-1),(a[0][0]+size//80,a[0][1])))
        draw.polygon(win,Color(50,50,50),((a[0][0]-size//10,a[0][1]-2*size//400),(a[0][0]-9*size//100,a[0][1]-2*size//400),(a[0][0]-19*size//200,a[0][1]-4*size//400),(a[0][0]-21*size//200,a[0][1]-4*size//400)))
        draw.polygon(win,Color(50,50,50),((a[0][0]-size//10,a[0][1]+2*size//400),(a[0][0]-9*size//100,a[0][1]+2*size//400),(a[0][0]-19*size//200,a[0][1]+4*size//400),(a[0][0]-21*size//200,a[0][1]+4*size//400)))    

def nMapGen(size, spaces, randRec, mapOffset):
    genNums = [0,2,0.76,1,1]
    numScale = [0,1.55,1.3,1.4,1]
    for i in range(len(spaces)):
        for j in (4,1,2,3):
            amount = genNums[j]
            attempts = 3*amount
            while amount > 0 and attempts > 0:
                x = random.randrange(len(spaces[i]))
                y = random.randrange(len(spaces[i][x]))
                if spaces[i][x][y] == 0:
                    spaces[i][x][y] = j
                    amount-=1
                    """if i == 0 and x == 1 and y == 3:
                        spaces[i][x][y] = 0
                        amount+=1"""
                    if j == 4:
                        if i<len(spaces)-1:
                            nExitGen(spaces,(i,x,y),randRec,mapOffset)
                        elif i == len(spaces)-1:
                            nEndGen(size,spaces,(i,x,y),randRec,mapOffset)
                        else: spaces[i][x][y] = 0
                if j != 4:
                    attempts-=1
            genNums[j]*=numScale[j]
    sKeep = False
    while not sKeep:
        x = random.randrange(4)
        y = random.randrange(4)
        if spaces[1][x][y] == 0:
            spaces[1][x][y] = 6
            randRec[1][x][y]=[int((random.random()*6*400/10)+(2*400//10)),int((random.random()*5*400//10)+(7*400//20)),0]
            sKeep = True

def nShopUI(size, item, win):
    draw.rect(win,Color(75,75,0),Rect(3*size//40,4*size//40,16*size//40,31*size//40),size//20)
    draw.rect(win,Color(75,75,0),Rect(3*size//40,4*size//40,16*size//40,31*size//40))
    draw.circle(win,Color(75,75,0),(3*size//40,4*size//40),size//40-1)
    draw.circle(win,Color(75,75,0),(19*size//40,4*size//40),size//40-1)
    draw.circle(win,Color(75,75,0),(3*size//40,35*size//40),size//40-1)
    draw.circle(win,Color(75,75,0),(19*size//40,35*size//40),size//40-1)
    
    face = font.SysFont("freesans",size//20)
    tColors = [[0,0,0]]*6
    try: tColors[item] = [0,150,150]
    except TypeError: tColors[int(item)] = [200,0,0]
    text = [face.render("Exit",1,tColors[0]),
            face.render("Extra",1,tColors[1]),
            face.render("Arrow",1,tColors[1]),
            face.render("Health",1,tColors[2]),
            face.render("Potion",1,tColors[2]),
            face.render("Gold",1,tColors[3]),
            face.render("Magnet",1,tColors[3]),
            face.render("Umbrella",1,tColors[4]),
            face.render("Wumpus",1,tColors[5]),
            face.render("Repellant",1,tColors[5]),
            face.render("50",1,tColors[1]),
            face.render("100",1,tColors[2]),
            face.render("130",1,tColors[3]),
            face.render("200",1,tColors[4]),
            face.render("250",1,tColors[5])]
    textpos = [text[0].get_rect(centerx=11*size//40,top=33*size//40),
               text[1].get_rect(left=4*size//40,top=5*size//40),
               text[2].get_rect(left=4*size//40,top=7*size//40),
               text[3].get_rect(left=4*size//40,top=10*size//40),
               text[4].get_rect(left=4*size//40,top=12*size//40),
               text[5].get_rect(left=4*size//40,top=15*size//40),
               text[6].get_rect(left=4*size//40,top=17*size//40),
               text[7].get_rect(left=4*size//40,top=22*size//40),
               text[8].get_rect(left=4*size//40,top=25*size//40),
               text[9].get_rect(left=4*size//40,top=27*size//40),
               text[10].get_rect(right=18*size//40,top=7*size//40),
               text[11].get_rect(right=18*size//40,top=12*size//40),
               text[12].get_rect(right=18*size//40,top=17*size//40),
               text[13].get_rect(right=18*size//40,top=22*size//40),
               text[14].get_rect(right=18*size//40,top=27*size//40)]
    for i in range(15):
        win.blit(text[i],textpos[i])

def nUI(size, inv, money, health, win):
    h = size*health//800
    draw.rect(win,Color(230,0,0),Rect(size//40,37*size//40,size//8,size//20))
    if h > 0: draw.rect(win,Color(0,200,200),Rect(size//40,37*size//40,h,size//20))
    face = font.SysFont("freesans",size//20)
    text = [face.render("Gold: "+str(money),1,(255,200,0))]
    textpos = [text[0].get_rect(left=13*size//80,centery=19*size//20)]
    offset = 0
    countFace = font.SysFont("freesans",size//40)
    for i in range(len(inv)):
        #draw.rect(win,Color(200,200,200),Rect(49*size//80+offset,73*size//80,3*size//40,3*size//40))
        #draw.rect(win,Color(220,220,220),Rect(25*size//40+offset,37*size//40,2*size//40,2*size//40)) #Probably Remove
        if i == 1 or inv[i][0] > 1:
            text.append(countFace.render(str(inv[i][0]),1,(0,0,0)))
            textpos.append(text[-1].get_rect(right=55*size//80+offset,bottom=79*size//80))
        if i == 1:
            draw.polygon(win,Color(100,50,50),((25*size//40+offset,39*size//40-size//200),(25*size//40+offset+size//200,39*size//40),(27*size//40+offset,37*size//40+size//200),(27*size//40+offset-size//200,37*size//40)))
            draw.polygon(win,Color(100,100,100),((27*size//40+offset,37*size//40+3*size//400),(27*size//40+offset-3*size//400,37*size//40),(27*size//40+offset+3*size//400,37*size//40-3*size//400)))
            draw.polygon(win,Color(50,50,50),((25*size//40+offset,39*size//40-size//200),(254*size//400+offset,384*size//400),(252*size//400+offset,384*size//400),(248*size//400+offset,39*size//40-size//200)))
            draw.polygon(win,Color(50,50,50),((25*size//40+offset+size//200,39*size//40),(256*size//400+offset,386*size//400),(256*size//400+offset,388*size//400),(25*size//40+offset+size//200,392*size//400)))
            offset+=size//10
        if i == 3 and inv[i][0]:
            draw.polygon(win,Color(100,100,100),((252*size//400+offset,387*size//400),(250*size//400+offset,379*size//400),(250*size//400+offset,376*size//400),(252*size//400+offset,372*size//400),(255*size//400+offset,370*size//400),(260*size//400+offset,369*size//400),(265*size//400+offset,370*size//400),(268*size//400+offset,372*size//400),(270*size//400+offset,376*size//400),(270*size//400+offset,380*size//400),(268*size//400+offset,387*size//400),(264*size//400+offset,387*size//400),(266*size//400+offset,380*size//400),(263*size//400+offset,375*size//400),(257*size//400+offset,375*size//400),(254*size//400+offset,380*size//400),(256*size//400+offset,387*size//400)))
            draw.rect(win,Color(100+125*inv[3][1]//100,100+90*inv[3][1]//100,100-inv[3][1]),Rect(252*size//400+offset,387*size//400,size//100+1,size//200))
            draw.rect(win,Color(100+125*inv[3][1]//100,100+90*inv[3][1]//100,100-inv[3][1]),Rect(264*size//400+offset,387*size//400,size//100+1,size//200))
            offset+=size//10
        if i == 4 and inv[i][0]:
            draw.polygon(win,Color(0,0,0),((251*size//400+offset,388*size//400),(262*size//400+offset,377*size//400),(263*size//400+offset,378*size//400),(250*size//400+offset,391*size//400),(248*size//400+offset,391*size//400),(246*size//400+offset,389*size//400),(246*size//400+offset,387*size//400),(248*size//400+offset,385*size//400),(249*size//400+offset,385*size//400),(249*size//400+offset,386*size//400),(247*size//400+offset,388*size//400),(249*size//400+offset,390*size//400)))
            draw.polygon(win,Color(50,50,50),((253*size//400+offset,371*size//400),(259*size//400+offset,369*size//400),(265*size//400+offset,369*size//400),(271*size//400+offset,375*size//400),(271*size//400+offset,381*size//400),(269*size//400+offset,387*size//400),(262*size//400+offset,378*size//400)))
            draw.polygon(win,Color(150-inv[4][1],150-inv[4][1],150-inv[4][1]),((257*size//400+offset,372*size//400),(262*size//400+offset,372*size//400),(264*size//400+offset,378*size//400),(268*size//400+offset,374*size//400),(270*size//400+offset,380*size//400),(265*size//400+offset,376*size//400),(263*size//400+offset,372*size//400),(269*size//400+offset,384*size//400),(266*size//400+offset,373*size//400),(261*size//400+offset,375*size//400)))
            offset+=size//10
        if i == 5 and inv[i][0]:
            draw.rect(win,Color(255,150,150),Rect(255*size//400+offset,393*size//400-inv[i][1]*18*size//40000,10*size//400,inv[i][1]*18*size//40000))    #height (and ypos) will rely on durability
            draw.rect(win,Color(0,0,0),Rect(255*size//400+offset,375*size//400,10*size//400,18*size//400),size//400)
            draw.rect(win,Color(0,0,0),Rect(259*size//400+offset,374*size//400,2*size//400,size//400))
            draw.rect(win,Color(0,0,0),Rect(258*size//400+offset,369*size//400,4*size//400,5*size//400))
            offset+=size//10
    for i in range(len(text)): win.blit(text[i],textpos[i])

def nEndScreen(size, t, scores, dItem, weights, win):
    if t == 1 or t == 2: scores[0] = 0
    big = font.SysFont("freesans",size//8)
    small = font.SysFont("freesans",size//20)
    if t == 1: bigText, subText = "You Died!" , "You fell to your death"
    if t == 2: bigText, subText = "You Died!" , "You were eaten by a Wumpus"
    if t == 3: bigText, subText = "You Won!" , "You escaped alive"
    colors = [(0,0,0)]*3
    colors.append((255,255,255))
    colors[dItem] = (0,200,200)
    draw.rect(win,Color(200,200,200),Rect(-size//100,-size//100,102*size//100,26*size//100))
    draw.rect(win,Color(200,200,200),Rect(-size//100,9*size//10,102*size//100,11*size//100))
    text = [big.render(bigText,1,colors[2]),
            small.render(subText,1,colors[2]),
            small.render("Gold: "+str(scores[2]),1,colors[3]),
            small.render("Wumpus Killed: "+str(scores[1]),1,colors[3]),
            small.render(str(scores[2]*weights[2]),1,colors[3]),
            small.render(str(scores[1]*weights[1]),1,colors[3]),
            small.render("Restart",1,colors[0]),
            small.render("Menu",1,colors[1])]
    textpos = [text[0].get_rect(centerx=size//2,centery=2*size//20),
               text[1].get_rect(centerx=size//2,centery=4*size//20),
               text[2].get_rect(left=size//5,centery=8*size//20),
               text[3].get_rect(left=size//5,centery=10*size//20),
               text[4].get_rect(right=4*size//5,centery=8*size//20),
               text[5].get_rect(right=4*size//5,centery=10*size//20),
               text[6].get_rect(centerx=size//5,centery=19*size//20),
               text[7].get_rect(centerx=4*size//5,centery=19*size//20)]
    if t == 1 or t == 2:
        draw.line(win,Color(colors[3][0],colors[3][1],colors[3][2]),(size//5,11*size//20),(4*size//5,11*size//20),size//100)
        text.append(small.render("Score: ",1,colors[3]))
        text.append(small.render(str(scores[2]*weights[2]+scores[1]*weights[1]),1,colors[3]))
        textpos.append(text[8].get_rect(left=size//2,centery=12*size//20))
        textpos.append(text[9].get_rect(right=4*size//5,centery=12*size//20))
    elif t == 3:
        fTime = ((scores[3]//1000)//60,(scores[3]//1000)%60)
        draw.line(win,Color(colors[3][0],colors[3][1],colors[3][2]),(size//5,15*size//20),(4*size//5,15*size//20),size//100)
        draw.rect(win,Color(230,0,0),Rect(2*size//5,23*size//40,size//5,size//20))
        if scores[0] > 0: draw.rect(win,Color(0,200,200),Rect(2*size//5,23*size//40,scores[0]*size//500,size//20))
        text.append(small.render("Health: ",1,colors[3]))
        text.append(small.render("Time: "+str(fTime[0])+":"+str(fTime[1]),1,colors[3]))
        text.append(small.render(str(scores[0]*weights[0]),1,colors[3]))
        text.append(small.render(str(weights[3]//scores[3]),1,colors[3]))
        text.append(small.render("Score: ",1,colors[3]))
        text.append(small.render(str(scores[2]*weights[2]+scores[1]*weights[1]+scores[0]*weights[0]+weights[3]//scores[3]),1,colors[3]))
        textpos.append(text[8].get_rect(left=size//5,centery=12*size//20))
        textpos.append(text[9].get_rect(left=size//5,centery=14*size//20))
        textpos.append(text[10].get_rect(right=4*size//5,centery=12*size//20))
        textpos.append(text[11].get_rect(right=4*size//5,centery=14*size//20))
        textpos.append(text[12].get_rect(left=size//2,centery=16*size//20))
        textpos.append(text[13].get_rect(right=4*size//5,centery=16*size//20))
    for i in range(len(text)):
        win.blit(text[i],textpos[i])

def nythingAround(spaces, rm):
    if rm == (0,1,3): return False
    adj = []
    if rm[1] > 0: adj.append(spaces[rm[0]][rm[1]-1][rm[2]]%10)
    if rm[1] < len(spaces[rm[0]])-1: adj.append(spaces[rm[0]][rm[1]+1][rm[2]]%10)
    if rm[2] > 0: adj.append(spaces[rm[0]][rm[1]][rm[2]-1]%10)
    if rm[2] < len(spaces[rm[0]][rm[1]])-1: adj.append(spaces[rm[0]][rm[1]][rm[2]+1]%10)
    if 1 in adj or 2 in adj or 3 in adj: return True

def nHintGen(spaces, rm, actHints, ID):
    actHints.clear()
    infile = open("wumpusdata.txt","r")
    lines = []
    for line in infile: lines.append(line)
    infile.close()
    conds = (True,spaces[rm[0]][rm[1]][rm[2]]%10==1,spaces[rm[0]][rm[1]][rm[2]]%10==2,spaces[rm[0]][rm[1]][rm[2]]%10==3,spaces[rm[0]][rm[1]][rm[2]]%10==4,spaces[rm[0]][rm[1]][rm[2]]%10==5,spaces[rm[0]][rm[1]][rm[2]]%10==6 and rm != (0,1,3),False,rm==(0,1,3) and spaces[0][1][3]%10==6,False,nythingAround(spaces,rm),True,True,False)
    for i in range(14):
        if lines[10][i] == "0" and (conds[i] or ID==i):
            actHints.append(i)
            if i != 9: lines[10] = lines[10][:i]+"1"+lines[10][i+1:]
            outfile = open("wumpusdata.txt","w")
            for line in lines: print(line,end="",file=outfile)
            outfile.close()
            return

def nHintDraw(size, pPos, randRec, actHints, iKeys, win):
    if not actHints: return
    keys = []
    for i in range(7): keys.append(key.name(iKeys[i]))
    face = font.SysFont("freesans",size//30)
    tColors = ((0,200,200),(255,255,255),(230,0,0),(225,190,0),(180,225,180),(180,225,180),(75,75,0),(75,75,0),(75,75,0),(225,190,0),(100,100,100),(0,200,200),(0,200,200),(225,190,0))
    hints = [("Use ["+keys[0]+"], ["+keys[1]+"],","["+keys[2]+"], and ["+keys[3]+"]","to move"),
             ("Avoid pits:","falling hurts!"),
             ("Wumpus can kill you instantly.","Dodge them or shoot them!"),
             ("Collect gold to","use at the shop!"),
             ("Hit ["+keys[4]+"] to delve","deeper into the dungeon"),
             ("Hit ["+keys[4]+"] to","climb back up"),
             ("Hit ["+keys[4]+"]","to assist"),
             ("The shop will now be","open! Return to the","entrance to visit it"),
             ("Hit ["+keys[4]+"] to","open the shop and","purchase items"),
             ("Most items are","passive and will","eventually wear out"),
             ("You can't see into","other rooms, but you","can tell that a","nearby room contains","danger or riches"),
             ("Hold ["+keys[6]+"] to","run faster"),
             ("Hold ["+keys[5]+"] to charge","and fire an arrow"),
             ("You have defeated the Wumpus!","Now you must safely exit the maze")]
    if keys[0] == "up" and keys[1] == "down" and keys[2] == "right" and keys[3] == "left":
        hints[0] = ("Use arrow","keys to move")
    pos = [(size//2,4*size//5),(size//2,size//2),(size//2,4*size//5),(size//2,4*size//5),(size//2,7*size//20),(size//2,7*size//20),(size//2,4*size//5),(size//2,4*size//5),(size//2,4*size//5),(3*size//5,3*size//4),(6*size//10,size//10),(size//2,4*size//5),(size//2,4*size//5),(size//2,4*size//5)]
    text = []
    textpos = []
    for i in actHints:
        for j in range(len(hints[i])):
            text.append(face.render(hints[i][j],1,tColors[i]))
            if i == 9 or i == 10: textpos.append(text[-1].get_rect(left=pos[i][0],top=pos[i][1]+j*size//30))
            else: textpos.append(text[-1].get_rect(centerx=pos[i][0],centery=pos[i][1]+j*size//30))
    for i in range(len(text)):
        win.blit(text[i],textpos[i])

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                              New Center
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

def newHTW(size,win):

    spaces = [[[0,0,0],         #Flipped along diagonal
               [0,0,10,10],     #0-Empty, 1-Pit, 2-Beast, 3-Gold, 4-Exit, 5-AntiExit, 6-Shop(keep)
               [0,0,0]],        #1 in tens place - Explored
              [[0,0,0,0],
               [0,0,0,0],
               [0,0,0,0],
               [0,0,0,0]],
              [[0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0]],
              [[0,0,0,0,0,0],
               [0,0,0,0,0,0],
               [0,0,0,0,0,0],
               [0,0,0,0,0,0],
               [0,0,0,0,0,0],
               [0,0,0,0,0,0]],
              [[0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0]],
              [[0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0]],
              [[0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0]]]
    mapOffset = [(0,0)]*(len(spaces))
    rm = (0,1,2)
    pPos = (size//2,size//2)
    pFace = ["u"]
    pSpeed = size//200
    health = 100
    
    aCharge = 0
    aTracker = []
    aInRoom = []
    aStart = [pPos[0],pPos[1]]
    inv = [[0,0],[1,100],[0,100],[0,100],[0,100],[0,100]]   #null, arrows, healthpot, goldmag, para, wumprep
    prices = [0,50,100,130,200,250]
    inShop = False
    sItem = 0
    money = 0
    bKilled = 0
    bigKilled = False
    weights = (10,50,1,1500000000)

    randRec = []
    for i in range(len(spaces)):
        randRec.append([])
        for j in range(len(spaces[i])):
            randRec[i].append([])
            for k in range(len(spaces[i][j])):
                randRec[i][j].append(0)

    nMapGen(size,spaces,randRec,mapOffset)
    
    clock = time.Clock()
    finTime = 1
    dead = False
    dItem = 0
    pause = False
    pItem = 0
    highScore = False
    name = ""
    actHints = []
    nHintGen(spaces,rm,actHints,0)

    while True:
        try:
            infile = open("wumpusdata.txt","r")
            lines = []
            for line in infile:
                lines.append(line)
            infile.close()
            uk = eval(lines[0])
            dk = eval(lines[1])
            rk = eval(lines[2])
            lk = eval(lines[3])
            ek = eval(lines[4])
            fk = eval(lines[5])
            spk = eval(lines[6])
            break
        except ValueError and IndexError: resetData()

    uPress = False
    dPress = False
    rPress = False
    lPress = False
    shPress = False

    while True:
        clock.tick(90)
        oldRm = rm
        for item in event.get():
            if item.type == QUIT:
                display.quit()
                sys.exit()
            if item.type == KEYDOWN:
                if highScore:
                    if item.mod & KMOD_SHIFT: shPress = True
                    else: shPress = False
                    if item.key >= 48 and item.key <= 57: name+=key.name(item.key)
                    if item.key == 32: name+=" "
                    if item.key >= 97 and item.key <= 122:
                        if shPress: name+=(key.name(item.key)).capitalize()
                        else: name+=key.name(item.key)
                    if item.key == 8: name = name[:-1]
                    name = name[:8]
                    if item.key == 13:
                        for i in range(len(hLines)):
                            hLines[i] = hLines[i].replace("pholder!",name.ljust(8))
                        outfile = open("wumpusdata.txt","w")
                        for line in hLines: print(str(line),end="",file=outfile)
                        highScore = False
                        break
                    if item.key == K_ESCAPE:
                        for i in range(len(hLines)):
                            hLines[i] = hLines[i].replace("pholder!","No name ")
                        outfile = open("wumpusdata.txt","w")
                        for line in hLlines: print(str(line),end="",file=outfile)
                        highScore = False
                        break
                sItem = int(sItem)
                if item.key == uk and not highScore:
                    if pause: pItem = (pItem-1)%3
                    elif dead: pass
                    elif inShop: sItem = (sItem-1)%6
                    else:
                        uPress = True
                        if pFace.count("u"): pFace.remove("u")
                        pFace.append("u")
                if item.key == dk and not highScore:
                    if pause: pItem = (pItem+1)%3
                    elif dead: pass
                    elif inShop: sItem = (sItem+1)%6
                    else:
                        dPress = True
                        if pFace.count("d"): pFace.remove("d")
                        pFace.append("d")
                if item.key == lk and not highScore:
                    if pause: pass
                    elif dead: dItem = 0
                    elif not inShop:
                        lPress = True
                        if pFace.count("l"): pFace.remove("l")
                        pFace.append("l")
                if item.key == rk and not highScore:
                    if pause: pass
                    elif dead: dItem = 1
                    elif not inShop:
                        rPress = True
                        if pFace.count("r"): pFace.remove("r")
                        pFace.append("r")
                if item.key == ek and not highScore:
                    if pause:
                        if pItem == 0:
                            pause = False
                        if pItem == 1:
                            prevSize = size
                            newKeys = options(size,win)
                            uk, dk, rk, lk, ek, fk, spk, size, hint = eval(newKeys[0]), eval(newKeys[1]), eval(newKeys[2]), eval(newKeys[3]), eval(newKeys[4]), eval(newKeys[5]), eval(newKeys[6]), int(newKeys[8]), newKeys[10]
                            pSpeed = size//200
                            pPos = (pPos[0]*size//prevSize,pPos[1]*size//prevSize)
                            for a in aTracker:
                                a[0] = [a[0][0]*size//prevSize,a[0][1]*size//prevSize]
                            if hint[0] == "0":
                                nHintGen(spaces,rm,actHints,0)
                        if pItem == 2:
                            return "menu", size, uk, dk, ek
                    elif dead:
                        if dItem == 0: return "restart", size, uk, dk, ek
                        if dItem == 1: return "menu", size, uk, dk, ek
                    elif rm == (0,1,3) and pPos[0] > pPos[1]//3+9*size//20 and not inShop and spaces[0][1][3]%10 == 6:
                        nHintGen(spaces,rm,actHints,9)
                        inShop = True
                        sItem = 0
                    elif inShop:
                        nHintGen(spaces,rm,actHints,9)
                        if money >= prices[sItem]:
                            money-=prices[sItem]
                            if sItem == 0: inShop = False
                            elif sItem == 2:
                                health += random.randrange(40,61)
                                if health > 100: health = 100
                            else: inv[sItem][0]+=1
                        else: sItem = str(sItem)
                    elif spaces[rm[0]][rm[1]][rm[2]]%10 == 6 and randRec[rm[0]][rm[1]][rm[2]][2]==0:
                        tempx = randRec[rm[0]][rm[1]][rm[2]][0]*size//400
                        tempy = randRec[rm[0]][rm[1]][rm[2]][1]*size//400
                        if pPos[0] > tempx-15*size//80 and pPos[0] < tempx+2*size//80 and pPos[1] > tempy-5*size//80 and pPos[1] < tempy+size//80:
                            randRec[rm[0]][rm[1]][rm[2]][2] = 1
                            spaces[0][1][3] = 16
                            nHintGen(spaces,rm,actHints,7)
                    elif pPos[0]<13*size//20 and pPos[0]>7*size//20 and pPos[1]<3*size//4 and pPos[1]>9*size//20:
                        if spaces[rm[0]][rm[1]][rm[2]]%10 == 4: rm, pPos = nRoomSwitch("f",size,spaces,rm,pPos,mapOffset)
                        elif spaces[rm[0]][rm[1]][rm[2]]%10 == 5: rm, pPos = nRoomSwitch("ae",size,spaces,rm,pPos,mapOffset)
                if item.key == fk and inv[1][0] and not highScore:
                    aCharge = 1
                if item.key == spk and not highScore: pSpeed = 3*pSpeed//2
                if item.key == K_ESCAPE and not highScore:
                    if inShop: inShop = False
                    elif dead: return "menu",size, uk, dk, ek
                    else:
                        if pause: pause = False
                        else:
                            pItem = 0
                            pause = True
            if item.type == KEYUP and not dead:
                """if item.key == K_RSHIFT or item.key == K_LSHIFT:
                    shPress = False"""
                if item.key == uk:
                    uPress = False
                    if len(pFace) > 1: pFace.remove("u")
                if item.key == dk:
                    dPress = False
                    if len(pFace) > 1: pFace.remove("d")
                if item.key == lk:
                    lPress = False
                    if len(pFace) > 1: pFace.remove("l")
                if item.key == rk:
                    rPress = False
                    if len(pFace) > 1: pFace.remove("r")
                if item.key == fk:
                    if aCharge > 75:
                        inv[1][0]-=1
                        aTracker.append([aStart,pFace[-1],rm])
                    aCharge = 0
                if item.key == spk: pSpeed = 2*pSpeed//3
        if uPress and not dead and not pause:
            if not (dPress or lPress or rPress): pFace = ["u"]
            rm, pPos = nRoomSwitch("u",size,spaces,rm,pPos,mapOffset)
            if pPos[1] > 13*size//40 and (rm != (0,1,3) or pPos[1] > 55*size//80 or pPos[0] < 8*size//10):
                pPos = (pPos[0],pPos[1]-pSpeed)
            if pPos[1] < 6*((size//5)-pPos[0]):
                pPos = (pPos[0]+pSpeed//2,pPos[1])
            if pPos[1] < 6*(pPos[0]-(4*size//5)) or (rm == (0,1,3) and pPos[1] < 3*(pPos[0]-(11*size//20)) and pPos[0] < 8*size//10):
                pPos = (pPos[0]-pSpeed//2,pPos[1])
        if dPress and not dead and not pause:
            if not (uPress or lPress or rPress): pFace = ["d"]
            rm, pPos = nRoomSwitch("d",size,spaces,rm,pPos,mapOffset)
            if pPos[1] < 7*size//8:
                pPos = (pPos[0],pPos[1]+pSpeed)
        if lPress and not dead and not pause:
            if not (dPress or uPress or rPress): pFace = ["l"]
            rm, pPos = nRoomSwitch("l",size,spaces,rm,pPos,mapOffset)
            if pPos[0] > ((size//5)-(pPos[1]//6)):
                pPos = (pPos[0]-pSpeed,pPos[1])
        if rPress and not dead and not pause:
            if not (dPress or lPress or uPress): pFace = ["r"]
            rm, pPos = nRoomSwitch("r",size,spaces,rm,pPos,mapOffset)
            if pPos[0] < (pPos[1]//6+(4*size//5)) and (rm != (0,1,3) or pPos[0] < (pPos[1]//3+11*size//20) or pPos[1] > 27*size//40):
                pPos = (pPos[0]+pSpeed,pPos[1])
        nRoomDraw(size,spaces,rm,randRec,win)
        if oldRm != rm: nHintGen(spaces,rm,actHints,0)
        nHintDraw(size,pPos,randRec,actHints,(uk,dk,rk,lk,ek,fk,spk),win)
        if pFace[-1] == "u":
            aStart = [pPos[0]+6*size//400,pPos[1]-70*size//400+aCharge*size//4000]
        if pFace[-1] == "d":
            aStart = [pPos[0]-6*size//400,pPos[1]-aCharge*size//4000-size//50]
        if pFace[-1] == "l":
            aStart = [pPos[0]-size//10+aCharge*size//4000,pPos[1]-43*size//400]
        if pFace[-1] == "r":
            aStart = [pPos[0]-aCharge*size//4000+size//10,pPos[1]-33*size//400]
        if rm == (0,1,3): aCharge = 0
        if aCharge and not dead and not pause:
            if aCharge > 100:
                aCharge = 0
                inv[1][0]-=1
                aTracker.append([aStart,pFace[-1],rm])
            else: aCharge+=1
        if spaces[rm[0]][rm[1]][rm[2]]%10 == 1:
            nPlayerDraw(size,pPos,pFace[-1],aCharge,aInRoom,win)
            for a in aInRoom: nArrowDraw(size, a, win)
            if nPitCollide(size,rm,pPos,randRec,win) and not dead:
                rm, pPos = nRoomSwitch("f",size,spaces,rm,pPos,mapOffset)
                nHintGen(spaces,rm,actHints,0)
                if inv[4][0]:
                    health-=random.randrange(6,11)
                    inv[4][1]-=random.randrange(5,15)
                    if inv[4][1] <= 0:
                        inv[4][0]-=1
                        inv[4][1]=100
                else:
                    health-=20
                    if health <= 0:
                        finTime = time.get_ticks()
                        pFace.append("fatal")
                        dead = 1
                        hLines = scoreTest("n",money*weights[2]+bKilled*weights[1],(money,bKilled))
                        if hLines: highScore = True
        elif spaces[rm[0]][rm[1]][rm[2]]%10 == 2:
            if not oldRm == rm:
                randRec[rm[0]][rm[1]][rm[2]][3] = False
            if pause and randRec[rm[0]][rm[1]][rm[2]][2][0] != "s": nBeastDraw(size,[randRec[rm[0]][rm[1]][rm[2]][0],randRec[rm[0]][rm[1]][rm[2]][1],[1,1],randRec[rm[0]][rm[1]][rm[2]][3],randRec[rm[0]][rm[1]][rm[2]][4]],pPos,pFace[-1],aCharge,aInRoom,inv,win)
            elif nBeastDraw(size,randRec[rm[0]][rm[1]][rm[2]],pPos,pFace[-1],aCharge,aInRoom,inv,win) and not dead:
                finTime = time.get_ticks()
                pFace.append("fatal")
                dead = 2
                hLines = scoreTest("n",money*weights[2]+bKilled*weights[1],(money,bKilled))
                if hLines: highScore = True
        elif spaces[rm[0]][rm[1]][rm[2]]%10 == 3:
            gAdd = nGoldDraw(size,randRec[rm[0]][rm[1]][rm[2]],pPos,pFace[-1],aCharge,aInRoom,inv,win)
            try: money+=gAdd
            except TypeError:
                money+=int(gAdd)
                spaces[rm[0]][rm[1]][rm[2]]=10
        elif spaces[rm[0]][rm[1]][rm[2]]%10 == 4: nExitDraw(size,randRec[rm[0]][rm[1]][rm[2]],pPos,pFace[-1],aCharge,aInRoom,win)
        elif spaces[rm[0]][rm[1]][rm[2]]%10 == 5: nAExitDraw(size,randRec[rm[0]][rm[1]][rm[2]],pPos,pFace[-1],aCharge,aInRoom,win)
        elif spaces[rm[0]][rm[1]][rm[2]]%10 == 6 and rm != (0,1,3):
            if not oldRm == rm and randRec[rm[0]][rm[1]][rm[2]][2] == 1:
                spaces[rm[0]][rm[1]][rm[2]]-=6
            else: nShopDraw(size,randRec[rm[0]][rm[1]][rm[2]],rm,pPos,pFace[-1],aCharge,aInRoom,win)
        else:
            nPlayerDraw(size,pPos,pFace[-1],aCharge,aInRoom,win)
            for a in aInRoom: nArrowDraw(size, a, win)
        if bigKilled and rm == (0,1,3) and not dead:
            finTime = time.get_ticks()
            pPos = [size//2,size//2]
            dead = 3
            hLines = scoreTest("n",money*weights[2]+bKilled*weights[1]+health*weights[0]+weights[3]//finTime,(money,bKilled,health,finTime))
            if hLines: highScore = True
        if aTracker:
            pickup,aInRoom,spoils = nArrowUpdate(spaces,randRec,aTracker,pPos,rm,size,pause,win)
            inv[1][0]+=pickup
            bKilled+=spoils[0]
            money+=spoils[1]
            if spoils[1]:
                nHintGen(spaces,rm,actHints,13)
                bigKilled = True
        else: aInRoom = []
        nUI(size,inv,money,health,win)
        if inShop:
            nShopUI(size,sItem,win)
        if pause: Pause(size//10,pItem,win)
        if dead: nEndScreen(size,dead,[health,bKilled,money,finTime],dItem,weights,win)
        if highScore: hsUI(size//10,name,win)
        display.flip()

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                Main
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

def options(size,win):
    infile = open("wumpusdata.txt","r")
    allLines = []
    lines = []
    for line in infile:
        allLines.append(line)
    infile.close()
    for i in range(7):
        lines.append(eval(allLines[i]))
    lines.append(allLines[7].replace("\n",""))
    lines.append(allLines[8].replace("\n",""))
    lines.append(allLines[9].replace("\n",""))
    lines.append(allLines[10].replace("\n",""))
    oItem = 10
    face = font.SysFont("freesans",size//20)
    tiny = font.SysFont("freesans",size//50)
    
    while True:
        win.fill(Color(200,255,200))
        for item in event.get():
            if item.type == QUIT:
                display.quit()
                sys.exit()
            if item.type == KEYDOWN:
                if oItem < 7 and lines[oItem] == "Press a key":
                    lines[oItem] = key.key_code(key.name(item.key))
                elif item.key == lines[0]:
                    oItem=(oItem-1)%12
                elif item.key == lines[1]:
                    oItem=(oItem+1)%12
                elif item.key == lines[4]:
                    if oItem == 7:
                        if lines[7] == "on":
                            lines[7] = "off"
                            print(display.get_window_size())
                            display.toggle_fullscreen()
                            #display.set_mode((size,size))
                        elif lines[7] == "off":
                            lines[7] = "on"
                            print(display.get_window_size())
                            display.toggle_fullscreen()
                            #display.set_mode((size,size),FULLSCREEN)
                    if oItem == 8:
                        if lines[8] == "400": lines[8], size = "800", 800
                        elif lines[8] == "800": lines[8], size = "400", 400
                        if lines[7] == "on":
                            win = display.set_mode((size,size),FULLSCREEN)
                        else:
                            win = display.set_mode((size,size))
                        face = font.SysFont("freesans",size//20)
                        tiny = font.SysFont("freesans",size//50)
                    if oItem == 9:
                        if lines[9] == "prompt":
                            lines[9] = "off"
                            lines[10] = "11111111111111"
                        elif lines[9] == "off":
                            lines[9] = "prompt"
                            lines[10] = "00000000000000"
                    if oItem == 10:
                        for i in range(len(lines)):
                            allLines[i] = str(lines[i])+"\n"
                    if oItem == 10 or oItem == 11:
                        outfile = open("wumpusdata.txt","w")
                        for line in allLines:
                            print(str(line),end="",file=outfile)
                        outfile.close()
                        if allLines[7] == "on\n": win = display.set_mode((int(allLines[8]),int(allLines[8])),FULLSCREEN)
                        else: win = display.set_mode((int(allLines[8]),int(allLines[8])))
                        return allLines
                    if oItem < 7: lines[oItem] = "Press a key"
                if item.key == K_ESCAPE:
                    outfile = open("wumpusdata.txt","w")
                    for line in allLines:
                        print(str(line),end="",file=outfile)
                    outfile.close()
                    if allLines[7] == "on\n": win = display.set_mode((int(allLines[8]),int(allLines[8])),FULLSCREEN)
                    else: win = display.set_mode((int(allLines[8]),int(allLines[8])))
                    return allLines
        tColors = [(0,0,0)]*12
        tColors[oItem] = (0,200,200)
        text = [face.render("Controls",1,(0,0,0)),
                face.render("Up",1,tColors[0]),
                face.render("Down",1,tColors[1]),
                face.render("Right",1,tColors[2]),
                face.render("Left",1,tColors[3]),
                face.render("Select/Interact",1,tColors[4]),
                face.render("Fire",1,tColors[5]),
                face.render("Sprint",1,tColors[6]),
                face.render("Fullscreen: "+lines[7],1,tColors[7]),
                face.render("Resolution: "+lines[8],1,tColors[8]),
                face.render("Hints: "+lines[9],1,tColors[9]),
                face.render("Apply",1,tColors[10]),
                face.render("Cancel",1,tColors[11]),
                tiny.render("Version 1.9.1",1,(0,0,0)),
                tiny.render("Created by RubeGoldbegGuy",1,(0,0,0)),
                tiny.render("Made using Pygame",1,(0,0,0))]
        textpos = [text[0].get_rect(centerx=size//2,centery=3*size//20),
                   text[1].get_rect(left=size//5,centery=4*size//20),
                   text[2].get_rect(left=size//5,centery=5*size//20),
                   text[3].get_rect(left=size//5,centery=6*size//20),
                   text[4].get_rect(left=size//5,centery=7*size//20),
                   text[5].get_rect(left=size//5,centery=8*size//20),
                   text[6].get_rect(left=size//5,centery=9*size//20),
                   text[7].get_rect(left=size//5,centery=10*size//20),
                   text[8].get_rect(centerx=size//2,centery=12*size//20),
                   text[9].get_rect(centerx=size//2,centery=13*size//20),
                   text[10].get_rect(centerx=size//2,centery=14*size//20),
                   text[11].get_rect(centerx=size//2,centery=16*size//20),
                   text[12].get_rect(centerx=size//2,centery=17*size//20),
                   text[13].get_rect(left=0,bottom=size),
                   text[14].get_rect(centerx=size//2,bottom=size),
                   text[15].get_rect(right=size,bottom=size)]
        for i in range(7):
            try:
                if lines[i] == "Press a key": int("yes")
                text.append(face.render(key.name(lines[i]),1,tColors[i]))
            except ValueError: text.append(face.render(lines[i],1,tColors[i]))
            textpos.append(text[-1].get_rect(right=4*size//5,centery=i*size//20+4*size//20))
                

        for i in range(len(text)):
            win.blit(text[i],textpos[i])
        display.flip()

def scoreTest(game,score,scores):
    text = ""
    if game == "n":
        for i in scores:
            if i > 9999999: i = 9999999
            text+=str(i).rjust(7,"0")
        offset = 11
    if game == "c": offset = 16
    infile = open("wumpusdata.txt","r")
    lines = infile.readlines()
    for i in range(5):
        if lines[offset+i][:8] == "        " or int(lines[offset+i][8:14]) < score:
            lines.insert(offset+i,"pholder!"+str(score).rjust(6,"0")+text+"\n")
            lines.pop(offset+5)
            return lines
    return False

def dataReset():
    outfile = open("wumpusdata.txt","w")
    lines = ("K_UP","K_DOWN","K_RIGHT","K_LEFT","K_RETURN","K_SPACE","K_b","off",800,"prompt","00000000000000","        000000","        000000","        000000","        000000","        000000","        000000","        000000","        000000","        000000","        000000")
    for line in lines:
        print(str(line),file=outfile)

def Pause(size, item, win):
    draw.rect(win,Color(200,200,200),Rect(4*size,7*size//2,2*size,3*size),size)
    draw.rect(win,Color(200,200,200),Rect(4*size,7*size//2,2*size,3*size))
    draw.circle(win,Color(200,200,200),(4*size,7*size//2),size//2-1)
    draw.circle(win,Color(200,200,200),(6*size,7*size//2),size//2-1)
    draw.circle(win,Color(200,200,200),(4*size,13*size//2),size//2-1)
    draw.circle(win,Color(200,200,200),(6*size,13*size//2),size//2-1)
    tColors = [[255,255,255]]*3
    tColors[item] = [0,200,200]
    face = font.SysFont("freesans",size//2)
    text = [face.render("Resume",1,(tColors[0])),
            face.render("Options",1,(tColors[1])),
            face.render("Exit",1,(tColors[2]))]
    textpos = [text[0].get_rect(centerx=5*size,centery=4*size),
               text[1].get_rect(centerx=5*size,centery=5*size),
               text[2].get_rect(centerx=5*size,centery=6*size)]
    for i in range(3): win.blit(text[i],textpos[i])

def hsUI(size,name,win):
    draw.rect(win,Color(200,200,200),Rect(2*size,7*size//2,6*size,3*size),size)
    draw.rect(win,Color(200,200,200),Rect(2*size,7*size//2,6*size,3*size))
    draw.circle(win,Color(200,200,200),(2*size,7*size//2),size//2-1)
    draw.circle(win,Color(200,200,200),(8*size,7*size//2),size//2-1)
    draw.circle(win,Color(200,200,200),(2*size,13*size//2),size//2-1)
    draw.circle(win,Color(200,200,200),(8*size,13*size//2),size//2-1)
    big = font.SysFont("freesans",size)
    small = font.SysFont("freesans",size//4)
    text = [big.render("High Score",1,(255,255,255)),
            small.render("Enter a name and hit [enter] to confirm",1,(255,255,255)),
            big.render(name+"|",1,(0,0,0))]
    textpos = [text[0].get_rect(centerx=5*size,centery=4*size),
               text[1].get_rect(centerx=5*size,centery=5*size),
               text[2].get_rect(centerx=5*size,centery=6*size)]
    for i in range(3): win.blit(text[i],textpos[i])

def scoreboard(size,win):
    win.fill(Color(200,255,200))
    infile = open("wumpusdata.txt","r")
    lines = infile.readlines()
    ek = eval(lines[4])
    face = font.SysFont("freesans",size//25)
    offset = 0
    text = [face.render("High Scores",1,(0,0,0)),
            face.render("Name",1,(0,0,0)),
            face.render("Wumpus",1,(0,0,0)),
            face.render("Gold",1,(0,0,0)),
            face.render("Health",1,(0,0,0)),
            face.render("Time",1,(0,0,0)),
            face.render("Points",1,(0,0,0)),
            face.render("Classic",1,(0,0,0)),
            face.render("Menu",1,(0,200,200))]
    textpos = [text[0].get_rect(centerx=size//2,centery=2*size//20),
               text[1].get_rect(left=size//16,centery=4*size//20),
               text[2].get_rect(right=29*size//64,centery=4*size//20),
               text[3].get_rect(right=9*size//16,centery=4*size//20),
               text[4].get_rect(right=45*size//64,centery=4*size//20),
               text[5].get_rect(right=13*size//16,centery=4*size//20),
               text[6].get_rect(right=38*size//40,centery=4*size//20),
               text[7].get_rect(centerx=size//2,centery=23*size//40),
               text[8].get_rect(centerx=size//2,centery=37*size//40)]
    for i in range(5):
        if lines[11+i][:8] != "        ":
            text.append(face.render(lines[11+i][:8],1,(0,0,0)))
            text.append(face.render(str(int(lines[11+i][8:14])),1,(0,0,0)))
            text.append(face.render(str(int(lines[11+i][14:21])),1,(0,0,0)))
            text.append(face.render(str(int(lines[11+i][21:28])),1,(0,0,0)))
            if lines[11+i][35:42] and lines[11+i][32]!="\n": time = ((int(lines[11+i][32:38])//1000)//60,(int(lines[11+i][32:38])//1000)%60)
            else: time = ("--","--")
            text.append(face.render(str(time[0])+":"+str(time[1]),1,(0,0,0)))
            textpos.append(text[-5].get_rect(left=size//16,centery=(11+offset)*size//40))
            textpos.append(text[-4].get_rect(right=38*size//40,centery=(11+offset)*size//40))
            textpos.append(text[-3].get_rect(right=9*size//16,centery=(11+offset)*size//40))
            textpos.append(text[-2].get_rect(right=29*size//64,centery=(11+offset)*size//40))
            textpos.append(text[-1].get_rect(right=13*size//16,centery=(11+offset)*size//40))
            draw.rect(win,Color(230,0,0),Rect(24*size//40,(21+2*offset)*size//80,size//10,size//40))
            if lines[11+i][28:35] and lines[11+i][28]!="\n": draw.rect(win,Color(0,200,200),Rect(24*size//40,(21+2*offset)*size//80,int(lines[11+i][26:32])*size//1000,size//40))
            offset+=2
    offset = 0
    for i in range(5):
        if lines[16+i][:8] != "        ":
            text.append(face.render(lines[16+i][:8],1,(0,0,0)))
            text.append(face.render(str(int(lines[16+i][8:14])),1,(0,0,0)))
            textpos.append(text[-2].get_rect(left=size//16,centery=(26+offset)*size//40))
            textpos.append(text[-1].get_rect(right=38*size//40,centery=(26+offset)*size//40))
            offset+=2
    for i in range(len(text)): win.blit(text[i],textpos[i])
    display.flip()
    while True:
        for item in event.get():
            if item.type == QUIT:
                display.quit()
                sys.exit()
            if item.type == KEYDOWN:
                if item.key == K_ESCAPE or item.key == ek:
                    return

def mScreen(size,item,win):
    win.fill(Color(200,255,200))
    big = font.SysFont("freesans",size//6)
    small = font.SysFont("freesans",size//13)
    tColors = [[0,0,0]]*5
    tColors[item] = [0,200,200]
    text = [big.render("Hunt",1,(0,0,0)),
            small.render("the",1,(0,0,0)),
            big.render("Wumpus",1,(230,0,0)),
            small.render("Start Game",1,tColors[0]),
            small.render("Play Classic",1,tColors[1]),
            small.render("Options",1,tColors[2]),
            small.render("High Scores",1,tColors[3]),
            small.render("Quit",1,tColors[4])]
    textpos = [text[0].get_rect(centerx=size//2,centery=size//8),
               text[1].get_rect(centerx=size//2,centery=17*size//64),
               text[2].get_rect(centerx=size//2,centery=3*size//8),
               text[3].get_rect(centerx=size//2,centery=9*size//16),
               text[4].get_rect(centerx=size//2,centery=21*size//32),
               text[5].get_rect(centerx=size//2,centery=12*size//16),
               text[6].get_rect(centerx=size//2,centery=27*size//32),
               text[7].get_rect(centerx=size//2,centery=15*size//16)]
    for i in range(8):
        win.blit(text[i],textpos[i])
    display.flip()

def menu():
    #print(1)
    while True:
        try:
            #print(2)
            infile = open("wumpusdata.txt","r")
            lines = []
            for line in infile:
                lines.append(line)
            infile.close()
            init()
            size = int(lines[8])
            uk = eval(lines[0])
            dk = eval(lines[1])
            ek = eval(lines[4])
            break
        except:
            dataReset()
    if lines[7] == "on\n": win = display.set_mode((size,size),FULLSCREEN)
    else: win = display.set_mode((size,size))
    mItem = 0           #start, classic, options, high, quit

    while True:
        for item in event.get():
            if item.type == QUIT:
                display.quit()
                sys.exit()
            if item.type == KEYDOWN:
                #print(item.key)
                #print(item.mod)
                if item.key == uk:
                    mItem-=1
                    if mItem < 0:
                        mItem=4
                if item.key == dk:
                    mItem+=1
                    if mItem > 4:
                        mItem=0
                if item.key == ek:
                    if mItem == 0:
                        while True:
                            choice, size, uk, dk, ek = newHTW(size,win)
                            if choice == "menu": break
                    if mItem == 1:
                        while True:
                            choice, cSize, uk, dk, ek = classic(size//10,win)
                            size = 10*cSize
                            if choice == "menu": break
                    if mItem == 2:
                        newKeys = options(size,win)
                        uk, dk, ek, size = eval(newKeys[0]), eval(newKeys[1]), eval(newKeys[4]), int(newKeys[8])
                    if mItem == 3:
                        scoreboard(size,win)
                    if mItem == 4:
                        display.quit()
                        sys.exit()
                if item.key == K_ESCAPE:
                    display.quit()
                    sys.exit()
        mScreen(size,mItem,win)

if __name__ == '__main__':
    init()
    logo.logoDraw()
    menu()
    #size = 400
    #win = display.set_mode((size,size))
    #newHTW(size,win)
    #try:
    #    menu()
    #except:
    #    display.quit()
    #    print(twenty)
