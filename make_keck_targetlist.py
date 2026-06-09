#using the UT date below, which oyu need to update, this will query
#Horizons for the object given in the command line and return a CSV
#needed for the Palomar telescope target selector int he TCS

def getPosCSV(Hname,JD,verbose=False):

    cmd="https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND=%27{target}%3B%27&CENTER=%27675@399%27&MAKE_EPHEM=%27YES%27&TABLE_TYPE=%27O%27&START_TIME=%27JD{start_jd}%27&STOP_TIME=%27JD{stop_jd}%27&STEP_SIZE=%2715m%27&CSV_FORMAT=%27YES%27&QUANTITIES=%271,3,4,9%27".format(target=Hname,start_jd=JD,stop_jd=JD+1)
    ret=urllib.request.urlopen(cmd,context=gcontext)
    rline=ret.readline().decode('ascii').rstrip()
    while rline!='$$SOE':
        rline=ret.readline().decode('ascii').rstrip()

    while rline!='$$EOE':
        rline=ret.readline().decode('ascii').rstrip()
        rdat=rline.split(',')
        if len(rdat)<8:
            continue
        if rdat[1]=='*':
            continue
        if 'NOFRAG' in Hname:
            nout='c'+Hname.split('=')[1].split('%3B')[0]+'_'+rdat[0].split()[1]
        else:
            nout=Hname+'_'+rdat[0].split()[1]+'UT'

        raout=rdat[3].strip().split()
        decout=rdat[4].strip().split()
        dra=float(rdat[5])/15  #Keck uses sec_per_hour = arcsec_per_hr / 15
        ddec=float(rdat[6])
        vmag=float(rdat[9])
            
        if float(rdat[8])>10:
            print(f"{nout:16s} {int(raout[0]):02d} {int(raout[1]):02d} {float(raout[2]):7.4f} {int(decout[0]):-02d} {int(decout[1]):02d} {float(decout[2]):7.4f} 2000 vmag={vmag:.2f} dra={dra:+.3f} ddec={ddec:+.3f} pa=0.00 lgs=0")


            #"Io 5-27 6:00 UT  07 38 56.6300  21 55 51.8000 2000 vmag=5.951  pa=0.00 lgs=0"

        
    return()

if __name__ == "__main__":
    import urllib.request
    import ssl
    import numpy
    gcontext = ssl.SSLContext() #this is needed to short-circuit an SSL verification error that pops up on Mac OSX for some reason.
    #above is from here: https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
    import astropy
    import sys
        
    
    if len(sys.argv)<2:
        print("runline: get_ast_target.py (horizons_name, use quotes for provisional desigs)")
        exit()


    n=sys.argv[1].strip()
    if n[-1]=='P' and n[0:-1].isnumeric():
        Hname="DES="+n+"%3BCAP%3BNOFRAG"
    else:
        Hname=n.replace(' ','%20')
    
    #UT date
    d='2026-06-29' #leave dashes here for astropy parsing
    getPosCSV(Hname,astropy.time.Time(d).jd)
    
    
    
    
