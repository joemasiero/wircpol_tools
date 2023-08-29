#after data reduction is complete (wircpol_getQU) this will replot the
#output specpol figs with the expected P and Theta as given in the
#'expected' dictionary


from wirc_drp.utils import source_utils
import matplotlib.pyplot as plt
import numpy as np
import os


#wircpol_dir = os.environ['WIRC_DRP'] # Your WIRCPOL_DRP directory (with a "/" at the end!)
#data_dir='/Users/jmasiero/WIRCPol/Observations/20230113/Data/'
data_dir='./'

do_plot=False

do_plot_qu=False
    
do_plot_final=False

obslists=os.popen("ls "+data_dir+"*_list.dat").readlines()


#make list here of object, pJ, PH, angle, range
expected={'Ceres':(0.4,0.4,20,1.5),
          'Ivar':(3,2.5,20,8),
          'neo154244':(4,3.5,41,6),
          'a20':(0.4,0.4,96,1.5),
          'a393':(0.01,0.01,139,1), #neg=139
          'a234':(1.6,1.5,173,2),
          'a402':(0.6,0.8,73,2),
          'a10':(1.4,1.4,63,2),
          'a433':(0.5,0.5,62,1.5),
          'a51':(0.5,0.5,63,1.5),
          'a88':(0.4,0.4,153,1.5),
          'a233':(0.5,0.5,62,1.5), #neg=62
          'a41':(0.4,0.4,67,1.5),
          'a140':(1.5,1.5,159,1.6),
          'a704':(0.4,0.4,179,1.5), #pos=179
}
    
