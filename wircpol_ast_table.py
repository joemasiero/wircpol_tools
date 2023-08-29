#Make a latex table suitable for a paper of all asteroids in the Data
#directory

from wirc_drp.utils import source_utils
import numpy as np
import os

import urllib.request
import ssl
gcontext = ssl.SSLContext() #this is needed to short-circuit an SSL verification error that pops up on Mac OSX for some reason.
#above is from here: https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
import nss


def getPlane(Hname,JD,verbose=False):
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
    ang_prime=90+ang
    if ang_prime>180:
        ang_prime-=180
    #negative and positive pol angles
    return(ang,ang_prime)



#correction to the final theta angle based on the Polgt1 asteroid observations in Results/
theta_corr={}
theta_corr['J']=7.8
theta_corr['H']=7.8

#wircpol_dir = os.environ['WIRC_DRP'] # Your WIRCPOL_DRP directory (with a "/" at the end!)
data_dir='./Data/'

date_obs=os.popen('pwd').readline().strip().split('/')[5]

do_plot=False

do_plot_qu=False
    
do_plot_final=False

obslists=os.popen("ls "+data_dir+"[aAn]*_list.dat").readlines()

oline="Asteroid & Observation Date & UT & Filter & $P_r$ & $\\theta$ (E-of-N) & $\\theta_{scattering plane}\\\\ "
print(oline)

    
for inf in obslists:
    list_fn=inf.rstrip().split('/')[-1]

    #this assumes a standardized file name for the object lists of (name)_(filt)_(PG)_(etime)_list.dat
    params=list_fn.split('_')
    obj=params[0]

    if obj in ['flat','sky','dark']:
        continue
    #print("*** Working on "+obj)
    
    filt=params[1]
    etime=params[-2]

    
    polout=np.load(data_dir+obj+'_'+filt+'_pol.npy')

    wlSol_smooth=polout[0]
    cal_q_sm=polout[1]
    cal_q_err_sm=polout[2]
    cal_u_sm=polout[3]
    cal_u_err_sm=polout[4]
    cal_p=polout[5]
    cal_p_err=polout[6]
    cal_theta=polout[7]
    cal_theta_err=polout[8]

    if filt=='H':
        wavemin=1.52
        wavemax=1.78
        
    elif filt=='J':
        wavemin=1.155
        wavemax=1.33

    sqhold=0
    wqhold=0
    suhold=0
    wuhold=0
    for ii in range(len(cal_q_sm)):
        if wlSol_smooth[ii]<wavemin or wlSol_smooth[ii]>wavemax:
            continue

        if cal_q_err_sm[ii]<0.001:
            cal_q_err_sm[ii]=0.001
        if cal_u_err_sm[ii]<0.001:
            cal_u_err_sm[ii]=0.001

        wq=1/cal_q_err_sm[ii]**2
        sqhold+=(cal_q_sm[ii] * wq)
        wqhold+=wq
        wu=1/cal_u_err_sm[ii]**2
        suhold+=(cal_u_sm[ii] * wu)
        wuhold+=wu

    wqmean=sqhold/wqhold
    wqerr=np.sqrt(1/wqhold + 0.001**2)
    wumean=suhold/wuhold
    wuerr=np.sqrt(1/wuhold + 0.001**2)

    p, p_corr, p_err, theta, theta_err = source_utils.compute_p_and_pa(wqmean, wumean ,wqerr, wuerr)

    theta_deg=np.degrees(theta) + theta_corr[filt]
    theta_err_deg=np.degrees(theta_err)

    if theta_deg<0:
        theta_deg+=180
    if theta_deg>180:
        theta_deg-=180

    if obj[0]=='a' or obj[0]=='A':
        n=obj[1:]
    elif obj[0:3]=='neo':
        n=obj[3:]
    else:
        continue

    ymd='{y:4d} {m:02d} {d:02d}.0'.format(y=int(date_obs[0:4]),m=int(date_obs[4:6]),d=int(date_obs[6:8])+1)
    (n_ast_plane,p_ast_plane)=getPlane(n,nss.Time(ymd,'ymd').jd)
    diff=abs(n_ast_plane-theta_deg)
    if diff<45 or diff>135:
        pout=p*-100
    else:
        pout=p*100

    errout=p_err*100
        
    oline="{name:9s} & {y:4d}-{m:02d}-{d:02d} & 00:00 & {filt:1s} & ${pol:+4.2f} \pm {perr:4.2f}\%$ & ${theta:5.1f} \pm {terr:5.1f}$ & ${theta_s:5.1f}$\\\\ ".format(name=obj,y=int(date_obs[0:4]),m=int(date_obs[4:6]),d=int(date_obs[6:8])+1,filt=filt,pol=pout,perr=errout,theta=theta_deg,terr=theta_err_deg,theta_s=n_ast_plane)
    print(oline)
    
