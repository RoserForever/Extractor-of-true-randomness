import math
from random import getrandbits
TOKEN_LENGTH = 8
filename = 'data1000.1.txt'
outputfile = 'Truerandomness.txt'
t = 0
Ocr = 0
tokensDict = dict()
occurrence = 0
maxToken, temp = '', ''

a = open(filename, 'r').read().replace("\n", "")

for i in range(0, len(a) - TOKEN_LENGTH, TOKEN_LENGTH):
    temp = a[i:i + TOKEN_LENGTH]
    tokensDict[temp] = tokensDict.get(temp, 0) + 1
for i in tokensDict.keys():
    if tokensDict[i] > occurrence:
        occurrence = tokensDict[i]
        maxToken = i

t= maxToken
Ocr = occurrence
n = len(a)
Pmax = Ocr/(n/TOKEN_LENGTH)
Hmin = -math.log(Pmax,2)
e = 10**(-30)
m = int(Hmin + 2*math.log((1/e),2))
Rand_Length = n+m-1
def randtoken(l):
    res = ''
    for i in range(l):
        res+= str(getrandbits(1))
    return res


# TODO - token to matrix
def toTable(n,m):
    print(n,m)
    res = [''] * m
    res[0] = randtoken(n)
    for i in range(1,m):
        res[i] = str(getrandbits(1)) + res[i-1] [:-1]
    return res
def multiplymatrix (a,b):
    res = ''
    for i in range (len(b)):
        temp = 0
        for j in range(len(a)) :
            temp = temp ^ (int(a[j]) & int(b[i][j]))
        res+= str(temp)
    return res
event = (multiplymatrix(a,toTable(n,m)))
file = open(outputfile, 'w')
file.write(event)
print(event)
file.close()
