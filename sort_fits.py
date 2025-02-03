import os
import sys
from astropy.io import fits

#run in Data directory

if not os.path.exists('Dark'):
    os.system("mkdir Dark")
if not os.path.exists('Flat'):
    os.system("mkdir Flat")


allfits=os.popen('ls *[0123456789].fits').readlines()

targets={}

nexttarget=1
prevtarg=os.popen("ls -d Target*").readlines()
for t in prevtarg:
    tcount=int(prevtarg.rstrip().split('Target')[1])
    if tcount>nexttarget:
        nexttarget=tcount

for ffile in allfits:
    fn=ffile.rstrip()
    indat=fits.open(fn)
    header=indat[0].header
    indat.close()
    
    if header['OBSTYPE'] == 'dark' or header['OBJECT'] in ['dark','Dark'] or (header['FORE']=='BrGamma__(2.17)' and header['AFT']=='J__(1.25)'):
        os.system(f"mv {fn:s} Dark")
    elif header['OBSTYPE'] == 'flat' or header['OBJECT'] in ['flat','Flat']:
        os.system(f"mv {fn:s} Flat")
    elif header['OBSTYPE'] in ['object','none'] :
        tname=header['OBJECT']
        if tname not in targets:
            targets[tname]=f"Target{nexttarget:d}"
            print(f"assigning {tname:s} to {targets[tname]:s}")
            os.system(f"mkdir {targets[tname]:s}")
            nexttarget+=1
        os.system(f"mv {fn:s} {targets[tname]:s}/")
    else:
        print(f"  ---Error: Don't know what to do with {fn:s}")
    
    
