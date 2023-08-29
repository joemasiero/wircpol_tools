#this will step through each database in the datfiles listed below and
#make a datfile of lit values needed for plotting

import sys

if len(sys.argv)<2:
    print("runline: get_lit.py (ast number)")
    exit()

find_obj=sys.argv[1]


datfiles=["/Users/jmasiero/PDS/asteroid_polarimetric_database_V2_0/data/apd.csv","/Users/jmasiero/Polar/CalernAsteroidPolSurvey/caps.dat","/Users/jmasiero/Polar/CalernAsteroidPolSurvey/casleo.dat"]

header="#band  phase  pol   err  ref"
print(header)



for df in datfiles:
    datfile=open(df)
    
    for line in datfile.readlines():
        if 'Calern' in df:
            dat=line.rstrip().split()
            name=dat[0]
            filt=dat[6]
            phase=dat[3]
            unc=dat[5]
            pol=dat[4]
            ref="Bendjoya22"
        else:
            dat=line.rstrip().split(',')
            name=dat[0]
            filt=dat[4]
            phase=dat[5]
            unc=dat[7]
            pol=dat[10]
            ref=dat[14].replace(' ','')
        if name!=find_obj:
            continue
        
        if unc=='-999.99':
            unc='0.2'
    
        if pol=='-999.99':
            continue
        
        print(filt,phase,pol,unc,ref)

