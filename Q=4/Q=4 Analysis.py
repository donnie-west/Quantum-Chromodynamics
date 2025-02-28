import os
import decimal
import JackKnife
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sympy import *
from IPython.display import display


def hash(fileArr):
    positions = ['+4_+0_-3',
                 '-4_+0_-3',
                 '+0_+4_-3',
                 '+0_-4_-3',
                 '+4_+0_+3',
                 '-4_+0_+3',
                 '+0_+4_+3',
                 '+0_-4_+3']
    
    fileDict =  {'+4_+0_-3':[],
                 '-4_+0_-3':[],
                 '+0_+4_-3':[],
                 '+0_-4_-3':[],
                 '+4_+0_+3':[],
                 '-4_+0_+3':[],
                 '+0_+4_+3':[],
                 '+0_-4_+3':[]}

    for i in range(len(fileArr)):
        for j in positions:
            if fileArr[i].rfind(j) == -1:
                pass
            else:
                fileDict[j].append(fileArr[i])
                continue

    return fileDict

def DictionaryInitialization(stopPointTime):
    Dict = {}
    for i in range(stopPointTime + 1):
        Dict.update({i: []})
    return Dict

def DirectoryToDictionary(dirname,dirlist,stopPointTime,stopPointFile):
    
    dirdicti = DictionaryInitialization(stopPointTime)
    
    #print(dirlist)
    
    for t in range(stopPointFile):
        file = os.path.join(dirname, dirlist[t])
        FileToMatrix(file, dirdicti, stopPointTime)

    #print(dirdicti)

    return dirdicti

def FileToMatrix(filename, dirdict, stopPointTime=20):
    file = open(filename, "r")

    for line in file:

        parsed = line.split()

        parsed[0] = int(float(parsed[0]))

        if parsed[0] == stopPointTime + 1:
            break

        parsed[1] = decimal.Decimal(parsed[1])

        dirdict[parsed[0]].append(parsed[1])
        
    file.close()

def Bins(stopPointTime,stopPointFile,dirdict):
    bins = DictionaryInitialization(stopPointTime)
    
    for i in range(stopPointTime+1):
        bins[i] = JackKnife.AvgOverBins(stopPointFile, 1, dirdict[i])
    return bins

def LogsOfBins(bins,stopPointFile):
    logs2 = {}
    
    for i in range(stopPointTime):
        logs2.update({'t{}/t{}'.format(i, i+1): []})
        for j in range(stopPointFile):
            #print(i)
            #print(j)
            #print(bins[i][j])
            #print(math.log(bins[i][j]/bins[i+1][j]))
            div = bins[i][j]/bins[i+1][j]
            
            #print(i)
            #print(div)
            if div < 0:
                logs2['t{}/t{}'.format(i, i+1)].append(0)
            else:
                logs2['t{}/t{}'.format(i, i+1)].append(math.log(div))
                       
            
    return logs2

def AvgOfBinLogs(logs2):
    arr = []
    Davg = {}
        
    for i in range(stopPointTime):
        arr.append('t{}/t{}'.format(i, i+1))

    for i in range(stopPointTime):
        Davg['t{}/t{}'.format(i, i+1)] = JackKnife.AvgOfBins(logs2[arr[i]])
        
    return Davg

def StatErrorOfBinLogs(logs2,Davg):
    arr = []
    StatError = {}
    
    for i in range(stopPointTime):
        arr.append('t{}/t{}'.format(i, i+1))

    for i in range(stopPointTime):
        StatError['t{}/t{}'.format(i,i+1)] = JackKnife.StatError(logs2[arr[i]], Davg[arr[i]])

    return StatError

if __name__ == '__main__':
    stopPointTime = 20
    positions = ['+4_+0_-3',
                 '-4_+0_-3',
                 '+0_+4_-3',
                 '+0_-4_-3',
                 '+4_+0_+3',
                 '-4_+0_+3',
                 '+0_+4_+3',
                 '+0_-4_+3']
    
    posDir = {}
    error = []
    dirlist = os.listdir('PolTwop_Q=4')
    #print(dirlist)
    filesByPosition = hash(dirlist)

    for pos in positions:
        stopPointFile = len(filesByPosition[pos])
        dir = DirectoryToDictionary('PolTwop_Q=4',filesByPosition[pos],stopPointTime,stopPointFile)
        bins = Bins(stopPointTime,stopPointFile,dir)
        logs = LogsOfBins(bins,stopPointFile)
        logsAvg = AvgOfBinLogs(logs)
        posDir.update({pos:logsAvg})
        staterr = StatErrorOfBinLogs(logs,logsAvg)
        error.append(staterr)

    times = logsAvg.keys()
    
    values = logsAvg.values()

    xr = np.arange(0,stopPointTime)
    yr = np.arange(-2,3,step=0.2)
    zeroes = []
    
    for x in range(20):
        zeroes.append(0)

    fig, ax = plt.subplots()
    
    plt.title('Averages of Q=4 Energy')

    plt.plot(posDir['+4_+0_-3'].values(),marker='o',markersize='4',label='+1_+0_-3')
    plt.plot(posDir['-4_+0_-3'].values(),marker='*',markersize='4',label='+1_+0_-3')
    plt.plot(posDir['+0_+4_-3'].values(),marker='^',markersize='4',label='+1_+0_-3')
    plt.plot(posDir['+0_-4_-3'].values(),marker='v',markersize='4',label='+1_+0_-3')
    plt.plot(posDir['+4_+0_+3'].values(),marker='o',markersize='4',label='+1_+0_-3')
    plt.plot(posDir['-4_+0_+3'].values(),marker='*',markersize='4',label='+1_+0_-3')
    plt.plot(posDir['+0_+4_+3'].values(),marker='^',markersize='4',label='+1_+0_-3')
    plt.plot(posDir['+0_-4_+3'].values(),marker='v',markersize='4',label='+1_+0_-3')
    plt.plot(xr,zeroes,color='k')

    plt.legend(loc='upper left')
    plt.grid(visible=True,linestyle='--')
    #plt.xticks(np.arange(0,20),times)
    
    ax.set_xticks(xr)
    #ax.set_yticks(yr)
    plt.xlabel('tx/tx+1')
    plt.ylabel('Averages')
    
    ax.tick_params(axis='both', labelsize=7)

    
    plt.errorbar(xr,posDir['+4_+0_-3'].values(),yerr=list(error[0].values()))
    plt.errorbar(xr,posDir['-4_+0_-3'].values(),yerr=list(error[1].values()))
    plt.errorbar(xr,posDir['+0_+4_-3'].values(),yerr=list(error[2].values()))
    plt.errorbar(xr,posDir['+0_-4_-3'].values(),yerr=list(error[3].values()))
    plt.errorbar(xr,posDir['+4_+0_+3'].values(),yerr=list(error[4].values()))
    plt.errorbar(xr,posDir['-4_+0_+3'].values(),yerr=list(error[5].values()))
    plt.errorbar(xr,posDir['+0_+4_+3'].values(),yerr=list(error[6].values()))
    plt.errorbar(xr,posDir['+0_-4_+3'].values(),yerr=list(error[7].values()))
    
    plt.show()



