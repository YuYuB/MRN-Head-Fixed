# -*- coding: utf-8 -*-
"""
Created on Tuesday 12 Dec 23:39:53 2017

@author: Youcef Bouchekioua & Koji Toda
"""

# Import libralies
import csv
import serial 
import time
import matplotlib.pyplot as plt
from scipy import signal
from scipy import stats
import seaborn as sns
import numpy as np

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

# Initial setting
#SerialP = "/dev/cu.usbmodem1421"
SerialP = "/dev/cu.usbmodem1421"
#SerialP = raw_input("Enter the Serial Port where is connected your device:")
print "Your Serial Port is =", SerialP
print ""
File = raw_input("Enter a file name :")
FileE = File + ".csv"
print "Your file name is =", FileE
print ""
Time = input("Enter the session length in seconds:")
print "The session will last) =", Time
print""
Tableau = []

# Arduino setting
arduino = serial.Serial(SerialP, 115200) 

# Wait Arduino connection
connected = False
while not connected:
    serin = arduino.read()
    connected = True

timeout_start = time.time()
while time.time() < timeout_start + Time:       
    while (arduino.inWaiting()==0): 
        pass # Does Nothing
    arduinoString = arduino.readline()      
    dataArray = arduinoString.split(',')    
    dataArray[0] = int (dataArray[0])
    dataArray[0] = dataArray[0]
    dataArray[1] = int (dataArray[1])
    dataArray[2] = str (dataArray[2])
    dataArray.remove(dataArray[2])           
    print dataArray
    Tableau.append(dataArray)
  
# SAVE 
with open(FileE, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in Tableau:
        writer.writerow(val)



## Open CSV file
#f = open('190904-ArchT993-A.csv', 'r')
f = open(FileE, 'r')
#File = raw_input("Enter a file name :")
FileG = File + ".pdf"
#print "Your file name is =", FileG

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
lick = eventT[np.where(event == 2000)]

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
    for trialLick in range(1,len(psthIndx[0])):
        lickWinTime = preT + lick[psthIndx[0][trialLick]] -rewd[trial]
        psth[trial][lickWinTime] = 1
        timePSTH.append(lickWinTime)
        trialPSTH.append(trial)
        
## Plot Setting
plt.figure(figsize=(5,15))
sns.set(context='notebook'
            , style='white'
            , palette='deep'
            , font='sans-serif'
            , font_scale=1
            , color_codes=False, rc=None
            )

## Raster Plot
plt.subplot(3, 1, 1)
plt.scatter(timePSTH, trialPSTH, s=5, c='k', marker='o'
            , cmap=None, norm=None
            , vmin=None, vmax=None, alpha=None, linewidth=None
            , verts=None, edgecolors=None, hold=None, data=None
            )
plt.xlim(0,timeRange)

## Spike Density Plot
plt.subplot(3, 1, 2)
psthHist = np.sum(psth, axis=0)  
psthDens = signal.savgol_filter(psthHist, 99, 4) # window size 51, polynomial order 3
plt.plot(psthDens
         , c='k', linestyle='solid', linewidth=1
         )
plt.xlim(0,timeRange)
plt.ylim(0,3)

## Averaging Plot with Binned Data
plt.subplot(3, 1, 3)
binSum = []
binSem = []
for secBin in range(0,11):
    binSum.append(np.average(psth[:,secBin*1000:secBin*1000+999])*1000)
    binSem.append(stats.sem(np.sum(psth[:,secBin*1000:secBin*1000+999], axis=1)))
x = np.linspace(-6000, 4000, 11)
plt.errorbar(x, binSum, yerr=binSem, fmt='-o', color='k' 
         , ecolor='k', elinewidth=1
         )
plt.ylim(0,6)
plt.show()
plt.savefig(FileG ,bbox_inches='tight')

## Statistics
#win1 = np.sum(psth[:,6*1000:6*1000+999], axis=1)    # Window 1
#win2 = np.sum(psth[:,7*1000:7*1000+999], axis=1)    # Window 2
#t,p  = stats.ttest_ind(win1,win2,equal_var = False) # Welch's t-test
#p < 0.01        
        
# CLEAR
#%reset

gmail_user = "NezumiDatabase@gmail.com"
gmail_pwd = "micehatepython"

def mail(to, subject, text, attach, image):
    msg = MIMEMultipart()

    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(text))
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(FileE, 'rb').read())
 
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition',
                'attachment; filename="%s"' % os.path.basename(FileE))
    msg.attach(part)

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(FileG, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition',
                'attachment; filename="%s"' % os.path.basename(FileG))
    msg.attach(part)

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()

mail("NezumiDatabase@gmail.com",
     "TEST" ,
     "End of the session" + '\n' + "Please find attached your data  "  , File, FileG)