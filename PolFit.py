import numpy
import scipy.optimize as sciopt
import matplotlib.pyplot as plt
import urllib.request
import ssl
import random

def ppcurve(p,x):
    #assume p['b']=-1 to ensure alpha=0 is pol=0
    #pout=p['a'] * (numpy.e**(-x/p['d']) + p['b']) + p['k']*x

    #p[0]=A, p[1]=k, p[2]=d
    pout=p[0] * (numpy.e**(-x/p[2]) -1) + p[1]*x
    return pout

def ppdiff(p,x,y):
    return y - ppcurve(p,x)


def PolPhase(phase,pol,p0=None):

    #following Muinonen et al. 2009.
    
    #if p0==None:
    #    p0={}
    #    p0['a']=5.5  #amplitude param
    #    p0['k']=0.22 #slope param
    #    p0['b']=-1  #assumed to ensure P=0 at alpha=0
    #    p0['d']=10.  #width of negative branch

    p0=[5.5,0.22,10]

    if 0 not in phase:
        #ensure the 0,0 point is fit and fixed
        go_phase=numpy.asarray(phase+[0])
        go_pol=numpy.asarray(pol+[0])
    else:
        go_phase=numpy.asarray(phase)
        go_pol=numpy.asarray(pol)

    
    pres = sciopt.leastsq(ppdiff,p0,args=(go_phase,go_pol),full_output=True)

    p_out=pres[0]

    #print(p_out)
    
    phold=99
    inv_angle=0
    for a in numpy.arange(5,40,0.1):
        ptest=ppcurve(p_out,a)
        if abs(ptest)<phold:
            phold=abs(ptest)
            inv_angle=a

    pol_params={}
            
            
#    slope=(p_out['b']*p_out['a'] + p_out['k']*inv_hold + p_out['k']*p_out['d'])/p_out['d'] 
    slope=(-1*p_out[0] + p_out[1]*inv_angle + p_out[1]*p_out[2])/p_out[2] 



#    alpha_min=-p_out['d']*numpy.log(p_out['k']*p_out['d']/p_out['a'])
    alpha_min=-p_out[2]*numpy.log(p_out[1]*p_out[2]/p_out[0])

#    Pmin=p_out['k']*p_out['d'] * (1-numpy.log(p_out['k']*p_out['d']/p_out['a'])) + p_out['b']*p_out['a']
    Pmin=p_out[1]*p_out[2] * (1-numpy.log(p_out[1]*p_out[2]/p_out[0])) - p_out[0]

    pol_params['inversion_angle']=inv_angle
    pol_params['h_slope']=slope
    pol_params['alpha_min']=alpha_min
    pol_params['P_min']=Pmin

    print(pol_params)
    return(p_out,pol_params)



