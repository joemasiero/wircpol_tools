#query horizons to get the expected scattering plane for each object
#in 'ob'.  This needs nss for Time conversion

def getPlane(Hname,JD,verbose=False):
    
#    cmd="https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1&COMMAND=%27{target}%3B%27&CENTER=%27675@399%27&MAKE_EPHEM=%27YES%27&TABLE_TYPE=%27O%27&START_TIME=%27JD{start_jd}%27&STOP_TIME=%27JD{stop_jd}%27&STEP_SIZE=%272d%27&CSV_FORMAT=%27YES%27&QUANTITIES=%2727%27".format(target=Hname,start_jd=JD,stop_jd=JD+1)
    cmd="https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND=%27{target}%3B%27&CENTER=%27675@399%27&MAKE_EPHEM=%27YES%27&TABLE_TYPE=%27O%27&START_TIME=%27JD{start_jd}%27&STOP_TIME=%27JD{stop_jd}%27&STEP_SIZE=%272d%27&CSV_FORMAT=%27YES%27&QUANTITIES=%2727%27".format(target=Hname,start_jd=JD,stop_jd=JD+1)
    ret=urllib.request.urlopen(cmd,context=gcontext)
    rline=ret.readline().decode('ascii').rstrip()
    while rline!='$$SOE':
        rline=ret.readline().decode('ascii').rstrip()
    rline=ret.readline()
    adat=rline.decode('ascii').rstrip().split(',')
    date=adat[0]
    ang=float(adat[3].strip())
    
    while ang>180:
        ang-=180
    if ang<0:
        ang+=180

    #this is perpendicular to the above, to align with polarization nomenclature where positive is 'perpendicular to the scattering plane
    ang_prime=90+ang
    if ang_prime>180:
        ang_prime-=180

    #negative and positive pol angles
    return(ang,ang_prime)


if __name__ == "__main__":
    import urllib.request
    import ssl
    import numpy
    gcontext = ssl.SSLContext() #this is needed to short-circuit an SSL verification error that pops up on Mac OSX for some reason.
    #above is from here: https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
    import nss
    
    
    
    obs={'387':"2022 10 15.1", 
         '4':"2022 10 15.125",
         '72':"2022 10 15.16",
         '24':"2022 10 15.22",
         '3':"2022 10 15.23",
         '38':"2022 10 15.25",
         '31':"2022 10 15.28",
         '46':"2022 10 15.29",
         '172':"2022 10 15.33",
         '349':"2022 10 15.37",
         '236':"2022 10 15.42",
         '980':"2022 10 15.5",
         '2':"2022 10 15.55"}
    
    for n,d in obs.items():
        (n_ast_plane,p_ast_plane)=getPlane(n,nss.Time(d,'ymd').jd)
        print("{name:>4s}: pos={pang:6.2f} neg={nang:6.2f}".format(name=n,pang=p_ast_plane,nang=n_ast_plane))
    
    
