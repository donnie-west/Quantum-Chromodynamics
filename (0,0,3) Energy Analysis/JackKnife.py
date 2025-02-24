'''
Temple RSP
Experimental JackKnife calculation
- Solves initial data set
- Handles multiple initial data points
- Implementation of user input for data points and omission number  
'''
import math
from itertools import combinations
from sympy import *


def AvgOverBins(Ndata,Nomit,dArr):
    '''
    Returns an array of doubles that signify the average of
    remaining data in each bin
    '''
    #Initializing bin array and number of bins
    BinArr = list(combinations(dArr,(Ndata-Nomit)))
    #print(BinArr)
    #print(sum(BinArr))
    DArr = []

    #Calculating the average over remaining data
    for i in BinArr:
        avg = sum(i)/(Ndata-Nomit)
        #print(avg)
        DArr.append(avg)        

    return DArr

def AvgOfBins(DArr):
    '''
    Returns the average of the bins
    '''
    #print(sum(DArr))
    #print(len(DArr))
    #print(sum(DArr)/len(DArr))
    return sum(DArr)/len(DArr)

def StatError(DArr,DAvg):
    '''
    Returns the statistical error of the average of bins
    '''
    x = symbols('x')
    expression = sqrt(x)
    sum = 0

    for i in DArr:
        sum += pow((i-DAvg),2)

    print(sum)
    
    if sum >= 0:
        return math.sqrt(sum) * math.sqrt((len(DArr)-1)/(len(DArr)))
    else:
        lim = limit(expression,x,sum)
        return lim * math.sqrt((len(DArr)-1)/(len(DArr)))


if __name__ == "__main__":
    #Initial data set
    dArr = [1.0,1.2,0.9,1.1]
    Ndata = 4
    Nomit = 1

    #User input option
    '''
    dArr = []
    Ndata = 0

    while True:
        di = input("Please enter a data point: ")
        
        if di == 'done':
            break

        d.append(float(di))
        Ndata += 1

    print('')

    Nomit = int(input("How many data points to omit? "))

    print('')
    '''

    AoverB = AvgOverBins(Ndata,Nomit,dArr)
    AoB = AvgOfBins(AoverB)

    #print("The average of remaining data in each bin is {}".format(AoverB))
    #print("The average of the bins is {}".format(round(AoB,5)))
    #print("The statistical error is {}".format(round(StatError(AoverB,AoB),5)))


