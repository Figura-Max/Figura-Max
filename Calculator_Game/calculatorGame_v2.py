#Max Figura - calculatorGame_v2.py
#Originally created 2021
#Updated October 2024

#Inserts 1s into large enough sequences of 0s (recursive)
#seq - slice of current sequence
#nSeq - slice of next sequence
#return nSeq with inserted 1s
def convert0s(seq, nSeq):
    #Base case: no change
    if seq.count(0)<3:
        return nSeq
    
    #Determine if the slice contains all 0s
    size = len(seq)
    if sum(seq) == 0:
        #Insert two in middle if slice is even length
        if size//2 == size/2:
            nSeq[size//2],nSeq[size//2-1]=1,1
            
        #Insert one in middle if slice is odd length
        else:
            nSeq[(size-1)//2]=1
            
    else:
        #Call recursively to find largest slices of all 0s
        #First try to pare down ends
        if seq[0]!=0:
            nSeq[1:]=convert0s(seq[1:],nSeq[1:])
            
        elif seq[-1]!=0:
            nSeq[:-1]=convert0s(seq[:-1],nSeq[:-1])

        else:
            #Otherwise find a nonzero value in the middle and call with the slices on either side
            for i in range(1, len(seq)-1):
                if seq[i]!=0:
                    nSeq[:i]=convert0s(seq[:i],nSeq[:i])
                    nSeq[i+1:]=convert0s(seq[i+1:],nSeq[i+1:])
                    break
    return nSeq

#Moves values alternating forwards/backwards
#size - length of the sequence
#seq - current sequence
#nSeq - next sequence
#return nSeq with values moved appropriately
def moveValues(size, seq, nSeq):
    #Initial direction is forward
    d = "f"
    #Iterate through each non-zero value, left-to-right
    for i in range(len(seq)):
        if seq[i]!=0:
            #Remove value from current position, add to destination; toggle direction
            nSeq[i]-=seq[i]
            if d == "f" :
                nSeq[(i+size+seq[i])%size]+=seq[i]
                d = "b"
            
            elif d == "b":
                nSeq[(i+size-seq[i])%size]+=seq[i]
                d = "f"
            
    return nSeq

#Flattens values to no more than the length, to demonstrate periodicity
#size - length of the sequence
#nSeq - sequence to flatten
#returns nSeq flattened with modulo
def flatten(size, nSeq):
    for i in range(size):
        if nSeq[i]>1:
            nSeq[i] = (nSeq[i]-1)%size + 1
        
    return nSeq

#Runs calculator game starting with a sequence of only 0s
#size - length of starting sequence
def main(size):
    #Initialise sequence
    seq = []
    nSeq = []
    for i in range(size):
        seq.append(0)
    doFlatten = False

    #Initialise archive (unused)
    #arch = []
    #for i in range(20):
    #    arch.append(seq.copy())
    
    print(seq)
    #Run 100 iterations; interface here could be improved
    for j in range(100):
        #Create nSeq as a copy of seq
        nSeq = seq.copy()
        #Update the sequence
        nSeq = convert0s(seq,nSeq)
        nSeq = moveValues(size,seq,nSeq)

        #Use modulo to demonstrate perodicity
        if doFlatten:
            nSeq = flatten(size,nSeq)
        
        #Clip values larger than 9 (unimplemented)
        #nSeq = clip(nSeq,9)
        seq = nSeq.copy()

        #Archive (unused)
        #arch.append(seq.copy())
        #arch.pop(0)
        
        #Display
        print(seq)

if __name__=="__main__":
    size = 7
    main(size)
