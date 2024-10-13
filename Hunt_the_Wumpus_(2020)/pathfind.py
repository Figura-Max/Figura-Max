#Pathfinding
#Hopefully no bugs?

def use(maze, safe, start, dest):
    rec = []
    for i in maze:
        rec.append(i.copy())
    for i in range(len(rec)):
        for j in range(len(rec[i])):
            rec[i][j] = 0
    return pf(maze, safe, start, dest, rec)

def pf(maze, safe, start, dest, record):
    if start == dest:
        return record#[start]
    nTest = []
    adj = ((1,0),(0,1),(-1,0),(0,-1))
    for i in adj:
        test = (start[0]+i[0],start[1]+i[1])
        if test[0] >= 0 and test[0] < len(maze) and test[1] >= 0 and test[1] < len(maze[test[0]]):
            for j in safe:
                if maze[test[0]][test[1]] == j and record[test[0]][test[1]]==0:
                    nTest.append(test)
                    record[test[0]][test[1]] = record[start[0]][start[1]]+1

    if nTest:
        retVal = []
        for i in nTest:
            retVal.append(pf(maze,safe,i,dest,record))
        for i in retVal:
            if i:
                #i.append(start)
                return i
        return False
    return False


def doHere():
    
    maze = [[0,1,0,0],
            [0,1,0,1],
            [0,0,0,0],
            [0,0,1,0]]
    """result = pf(maze,[0],(0,0),(0,3),maze)
    try:
        #result.reverse()
        for i in result:
            print(i)
    except: print(result)"""
    print(contig(maze,[0]))


def contig(maze, safe):
    while True:
    #try:
        access = []
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                for s in safe:
                    if maze[i][j] == s:
                        access.append((i,j))
        start = access[0]
        able = []
        for i in access:
            rec = []
            for j in maze:
                rec.append(j.copy())
            able.append(pf(maze,safe,start,i,rec))
        for i in able:
            if not i: return False
        return True
    #except: return False
    

if __name__ == '__main__': doHere()
