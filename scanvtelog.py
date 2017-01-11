#!/usr/bin/env python3

# ver1.0
#scanvtelog
#scans vte.log file either in current dir or in command line (Drag n drop)
# send centerx, width,centery,height of every well for every location
#!!! works ony with rectangle and elliptic areas.
# marks are filtered out


import re
import ctypes
import sys
import os

#Get required functions, strcpy..
strcpy = ctypes.cdll.msvcrt.strcpy
ocb = ctypes.windll.user32.OpenClipboard    #Basic Clipboard functions
ecb = ctypes.windll.user32.EmptyClipboard
gcd = ctypes.windll.user32.GetClipboardData
scd = ctypes.windll.user32.SetClipboardData
ccb = ctypes.windll.user32.CloseClipboard
ga = ctypes.windll.kernel32.GlobalAlloc    # Global Memory allocation
gl = ctypes.windll.kernel32.GlobalLock     # Global Memory Locking
gul = ctypes.windll.kernel32.GlobalUnlock
GMEM_DDESHARE = 0x2000


#paste to clipboard
#works with python2 and 3
def Paste( data ):
    ocb(None) # Open Clip, Default task
    ecb()
    if sys.version_info >= (3, 0):
        hCd = ga( GMEM_DDESHARE, len( bytes(data,"ascii") )+1 )
    else:
        hCd = ga(GMEM_DDESHARE, len(bytes(data)) + 1)

    pchData = gl(hCd)

    if sys.version_info >= (3, 0):
        strcpy(ctypes.c_char_p(pchData),bytes(data,"ascii"))
    else:
        strcpy(ctypes.c_char_p(pchData), bytes(data))

    gul(hCd)
    scd(1,hCd)
    ccb()


def getfilename():
    args = sys.argv
    if len(args)==2:
        return args[1]
    else:
        filename = os.getcwd()
        fileout = filename+r'\vte.log'
        return fileout



def decodeline(daline):
    laregexp=re.compile(r'(?<=:)[0-9]+')
    m = laregexp.findall(daline)
    animal=0
    if m[1]=='1':
        animal=m[0]
        laregexp = re.compile(r'\{\(([0-9]+),([0-9]+)\)\(([0-9]+),([0-9]+)\)\}')
        m=laregexp.findall(daline)[0]
#        print (animal,m)
        x1=int(m[0])
        x2=int(m[2])
        y1 = int(m[1])
        y2 = int(m[3])
        newline = animal +"\t"+str((x1+x2)/2)+"\t"+str(abs(x1-x2))+"\t"+str((y1+y2)/2)+"\t"+str(abs(y1-y2))+"\r\n"
        return newline
    return None


textout=''

#gets argument line or vte.log in current dir
filename = getfilename()
if os.path.isfile(filename) == False:
    Paste("File "+filename+" not found")  # paste to clipboard
    exit(1)  #exit if file not found

#opens vte.log file if file exists
with open (filename, "r") as myfile:
    for line in myfile.readlines():
        if line[0:3] =="fig":
            newline = decodeline(line)
            if newline is not None:
                textout = textout + newline


Paste(textout) #paste to clipboard

