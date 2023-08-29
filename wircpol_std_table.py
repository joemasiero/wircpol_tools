#This code goes through the data after reduction is complete
#(wircpol_cal and wircpol_getQU) and pulls out the final values for
#standard stars, in a LaTex format suitable for dropping into a paper.

from wirc_drp.utils import source_utils
import numpy as np
import os


#wircpol_dir = os.environ['WIRC_DRP'] # Your WIRCPOL_DRP directory (with a "/" at the end!)
data_dir='./'

date_obs=data_dir.split('/')[5]

do_plot=False

do_plot_qu=False
    
do_plot_final=False

obslists=os.popen("ls "+data_dir+"HD*_list.dat").readlines()

    
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

        
    maxp=0
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

        if cal_q_err_sm[ii]<0.0001:
            cal_q_err_sm[ii]=0.0001
        if cal_u_err_sm[ii]<0.0001:
            cal_u_err_sm[ii]=0.0001

        wq=1/cal_q_err_sm[ii]**2
        sqhold+=(cal_q_sm[ii] * wq)
        wqhold+=wq
        wu=1/cal_u_err_sm[ii]**2
        suhold+=(cal_u_sm[ii] * wu)
        wuhold+=wu

    wqmean=sqhold/wqhold
    wqerr=np.sqrt(1/wqhold)
    wumean=suhold/wuhold
    wuerr=np.sqrt(1/wuhold)


    p, p_corr, p_err, theta, theta_err = source_utils.compute_p_and_pa(wqmean, wumean ,wqerr, wuerr)

    theta_deg=np.degrees(theta)
    theta_err_deg=np.degrees(theta_err)

    if theta_deg<0:
        theta_deg+=180
    

    oline="{name:9s} & {y:4d}-{m:02d}-{d:02d} & 00:00 & {filt:1s} & $0.00\pm0.00\%$ & $000.00\pm0$ & ${pol:5.3f}\pm{perr:5.3f}\%$ & ${theta:6.2f}\pm{terr:6.2f}$\\\\ ".format(name=obj,y=int(date_obs[0:4]),m=int(date_obs[4:6]),d=int(date_obs[6:8])+1,filt=filt,pol=p*100,perr=p_err*100,theta=theta_deg,terr=theta_err_deg)
    print(oline)
    
    