for inf in obslists:
    list_fn=inf.rstrip().split('/')[-1]

    #this assumes a standardized file name for the object lists of (name)_(filt)_(PG)_(etime)_list.dat
    params=list_fn.split('_')
    obj=params[0]

    if obj in ['flat','sky','dark']:
        continue
    print("*** Working on "+obj)
    
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

        
    fig,axes = plt.subplots(2,2,figsize=(15,8))
    n_q = cal_q_sm.shape[0]
        #n_q = q.shape[0]
        #q_mean = np.nanmean(q[:,:],axis=(0))
        #u_mean = np.nanmean(u[:,:],axis=(0))
        #q_mean_err = np.sqrt(np.nanmean(q_err))
        #p_mean = np.sqrt(q_mean**2+u_mean**2)
        #theta_mean = 0.5*np.degrees(np.arctan2(u_mean,q_mean))
        #theta_mean[theta_mean<0] += 180
        #q_median = np.nanmedian(q[:,:],axis=(0))
        #u_median = np.nanmedian(u[:,:],axis=(0))
        #p_median = np.sqrt(q_median**2+u_median**2)
        #theta_median = 0.5*np.degrees(np.arctan2(u_median,q_median))
        #theta_median[theta_median<0] += 180
        #for i in range(n_q):
        #    #Plot Q
        #    axes[0,0].plot(wl_Sol,q[i,:], 'C0', alpha=2/n_q)
        #    #Plot U
        #    axes[0,1].plot(wl_Sol,u[i,:], 'C1', alpha=2/n_q)
        #    #Plot p
        #    axes[1,0].plot(wl_Sol,p[i,:], 'C2', alpha=2/n_q)
        #    #Plot theta
        #    axes[1,1].plot(wl_Sol,theta[i,:], 'C3', alpha=2/n_q)
        #
        #axes[0,0].plot(wl_Sol,q_mean,'k',label="Mean")    
        #axes[0,1].plot(wl_Sol,u_mean,'k',label="Mean")   
        #axes[1,0].plot(wl_Sol,p_mean,'k',label="Mean")
        #axes[1,1].plot(wl_Sol,theta_mean,'k', label='Mean')
        #axes[0,0].plot(wl_Sol,q_median,'k--',label="Median")    
        #axes[0,1].plot(wl_Sol,u_median,'k--',label="Median")    
        #axes[1,0].plot(wl_Sol,p_median,'k--',label="Median")    
        #axes[1,1].plot(wl_Sol,theta_median,'k--',label="Median")



    axes[0,0].errorbar(wlSol_smooth, cal_q_sm*100, cal_q_err_sm*100, marker = 's', ls = 'None')
    axes[0,0].plot([0,5],[0,0], marker=None, ls = 'dotted', color='black')
    axes[0,1].errorbar(wlSol_smooth, cal_u_sm*100, cal_u_err_sm*100, marker = 's', ls = 'None')
    axes[0,1].plot([0,5],[0,0], marker=None, ls = 'dotted', color='black')
    axes[1,0].errorbar(wlSol_smooth, cal_p*100, cal_p_err*100, marker = 's', ls = 'None')
    axes[1,1].errorbar(wlSol_smooth, cal_theta, cal_theta_err, marker = 's', ls = 'None')

    maxp=0.5
    if filt=='H':
        wavemin=1.52
        wavemax=1.78
        
    elif filt=='J':
        wavemin=1.155
        wavemax=1.33
        

    axes[0,0].set_xlim(wavemin,wavemax)
    axes[0,1].set_xlim(wavemin,wavemax)
    axes[1,0].set_xlim(wavemin,wavemax)
    axes[1,1].set_xlim(wavemin,wavemax)
    for w in range(len(wlSol_smooth)):
        if wlSol_smooth[w]>=wavemin and wlSol_smooth[w]<=wavemax:
            if abs(cal_p[w]*100)>maxp:
                maxp=abs(cal_p[w]*100)

    #for stars, Jpol~0.461 Vpol and Hpol~0.250 Vpol


    if obj in expected:
        if filt=='J':
            axes[1,0].errorbar(wlSol_smooth, [expected[obj][0] for p in cal_p], cal_p_err*0, marker = 'None', ls = 'dashed')
            axes[1,1].errorbar(wlSol_smooth, [expected[obj][2] for t in cal_theta], cal_theta_err*0, marker = 'None', ls = 'dashed')
            maxp=expected[obj][3]
        elif filt=='H':
            axes[1,0].errorbar(wlSol_smooth, [expected[obj][1] for p in cal_p], cal_p_err*0, marker = 'None', ls = 'dashed')
            axes[1,1].errorbar(wlSol_smooth, [expected[obj][2] for t in cal_theta], cal_theta_err*0, marker = 'None', ls = 'dashed')
            maxp=expected[obj][3]

        
            
    axes[0,0].set_ylim(-maxp,maxp)
    axes[0,1].set_ylim(-maxp,maxp)
    axes[1,0].set_ylim(0,maxp)
    axes[1,1].set_ylim(0,180)
    axes[0,0].set_ylabel("q",fontsize=18)
    axes[0,1].set_ylabel("u",fontsize=18)
    axes[1,0].set_ylabel("p",fontsize=18)
    axes[1,1].set_ylabel("theta",fontsize=18)
    axes[0,0].set_xlabel(r"Wavelength [$\mu m$]",fontsize=18)
    axes[0,1].set_xlabel(r"Wavelength [$\mu m$]",fontsize=18)
    axes[1,0].set_xlabel(r"Wavelength [$\mu m$]",fontsize=18)
    axes[1,1].set_xlabel(r"Wavelength [$\mu m$]",fontsize=18)


    
    pout=list_fn.replace('_list.dat','.png')
    fig.savefig(pout)
    
    if do_plot_final:
        plt.show()
    
    plt.close()



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

    if wqhold==0 or wuhold==0:
        continue
    wqmean=sqhold/wqhold
    wqerr=np.sqrt(1/wqhold)
    wumean=suhold/wuhold
    wuerr=np.sqrt(1/wuhold)

    p, p_corr, p_err, theta, theta_err = source_utils.compute_p_and_pa(np.asarray([wqmean]), np.asarray([wumean]) ,np.asarray([wqerr]), np.asarray([wuerr]))

    theta_deg=np.degrees(theta[0])
    theta_err_deg=np.degrees(theta_err[0])

    if theta_deg<0:
        theta_deg+=180
    
    oline="Error-weighted pol across band {filt:s} for {name:s}: {p:4.2f}+/-{e:4.2f}%  Theta: {theta:5.1f}+/-{terr:4.1f} deg".format(name=obj,filt=filt,p=p[0]*100,e=p_err[0]*100,theta=theta_deg,terr=theta_err_deg)
    print(oline)    
    
