#logo.py
#Making my fancy logo (grid curve)
#NOTE: with Qt graphics? yes...
#NO! try pygame?????

import sys, pygame
from pygame.locals import *

def logoDraw():
    win = pygame.display.set_mode((400,400))
    #print(pygame.font.get_fonts())
    s=list(range(1,401))
    s.reverse()

    clock = pygame.time.Clock()

    font = pygame.font.SysFont("freesans", 35)
    text = [font.render("RubeGoldbergGuy",1,(255,255,255)),
            font.render("Presents:",1,(255,255,255))]
    textpos1 = text[0].get_rect(centerx=200,centery=180)
    textpos2 = text[1].get_rect(centerx=200,centery=220)
    
    for i in s:
        clock.tick(40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN or event.type == MOUSEBUTTONUP:
                return 'done'
            
        n = 400//i
        if i>63:c=255
        else:c=i*4
        win.fill(pygame.Color(c,c,c))
        for j in range(1,n+1):
            pygame.draw.line(win,pygame.Color(255,0,0),(400-(i*j),0),(0,0+(i*j)),1)
            pygame.draw.line(win,pygame.Color(255,255,0),(0+(i*j),400),(0,0+(i*j)),1)
            pygame.draw.line(win,pygame.Color(0,255,0),(0+(i*j),400),(400,400-(i*j)),1)
            pygame.draw.line(win,pygame.Color(0,0,255),(400-(i*j),0),(400,400-(i*j)),1)
        win.blit(text[0], (textpos1))
        win.blit(text[1], (textpos2))
        pygame.display.flip()
    pygame.time.wait(5000)
    return "done"


def rotating():
    win = pygame.display.set_mode((400,400))
    s=list(range(1,401))
    s.reverse()

    clock = pygame.time.Clock()
    
    for i in s:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            
        win.fill(pygame.Color(0,0,0))
        n = 400//i
        for j in range(1,2):
            #pygame.draw.line(win,pygame.Color(255,0,0),(400-(i*j),0),(0,0+(i*j)),1)
            #pygame.draw.line(win,pygame.Color(255,255,0),(400-(i*j),400),(0,0+(i*j)),1)
            #pygame.draw.line(win,pygame.Color(0,255,0),(400-(i*j),400),(400,0+(i*j)),1)
            #pygame.draw.line(win,pygame.Color(0,0,255),(400-(i*j),0),(400,0+(i*j)),1)
            pygame.draw.polygon(win,pygame.Color(255,0,0),((400-(i*j),0),(0,0+(i*j)),(400-(i*j),400),(400,0+(i*j))))
        
        pygame.display.flip()

def drawHere():
    pygame.init()
    logoDraw()

    pygame.display.quit()
    sys.exit()

if __name__ == '__main__': drawHere()
