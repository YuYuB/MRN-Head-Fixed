#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 14:14:44 2018
@author: Koji Toda, Ph.D.

"""

## Libraries
import matplotlib.pyplot as plt
from scipy import signal
from scipy import stats
import seaborn as sns
import numpy as np
import csv
import glob
import re
import pandas as pd

"""

plt.figure(figsize=(5,15))
sns.set(context='notebook'
            , style='white'
            , palette='deep'
            , font='sans-serif'
            , font_scale=1
            , color_codes=False, rc=None
            )
"""

for FileE in glob.glob('*.csv'):

    ## Open CSV file
   ## f = open('200609-304-TrD4.csv', 'r')
    with open(FileE, 'r') as f:   

        rowNum    = np.array(0)
        event     = []
        eventT    = []
        
        reader    = csv.reader(f)
        header    = next(reader)
        for row in reader:    
            eCSV   = int(row[0])
            tCSV   = int(row[1])  
            event.append(eCSV)
            eventT.append(tCSV)
            rowNum = rowNum + 1
        
        event   = np.array(event)
        eventT  = np.array(eventT)
        
        rewd = eventT[np.where(event == 5000)]
        lick = eventT[np.where(event == 8000)]
        
        
        ## PSTH Matrix
        timePSTH  = []
        trialPSTH = []
        trialStart  = 0
        trialEnd    = len(rewd) - 1
        preT        = 6000
        postT       = 4000
        trialRange  = trialEnd - trialStart
        timeRange   = preT + postT
        psth = np.zeros((trialRange,timeRange))
        
        
        #Trial Loop
        for trial in range(trialStart,trialEnd):
            psthIndx = np.where((lick > rewd[trial]-preT) & (lick < rewd[trial]+postT))
        
        #Time Loop
        #    for trialLick in range(1,len(psthIndx[0])):
            for trialLick in range(1,len(psthIndx[0])):    
                lickWinTime = preT + lick[psthIndx[0][trialLick]] -rewd[trial]
                psth[trial][lickWinTime] = 1
                timePSTH.append(lickWinTime)
                trialPSTH.append(trial)
                Table = []
                Table.append(timePSTH)
                Table.append(trialPSTH)

    
    #plt.subplot(1, 1, 1)            
    plt.scatter(timePSTH, trialPSTH, s=1, c='k', marker='o'
            , cmap=None, norm=None
            , vmin=None, vmax=None, alpha=None, linewidth=None
            , verts=None, edgecolors=None, hold=None, data=None
            )
    plt.xlim(0,timeRange)
    
    plt.savefig(FileE.strip('.csv') + '_Graph.png')
    plt.show()
    
    
                    
"""                
        FileE_mod1 = FileE.strip('.csv') + '_event.csv'        
        with open(FileE_mod1, "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(Table)
"""
                
"""                
    ## Averaging Plot with Binned Data
    plt.subplot(2, 1, 2)
    binSum = []
    binSem = []
    for secBin in range(0,11):
        binSum.append(np.average(psth[:,secBin*1000:secBin*1000+999])*1000)
        binSem.append(stats.sem(np.sum(psth[:,secBin*1000:secBin*1000+999], axis=1)))
    
    
    x = np.linspace(-6000, 4000, 11)
    plt.errorbar(x, binSum, yerr=binSem, fmt='-o', color='k' 
             , ecolor='k', elinewidth=1
             )
    
    plt.ylim(0,10)
    
"""                 



    
     
    
         
                
"""                 
               

                
"""                
                
                    ## Plot Setting


## Raster Plot
#
"""
    ## Spike Density Plot
    plt.subplot(3, 1, 2)
    psthHist = np.sum(psth, axis=0)  
    psthDens = signal.savgol_filter(psthHist, 99, 4) # window size 51, polynomial order 3
    plt.plot(psthDens
             , c='k', linestyle='solid', linewidth=1
             )
    plt.xlim(0,timeRange)
    plt.ylim(0,3)


                
    
        
"""        
    
            
    
  
    




"""
## Statistics
win1 = np.sum(psth[:,6*1000:6*1000+999], axis=1)    # Window 1
win2 = np.sum(psth[:,7*1000:7*1000+999], axis=1)    # Window 2
t,p  = stats.ttest_ind(win1,win2,equal_var = False) # Welch's t-test
p < 0.01
"""