# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 10:43:14 2025

@author: donte
"""
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


def DictionaryInitialization(stopPointTime):
    Dict = {}
    for i in range(stopPointTime + 1):
        Dict.update({i: []})
    return Dict

def sort(filename):
    joiner = ''
    
    for char in filename:
        if char == '_':
            break
        joiner += char
        
    return int(joiner)

def DirectoryToDictionary(dirname,stopPointTime,stopPointFile,Ocol,Icol):
    dirlist = os.listdir(dirname)
    
    dirlist.pop(len(dirlist)-1)
    
    dirdict = DictionaryInitialization(stopPointTime)
    
    dirlist.sort(key=sort)
    #print(dirlist)
    
    for t in range(stopPointFile):
        file = os.path.join(dirname, dirlist[t])
        FileToMatrix(file, dirdict,Ocol,Icol, stopPointTime)

    return dirdict

def FileToMatrix(filename, dirdict, Ocol, Icol, stopPointTime=20):
    """
    Create a matrix based on the first two columns of a single file.
    Appends positive momentum value to dictionary depending on the time it was
    taken.

    Parameters
    ----------
    filename : String
        DESCRIPTION.
    dirdict : Dictionary
        DESCRIPTION.
    stopPointTime : Integer, optional
        DESCRIPTION. The default is 20.

    Returns
    -------
    matrix : TYPE
        DESCRIPTION.

    """
    f = open(filename, "r")
    matrix = []
    # Loop goes line by line in the file to return
    for i in f:
        # Parses the line by the whitespace in between columns
        parsed = i.split()
        # Omits the negative momentum
        parsed[0] = int(float(parsed[0]))
        
        parsed.pop(Ocol)
        # Stops the loop early if the user doesn't want to analyze all times
        if parsed[0] == stopPointTime + 1:
            break
        
        parsed[Icol] = decimal.Decimal(parsed[Icol])

        dirdict[parsed[0]].append(parsed[Icol])
        matrix.append(parsed)
        
    f.close()

    return matrix

def Bins(stopPointTime,stopPointFile,dirdict):
    bins = DictionaryInitialization(stopPointTime)
    
    for i in range(stopPointTime+1):
        bins[i] = JackKnife.AvgOverBins(stopPointFile, 1, dirdict[i])
    return bins

def LogsOfBins(bins):
    logs2 = {}
    x = symbols('x')
    expression = log(x)
    
    for i in range(stopPointTime):
        logs2.update({'t{}/t{}'.format(i, i+1): []})
        for j in range(stopPointFile):
            #print(i)
            #print(j)
            #print(bins[i][j])
            #print(math.log(bins[i][j]/bins[i+1][j]))
            div = bins[i][j]/bins[i+1][j]
            
            
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


if __name__ == "__main__":
    filearr = []
    stopPointFile = 397
    stopPointTime = 20
    
    Posdirdict = DirectoryToDictionary('PolTwopSink', stopPointTime, stopPointFile,2,1)
    #print(Posdirdict)
    #print(dirdict[0])
    Negdirdict = DirectoryToDictionary('PolTwopSink', stopPointTime, stopPointFile,1,1)
    #print(Negdirdict)
    
    Posbins = Bins(stopPointTime, stopPointFile, Posdirdict)
    #print(bins)
    Poslogsofbins = LogsOfBins(Posbins)
    #print(logsofbins)
    Posbinlogavg = AvgOfBinLogs(Poslogsofbins)
    #print(binlogavg)
    Posstaterror = StatErrorOfBinLogs(Poslogsofbins, Posbinlogavg)
    #print(StatErrorOfBinLogs)
    
    Negbins = Bins(stopPointTime, stopPointFile, Negdirdict)
    #print(bins)
    Neglogsofbins = LogsOfBins(Negbins)
    #print(logsofbins)
    Negbinlogavg = AvgOfBinLogs(Neglogsofbins)
    #print(binlogavg)
    Negstaterror = StatErrorOfBinLogs(Neglogsofbins, Negbinlogavg)
    #print(StatErrorOfBinLogs)
    
    for i in range(stopPointFile):
        filearr.append('File {}'.format(i+1))
    
    Posbindf = pd.DataFrame(Posbins, index=filearr)
    Poslogsofbinsdf = pd.DataFrame(Poslogsofbins, index=filearr)
    Posbinlogavgdf = pd.DataFrame(Posbinlogavg, index = ['Averages of Natural Log of Bins'])
    Posstaterrordf = pd.DataFrame(Posstaterror,index = ['Statistical Error of Logged Bins'])
    
    Negbindf = pd.DataFrame(Negbins, index=filearr)
    Neglogsofbinsdf = pd.DataFrame(Neglogsofbins, index=filearr)
    Negbinlogavgdf = pd.DataFrame(Negbinlogavg, index = ['Averages of Natural Log of Bins'])
    Negstaterrordf = pd.DataFrame(Negstaterror,index = ['Statistical Error of Logged Bins'])
    
    '''
    print('====Bins====')
    display(bindf)
    
    print('')
    print('====Natural Logs of Bins====')
    display(logsofbinsdf)
    
    print('')
    print('====Averages of Natural Logs of Bins====')
    print(binlogavg)
    print('')
    print('====Statistical Error of Averages====')
    print(staterror)
    with pd.ExcelWriter('TwoPointers.xlsx') as writer:
        bindf.to_excel(writer, sheet_name='Bins', index=True)
        logsofbinsdf.to_excel(writer, sheet_name='Logs of Bins', index=True)
        binlogavgdf.to_excel(writer, sheet_name='Average of Logs of Bins', index=True)
        staterrordf.to_excel(writer, sheet_name='Statistical Error', index=True)
        
    '''
    
    times = Posbinlogavg.keys()
    
    Posvalues = Posbinlogavg.values()
    Poserror = Posstaterror.values()
    
    Negvalues = Negbinlogavg.values()
    Negerror = Negstaterror.values()
    #print(error)
    xr = np.arange(0,stopPointTime)
    yr = np.arange(-2,3,step=0.2)
    zeroes = []
    
    for x in range(20):
        zeroes.append(0)
    
    #print(times)
    #print(values)
    fig, ax = plt.subplots()
    
    plt.title('Averages of Negative and Positive Momentum Energies')

    plt.plot(Posvalues,marker='o',markersize='4',color='b',label='Positive Momentum')
    plt.plot(Negvalues,marker='^',markersize='4',color='y',label='Negative Momentum')
    plt.plot(xr,zeroes,color='k')
    
    plt.legend(loc='upper left')
    plt.grid(visible=True,linestyle='--')
    #plt.xticks(np.arange(0,20),times)
    
    ax.set_xticks(xr)
    ax.set_yticks(yr)
    plt.xlabel('tx/tx+1')
    plt.ylabel('Averages')
    
    ax.tick_params(axis='both', labelsize=7)
    
    
    plt.errorbar(xr,Posvalues,yerr=list(Poserror),ecolor='r')
    plt.errorbar(xr,Negvalues,yerr=list(Negerror),ecolor='k')

    plt.show()




