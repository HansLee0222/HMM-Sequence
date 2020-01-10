import numpy as np
import pandas as pd
from math import log
import io
def backward(seq):
    H = []
    L = []
    prevN = 0
    currN=1
    prevP = 0
    currP = 1
    H.append(1)
    L.append(1)
    #Start at the very back
    if seq[len(seq)-1] == 'A' or seq[len(seq)-1] == 'T':
        currP = 0.5*0.2+0.5*0.3

        currN = 0.4*0.2+0.6*0.3
        H.append(currP)
        L.append(currN)
    elif seq[len(seq)-1] == 'G' or seq[len(seq)-1] == 'C':
        currP = 0.5*0.3+0.5*0.2
        currN = 0.4*0.3+0.6*0.2
        H.append(currP)
        L.append(currN)
    else:
        print("Wrong input within sequence")
        exit(0)
    #start at the third to last column
    for i in range(len(seq)-3,-1,-1):
        prevP = currP
        prevN = currN
        if seq[i+1] == 'G' or seq[i+1] == 'C':

            currP = 0.5*0.3*prevP+0.5*0.2*prevN
            currN = 0.4*0.3*prevP+0.6*0.2*prevN
            H.append(currP)
            L.append(currN)
        elif seq[i+1] == 'A'or seq[i+1]=='T':


            currP = 0.5*0.2*prevP+0.5*0.3*prevN
            currN = 0.4*0.2*prevP + 0.6*0.3*prevN
            H.append(currP)
            L.append(currN)
        else:
            print('Wrong input within sequence')
            exit(0)
    # The very last item
    if seq[0] == 'G' or seq[0] == 'C':
        currP = 0.5*0.3*currP+0.5*0.2*currN

    else:
        currP = 0.5*0.2*currP+0.5*0.3*currN
    #reverse since it was done in the oppsite way
    H = H[::-1]
    L = L[::-1]

    return H,L,currP

def forward(seq):
    prevN = 0
    prevP = 0
    currN = 0
    currP = 0
    H=[]
    L = []
    #initialize the first column
    if seq[0] == 'G' or seq[0] =='C':
        currP += 0.5*0.3
        currN += 0.5*0.2
        H.append(currP)
        L.append(currN)
    elif seq[0] =='A' or seq[0] == 'T':
        currP += 0.5*0.2
        currN +=0.5*0.3
        H.append(currP)
        L.append(currN)
    else:
        print("Wrong input within sequence")
        exit(0)
    #forward algorithm
    for i in range(1,len(seq)):
        prevP = currP
        prevN = currN
        if seq[i] == 'G' or seq[i]=='C':
            currP =  0.3*(0.5*prevP+0.4*prevN)
            currN = 0.2*0.6*prevN+0.5*0.2*prevP
            H.append(currP)
            L.append(currN)
        else:
            currP =  0.2*0.5*prevP+0.4*0.2*prevN
            currN =0.3*0.6*prevN+0.5*0.3*prevP
            H.append(currP)
            L.append(currN)

    return H,L,currP+currN

def viterbi(seq):
    #Done in Log based 2
    Nfrom = []
    Pfrom = []
    count = 0
    prevN = 0
    prevP = 0
    currN = 0
    currP = 0
    H =[]
    L = []
    path = []
    #inifinity
    H.append(float('-inf'))
    L.append(float('-inf'))
    #First column
    if seq[0] =='G' or seq[0] == 'C':
        currN = round(log(0.2,2)+log(0.5,2),2)
        L.append(currN)
        currP = round(log(0.5,2)+ log(0.3,2),2)
        H.append(currP)
    elif seq[0] =='A' or seq[0] == 'T':
        currP +=round( log(0.5,2)+log(0.2,2),2)
        H.append(currP)
        currN += round(log(0.5,2)+log(0.3,2),2)
        L.append(currN)
    else:
        print("Wrong input within sequence")

    for i in range(1,len(seq)):
        #prevN and prevP are temps
        prevN = currN
        prevP = currP
        if seq[i] == 'G' or seq[i]=='C':
            currP = round( log(0.3,2)+ max(prevP+log(0.5,2), prevN+log(0.4,2)),2)
            H.append(currP)
            if prevP+log(0.5,2)>prevN+log(0.4,2):
                Pfrom.append('H')
            elif prevP+log(0.5,2)<prevN+log(0.4,2):
                Pfrom.append('L')
            else:
                #check if there are more than one path
                Pfrom.append('H')
                count +=1
            currN = round(log(0.2,2)+ max(prevP+log(0.5,2), prevN+log(0.6,2)),2)
            if prevP+log(0.5,2)>prevN+log(0.6,2):
                Nfrom.append('H')
            elif prevP+log(0.5,2)<prevN+log(0.6,2):
                Nfrom.append('L')
            else:
                Pfrom.append('H')
                count +=1
            L.append(currN)

        else:
            currP = round(log(0.2,2)+ max(prevP+log(0.5,2), prevN+log(0.4,2)),2)
            H.append(currP)
            if prevP+log(0.5,2)>prevN+log(0.4,2):
                Pfrom.append('H')
            elif prevP+log(0.5,2)<prevN+log(0.4,2):
                Pfrom.append('L')
            else:
                Pfrom.append('H')
                count +=1

            currN = round(log(0.3,2)+ max(prevP+log(0.5,2), prevN+log(0.6,2)),2)
            L.append(currN)
            if prevP+log(0.5,2)>prevN+log(0.6,2):
                Nfrom.append('H')
            elif prevP+log(0.5,2)<prevN+log(0.6,2):
                Nfrom.append('L')
            else:
                count +=1
                Nfrom.append('H')

    prob = 0
    if currN<currP:
        path.append('H')
    else:
        path.append('L')
    for i in range(1,len(H)-1):
        if path[i-1] == 'L':
            #pointer for the previous
            path.append(Nfrom[len(Nfrom)-i])
        else:
            path.append(Pfrom[len(Pfrom)-i])
    #reverse
    path = path[::-1]
    g = np.exp2(H)
    c = np.exp2(L)
    if path[len(path)-1] == 'L':
        prob= c[c.size-1]
    else:
        prob = g[g.size-1]



    return H,L,path



lines = input("Enter Sequence: ")
x,y,z = backward(lines)
q,r,s = forward(lines)
a,b, path= viterbi(lines)



print("Optimal Path: ", path)
names =[]
names.append('0')
zeros = []
zeros.append('0')
for i in range(len(b)-1):
    zeros.append(float('-inf'))
for item in lines:
    names.append(item)


formmated = pd.DataFrame(data = (zeros,a,b),columns = names,index = ('0','H','L') )
print("HMM table: \n",formmated, end = '\n')
#c = forward(lines[1])


print("\nSequence Probability: ", z)
