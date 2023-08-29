#make list files in Data dir of everything observed for processing.
#This assumes the 'standard' structure was followed with files split
#into Dark, Flat, and Target* directories, and will try to name the
#files based on the FITS header info

import os
from astropy.io import fits

folders=os.popen('ls -d */').readlines()
for folder in folders:
    print(folder.rstrip()[0:-1])
    allfits=os.popen('ls '+folder.strip()+'*.fits')


    if 'Dark' in folder:
        targ_hold={}
        for fit in allfits:
            hdu1=fits.open(fit.rstrip())
            et=hdu1[0].header['EXPTIME']
            et_str=str(int(et))+'s'
            if et_str not in targ_hold:
                targ_hold[et_str]=[]
            targ_hold[et_str].append(fit.rstrip())

        for et_str in targ_hold:
            outfn="dark_"+et_str+"_list.dat"
            outf=open(outfn,'w')
            for f in targ_hold[et_str]:
                outf.write(f+'\n')
            outf.close()
            print('wrote dark files to '+outfn)
        
    elif 'Flat' in folder:
        targ_hold_J=[]
        targ_hold_H=[]
        for fit in allfits:
            hdu1=fits.open(fit.rstrip())
            pg=hdu1[0].header['FORE']
            if pg!='PG':
                continue
            filt=hdu1[0].header['AFT']
            if filt=='H__(1.64)':
                targ_hold_H.append(fit.rstrip())
            elif filt=='J__(1.25)':
                targ_hold_J.append(fit.rstrip())

        outfnJ="flat_J_PG_list.dat"
        outfJ=open(outfnJ,'w')
        for f in targ_hold_J:
            outfJ.write(f+'\n')
        outfJ.close()
        print('wrote J flats to '+outfnJ)
        
        outfnH="flat_H_PG_list.dat"
        outfH=open(outfnH,'w')
        for f in targ_hold_H:
            outfH.write(f+'\n')
        outfH.close()
        print('wrote H flats to '+outfnH)
        
    elif 'Target' in folder:
        objnames=[]
        targ_hold_J={}
        targ_hold_H={}
        for fit in allfits:
            hdu1=fits.open(fit.rstrip())
            pg=hdu1[0].header['FORE']
            if pg!='PG':
                continue
            obj=hdu1[0].header['OBJECT']
            objnames.append(obj)
            et=hdu1[0].header['EXPTIME']
            et_str=str(int(et))+'s'
            if et_str not in targ_hold_J:
                targ_hold_J[et_str]=[]
                targ_hold_H[et_str]=[]
            filt=hdu1[0].header['AFT']
            if filt=='H__(1.64)':
                targ_hold_H[et_str].append(fit.rstrip())
            elif filt=='J__(1.25)':
                targ_hold_J[et_str].append(fit.rstrip())

        if len(set(objnames))==1:
            print("using "+objnames[0]+" for "+folder.rstrip()[0:-1]+", verify this is right")
            if objnames[0]=='a20' and folder.rstrip()[0:-1]=='Target5':
                prefix='a393'
            else:
                prefix=objnames[0]
        else:
            print("could not guess object, using "+folder.rstrip()[0:-1])
            prefix=folder.rstrip()[0:-1]
            
        for et_str in targ_hold_J:
            outfnJ=prefix+"_J_PG_"+et_str+"_list.dat"
            outfJ=open(outfnJ,'w')
            for f in targ_hold_J[et_str]:
                outfJ.write(f+'\n')
            outfJ.close()
            print('wrote '+prefix+' J files to '+outfnJ)

        for et_str in targ_hold_H:
            outfnH=prefix+"_H_PG_"+et_str+"_list.dat"
            outfH=open(outfnH,'w')
            for f in targ_hold_H[et_str]:
                outfH.write(f+'\n')
            outfH.close()
            print('wrote '+prefix+' H files to '+outfnH)

            


    