def PolPhaseError(phase,pol,perr,p0=None,nmc=100):

    #run a monte carlo of the measured pol errors to get the error on the output params
    
    #following Muinonen et al. 2009.
    
    #if p0==None:
    #    p0={}
    #    p0['a']=5.5  #amplitude param
    #    p0['k']=0.22 #slope param
    #    p0['b']=-1  #assumed to ensure P=0 at alpha=0
    #    p0['d']=10.  #width of negative branch

    p0=[5.5,0.22,10]

    if 0 not in phase:
        #ensure the 0,0 point is fit and fixed
        go_phase=numpy.asarray(phase+[0])
        go_pol=numpy.asarray(pol+[0])
        go_err=numpy.asarray(perr+[0])
    else:
        go_phase=numpy.asarray(phase)
        go_pol=numpy.asarray(pol)
        go_err=numpy.asarray(perr)



    inv_mc=[]
    h_mc=[]
    alpha_mc=[]
    min_mc=[]
    p0_mc=[]
    p1_mc=[]
    p2_mc=[]
    
    for i in range(nmc):
        go_polerr = [random.gauss(go_pol[j],go_err[j]) for j in range(len(go_pol))]
        
        pres = sciopt.leastsq(ppdiff,p0,args=(go_phase,go_polerr),full_output=True)

        p_out=pres[0]
    
        phold=99
        inv_angle=0
        for a in numpy.arange(5,35,0.02):
            ptest=ppcurve(p_out,a)
            if abs(ptest)<phold:
                phold=abs(ptest)
                inv_angle=a
    
                
        slope=(-1*p_out[0] + p_out[1]*inv_angle + p_out[1]*p_out[2])/p_out[2] 
    
    
        alpha_min=-p_out[2]*numpy.log(p_out[1]*p_out[2]/p_out[0])

        Pmin=p_out[1]*p_out[2] * (1-numpy.log(p_out[1]*p_out[2]/p_out[0])) - p_out[0]

        inv_mc.append(inv_angle)
        h_mc.append(slope)
        alpha_mc.append(alpha_min)
        min_mc.append(Pmin)
        p0_mc.append(p_out[0])
        p1_mc.append(p_out[1])
        p2_mc.append(p_out[2])
        

    inv_mc.sort()
    h_mc.sort()
    alpha_mc.sort()
    min_mc.sort()
    p0_mc.sort()
    p1_mc.sort()
    p2_mc.sort()

    print("Parameter: Median, 16%, 84%")
    eo=med_err(inv_mc)
    print("{:s}: {:6.3f} -{:5.3f} +{:5.3f}".format("inversion",eo[0],eo[1],eo[2]))

    
    eo=med_err(h_mc)
    print("{:s}: {:6.3f} -{:5.3f} +{:5.3f}".format("h_slope",eo[0],eo[1],eo[2]))
    eo=med_err(alpha_mc)
    print("{:s}: {:6.3f} -{:5.3f} +{:5.3f}".format("alpha_min",eo[0],eo[1],eo[2]))
    eo=med_err(min_mc)
    print("{:s}: {:6.3f} -{:5.3f} +{:5.3f}".format("Pmin",eo[0],eo[1],eo[2]))
    eo=med_err(p0_mc)
    print("{:s}: {:6.3f} -{:5.3f} +{:5.3f}".format("A",eo[0],eo[1],eo[2]))
    eo=med_err(p1_mc)
    print("{:s}: {:6.3f} -{:5.3f} +{:5.3f}".format("k",eo[0],eo[1],eo[2]))
    eo=med_err(p2_mc)
    print("{:s}: {:6.3f} -{:5.3f} +{:5.3f}".format("d",eo[0],eo[1],eo[2]))
    
    return()

def med_err(inlist):
    inlist.sort()
    n=len(inlist)
    low=int(0.16*n)
    high=int(0.84*n)
    med=int(0.5*n)
    return(inlist[med],inlist[med]-inlist[low],inlist[high]-inlist[med])
          
def CurvePlot(fig_name=None,curve_param=None,phase_dat=None,pol_dat=None):

    if phase_dat is None:
        x_top=30
    else:
        x_top=max(30,max(phase_dat))

    x=numpy.arange(0,x_top,0.1)

    plt.figure()
    plt.plot(x,[0 for xx in x],'k:')

    if curve_param is not None:
        y=[ppcurve(curve_param,xx) for xx in x]
        plt.plot(x,y,'k--')
    if  phase_dat is not None and  pol_dat is not None:
        plt.plot(phase_dat,pol_dat,'rx')
        
    if fig_name is not None:
        plt.savefig(fig_name)
    else:
        plt.show()
    




def getPlane(Hname,JD,verbose=False):
    #get the expected scattering plane from Horizons
    gcontext = ssl.SSLContext() #this is needed to short-circuit an SSL verification error that pops up on Mac OSX for some reason.
    #above is from here: https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error

    
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


def get_index_of_refraction(inv_ang,dmin=1):
    #dmin is the smallest particle size, in microns
    #equation from Masiero et al. 2009

    bestn=0
    adiff=999
    for n in numpy.arange(1.5,3,0.01):
        alpha0_rad=(n*((n-1)/(n+2))**2 - (1/(2*(10*dmin)**2)) )**0.5
        alpha0=alpha0_rad*180/numpy.pi
        newdiff=abs(alpha0 - inv_ang)
        if newdiff<adiff:
            bestn=n
            adiff=newdiff

    return(bestn)
        
