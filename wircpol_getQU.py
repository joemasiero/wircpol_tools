#extract the Q,U,P,Theta spectra from all fits files.  This requires
#you to have edited the 'list' files to have columns like this:

## #path                  x   y    A/B             
## Target5/image0421.fits 704 1172 A
##

import wirc_drp.wirc_object as wo
from wirc_drp.utils import calibration, spec_utils as su
from wirc_drp.utils import source_utils
from wirc_drp.masks import *

from astropy.stats import sigma_clipped_stats
import matplotlib.pyplot as plt
import numpy as np
import astropy.io.ascii as asci
import os, copy
import time

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)



class ds9_xy(object):
    def __init__(self):
        self.x=0.
        self.y=0.
        return

#wircpol_dir = os.environ['WIRC_DRP'] # Your WIRCPOL_DRP directory (with a "/" at the end!)
#data_dir='/Users/jmasiero/WIRCPol/Observations/20230113/Data/'
data_dir='./'

obslists=os.popen("ls "+data_dir+"*_list.dat").readlines()



TEST=False  #just the first object, showing some plots
TEST2=False  #just the first 4 frames of each object, showing all plots
TEST3=False #First 20 frames of each object, showing some plots

show_plot_final=False #show to screen.  This will save regardless

if TEST2:
    do_plot=True
else:
    do_plot=False

if TEST or TEST2 or TEST3:
    do_plot_qu=True
else:
    do_plot_qu=False
    


if TEST==True:
    obslists=obslists[0:1]

    
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


    if filt=='H':
        if etime=='1s':
            def_bkg_frame=["/Users/jmasiero/WIRCPol/Pipeline/background_files/H_1s/wirc0841_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/H_1s/wirc0842_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/H_1s/wirc0843_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/H_1s/wirc0844_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/H_1s/wirc0845_cal.fits"]
        elif etime=='5s':
            def_bkg_frame=["/Users/jmasiero/WIRCPol/Pipeline/background_files/H_5s/wirc2377_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/H_5s/wirc2378_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/H_5s/wirc2379_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/H_5s/wirc2380_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/H_5s/wirc2381_cal.fits"]
        elif etime=='15s':
            def_bkg_frame=["/Users/jmasiero/WIRCPol/Pipeline/background_files/H_15s/wirc2374_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/H_15s/wirc2375_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/H_15s/wirc2376_cal.fits"]
        elif etime=='30s':
            def_bkg_frame=[
"/Users/jmasiero/WIRCPol/Pipeline/background_files/H_30s/image0384_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/H_30s/image0385_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/H_30s/image0386_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/H_30s/image0387_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/H_30s/image0388_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/H_30s/image0389_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/H_30s/image0390_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/H_30s/image0391_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/H_30s/image0392_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/H_30s/image0393_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/H_30s/image0394_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/H_30s/image0395_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/H_30s/image0396_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/H_30s/image0397_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/H_30s/image0398_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/H_30s/image0399_calib.fits"]
        else:
            def_bkg_frame='None'
    elif filt=='J':
        if etime=='1s':
            def_bkg_frame=["/Users/jmasiero/WIRCPol/Pipeline/background_files/J_1s/wirc0123_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J_1s/wirc0124_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J_1s/wirc0125_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J_1s/wirc0126_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J_1s/wirc0127_cal.fits"]
        elif etime=='5s':
            def_bkg_frame=["/Users/jmasiero/WIRCPol/Pipeline/background_files/J_5s/wirc0156_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J_5s/wirc0157_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J_5s/wirc0158_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J_5s/wirc0159_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J_5s/wirc0160_cal.fits"]
        elif etime=='15s':
            def_bkg_frame=["/Users/jmasiero/WIRCPol/Pipeline/background_files/J_15s/wirc0957_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J_15s/wirc0958_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J_15s/wirc0959_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J_15s/wirc0960_cal.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J_15s/wirc0961_cal.fits"]
        elif etime=='30s':
            def_bkg_frame=["/Users/jmasiero/WIRCPol/Pipeline/background_files/J_30s/image0400_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/J_30s/image0401_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/J_30s/image0402_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/J_30s/image0403_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/J_30s/image0404_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/J_30s/image0405_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/J_30s/image0406_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/J_30s/image0407_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/J_30s/image0408_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/J_30s/image0409_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/J_30s/image0410_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/J_30s/image0411_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/J_30s/image0412_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/J_30s/image0413_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/J_30s/image0414_calib.fits",
"/Users/jmasiero/WIRCPol/Pipeline/background_files/J_30s/image0415_calib.fits"]
        else:
            def_bkg_frame='None'

    
#    if filt=='J':
#        if etime=='1s':
#            bkg_frame=["/Users/jmasiero/WIRCPol/Pipeline/background_files/J2_1s/image1493_calib.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J2_1s/image1494_calib.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J2_1s/image1495_calib.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J2_1s/image1496_calib.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J2_1s/image1497_calib.fits"]
#        elif etime=='5s':
#            bkg_frame=["/Users/jmasiero/WIRCPol/Pipeline/background_files/J2_5s/image0825_calib.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J2_5s/image0826_calib.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J2_5s/image0827_calib.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J2_5s/image0828_calib.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J2_5s/image0829_calib.fits"]
#        elif etime=='15s':
#            bkg_frame=["/Users/jmasiero/WIRCPol/Pipeline/background_files/J2_15s/image1592_calib.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J2_15s/image1593_calib.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J2_15s/image1594_calib.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J2_15s/image1595_calib.fits","/Users/jmasiero/WIRCPol/Pipeline/background_files/J2_15s/image1596_calib.fits"]
#        else:
#            bkg_frame='None'
#    else:
#        bkg_frame='None'
    

    #calibrated_list = np.array([]) #This is a list of the calibrated files.

    #Read in the file names
    fnames  = (asci.read(inf.rstrip() , format = 'fast_no_header'))['col1']

    if TEST2:
        fnames  = (asci.read(inf.rstrip() , format = 'fast_no_header'))['col1'][0:4]
    if TEST3:
        fnames  = (asci.read(inf.rstrip() , format = 'fast_no_header'))['col1'][0:20]

    hwp_ang=np.zeros([len(fnames)])
    
    try:
        ds9_x  = (asci.read(inf.rstrip() , format = 'fast_no_header'))['col2']
        ds9_y  = (asci.read(inf.rstrip() , format = 'fast_no_header'))['col3']
        if TEST2:
            ds9_x  = (asci.read(inf.rstrip() , format = 'fast_no_header'))['col2'][0:4]
            ds9_y  = (asci.read(inf.rstrip() , format = 'fast_no_header'))['col3'][0:4]

    except KeyError:
        print("  Missing X, Y in input data list: ",inf.rstrip())
        print("\n\n^*^ ---Making baseless assumptions--- ^*^\n\n")
        time.sleep(5)
        ds9_y=np.array([1100. for i in range(len(fnames))])
        ds9_x=np.array([700 for i in range(len(fnames))])

    #add a column of 'A' or 'B' that marks which position the image is in to build the background list
    try:
        im_pos = (asci.read(inf.rstrip() , format = 'fast_no_header'))['col4']
    except KeyError:
        print("  Missing Image A/B posiiton label: ",inf.rstrip())
        print("\n\n Skipping background\n\n")
        bkg_frame='None'
    else:
        bkg_frame='Found'
        Abkg_frame=[]
        Bbkg_frame=[]
        for ii in range(len(im_pos)):
            ip=im_pos[ii]
            if ip=='A':
                Bbkg_frame.append(data_dir+fnames[ii].replace('.fits','_calib.fits'))
            elif ip=='B':
                Abkg_frame.append(data_dir+fnames[ii].replace('.fits','_calib.fits'))
            else:
                print("  Bad image A/B position for ",fnames[ii])
        print("N A_bkg: ",len(Abkg_frame)," B_bkg: ",len(Bbkg_frame))
        
    source_list = []
    all_spec_cube = []

    for i, fn in enumerate(fnames):

        print("  Extracting from file {} of {}".format(i+1, len(fnames)))
        raw_fn =data_dir+fn            
        #file name of the calibrated file
        outname = raw_fn.split('.fits')[0]+'_calib.fits'
        
        try:
            #if the calibrated file already exists, skip that part
            data = wo.wirc_data(wirc_object_filename=outname)
        except:
            print("Missing calibrated image: ",outname)
            print("Run cal script first, then rerun")
            exit()
            

        hwp_hold=data.header['HWP_ANG']

        if hwp_hold==22.5005:
            print("bad HWP angle",outname)
            hwp_hold=22.5
            
        hwp_ang[i]=hwp_hold

        #DS9_X, DS9_Y position of the zeroth order of the source (undispersed star in the center)
        #source_coords = [1340, 977] #DS9_Y, DS9_X position of the zeroth order of the source (undispersed star in the center)
        source_coords = ds9_xy()
        source_coords.x=float(ds9_x[i])
        source_coords.y=float(ds9_y[i])
        
            
        #Clear the source list
        data.source_list = []
        data.n_sources = 0
        try:

            # This function adds the source to our wirc_data object created in the last cell. 
            # update_w_chi2_shift flag centers the source
            data.add_source( source_coords.x, source_coords.y, slit_pos = "slitless",update_w_chi2_shift = True, verbose = False)
            #data.generate_bkg(method='shift_and_subtract',shift_dir='horizontal', bkg_sub_shift_size = 31)

            if bkg_frame=='None':
                data.generate_bkg(method='scaled_bkg',bkg_fns =def_bkg_frame ,bkg_by_quadrants = True, same_HWP= False)
            else:
                if im_pos[i]=='A':
                    #print(Abkg_frame)
                    data.generate_bkg(method='scaled_bkg',bkg_fns = Abkg_frame ,bkg_by_quadrants = True, same_HWP= False)
                elif im_pos[i]=='B':
                    #print(Bbkg_frame)
                    data.generate_bkg(method='scaled_bkg',bkg_fns = Bbkg_frame ,bkg_by_quadrants = True, same_HWP= False)
                else:
                    data.generate_bkg(method='scaled_bkg',bkg_fns = def_bkg_frame ,bkg_by_quadrants = True, same_HWP= False)


            #Get cutouts of the 4 spectra and plot them for every 10 frames
            data.source_list[0].get_cutouts(data.full_image, data.DQ_image, data.filter_name, data.bkg_image, replace_bad_pixels = True, sub_bar = False, method='median', cutout_size = 75)
            
            if do_plot:
                data.source_list[0].plot_cutouts(figsize=(10,6))
                plt.show()
                data.source_list[0].plot_cutouts(figsize=(10,6),plot_dq=True)
                plt.show()
                plt.close()
        except Exception as e:
            print("  --> Error in source extraction, skipping file {}".format(fn))
            print("  --> Error {}".format(e))
            continue

        try:
            #Now extract the spectra
            
            data.source_list[0].generate_cutout_backgrounds(update=True, mask_diag = False)
            data.source_list[0].extract_spectra(method="optimal_extraction", spatial_sigma=3, bad_pix_masking =1,plot_optimal_extraction = False, plot_findTrace = do_plot, verbose=False,trace_angle = [-44.8, -46.3, -43.7, -44.6])

            #try fixed_width instead of spatial sigma for extract spectra, 7 (pixels off center line)  10-12 for bad seeing
            
            #Save the spectra in this array
            all_spec_cube.append(data.source_list[0].trace_spectra)

            if do_plot:
                data.source_list[0].plot_trace_spectra(figsize=(10,6),filter_name=filt,xlow=0,xhigh=150)
                plt.show()
                plt.close()

            source_list += [data.source_list[0]]
                
            ##this isn't working; picking up some noisy points and mis-calibrating
            ##wait until after combining before doing wave cal
            #
            #if do_plot:
            #    data.source_list[0].rough_lambda_calibration(method=2,filter_name=filt)
            #    data.source_list[0].plot_trace_spectra(figsize=(10,6),filter_name=filt)
            #    plt.show()
            
            #Save the file
            data.save_wirc_object(outname)
            
        except Exception as e:
            print("  --> Error in spectral extraction, skipping file {}".format(fn))
            print("  --> Error {}".format(e))
            continue


    source_list = copy.deepcopy(source_list)
    target_all_spec_cube = np.array(all_spec_cube)

    align_vec = target_all_spec_cube[0,0,1,:]
    target_aligned_cube = su.align_spectral_cube(np.nan_to_num(target_all_spec_cube[:,:,:,:]), ref_trace = align_vec)

    #replaced by above 
    #target_aligned_cube = su.align_spectral_cube(target_all_spec_cube)

    #no longed needed
    #target_scaled_cube = su.scale_and_combine_spectra(target_aligned_cube, return_scaled_cube = True)
    #structure of above: t_s_c[list of images][traces 0-3][wave,flux,err]

    #median combine the 4 traces before doing wave cal
    #wl_rough=[]
    flux_spec=[]
    for jj in range(4):
        #fs=np.median(target_scaled_cube[:,jj,1], axis = 0)
        fs=np.median(target_aligned_cube[:,jj,1], axis = 0)
        fs=fs/np.max(fs)
        flux_spec.append(fs)
    med_spec=np.median(flux_spec,axis=0)
    wl_Sol = su.rough_wavelength_calibration_v2(med_spec, filter_name = filt)

    #paste the wavelength solutions into the target cube
    #for kk in range(len(target_scaled_cube)):
    for kk in range(len(target_aligned_cube)):
        for jj in range(4):
            #target_scaled_cube[kk][jj][0]=wl_Sol
            target_aligned_cube[kk][jj][0]=wl_Sol


    #np.save(data_dir+obj+'_'+filt+'_specCube.npy', target_scaled_cube)
    np.save(data_dir+obj+'_'+filt+'_specCube.npy', target_aligned_cube)
    np.save(data_dir+obj+'_'+filt+'_hwp.npy', hwp_ang)
    
    
    #get pol

    try:
        #q,u,q_err,u_err,q_ind,u_ind = source_utils.compute_qu_for_obs_sequence(target_scaled_cube,np.array(hwp_ang),run_alignment=True,method='flux_ratio')
        q,u,q_err,u_err,q_ind,u_ind = source_utils.compute_qu_for_obs_sequence(target_aligned_cube,np.array(hwp_ang),run_alignment=False)

        p = np.sqrt(q**2+u**2)
        theta = 0.5*np.degrees(np.arctan2(u,q))
        theta[theta<0] += 180

        q_ind0 = q[q_ind==0]
        q_ind1 = q[q_ind==1]
        u_ind0 = u[u_ind==0]
        u_ind1 = u[u_ind==1]

        P0q_sc,P0q_sc_med,P0q_sc_std = sigma_clipped_stats(q_ind0, sigma = 3, maxiters = 5, axis = 0)
        P0u_sc,P0u_sc_med,P0u_sc_std = sigma_clipped_stats(u_ind0, sigma = 3, maxiters = 5, axis = 0)
        P1q_sc,P1q_sc_med,P1q_sc_std = sigma_clipped_stats(q_ind1, sigma = 3, maxiters = 5, axis = 0)
        P1u_sc,P1u_sc_med,P1u_sc_std = sigma_clipped_stats(u_ind1, sigma = 3, maxiters = 5, axis = 0)

        if filt in ['J','H']:        
            cal_q0,cal_u0,cal_q_err0,cal_u_err0 = calibration.calibrate_qu(wl_Sol, P0q_sc, P0u_sc,P0q_sc_std/np.sqrt(len(q_ind0)), P0u_sc_std/np.sqrt(len(u_ind0)), trace_pair=0, filter_name = filt)
            cal_q1,cal_u1,cal_q_err1,cal_u_err1 = calibration.calibrate_qu(wl_Sol, P1q_sc, P1u_sc,P1q_sc_std/np.sqrt(len(q_ind1)), P1u_sc_std/np.sqrt(len(u_ind1)), trace_pair=1, filter_name = filt)
        else:
            cal_q0=P0q_sc
            cal_q1=P1q_sc
            cal_u0=P0u_sc
            cal_u1=P1u_sc
            cal_q_err0=P0q_sc_std
            cal_q_err1=P1q_sc_std
            cal_u_err0=P0u_sc_std
            cal_u_err1=P1u_sc_std
            
            
        if do_plot_qu:
            fig, ax = plt.subplots(1,2,figsize = (10,6))
    
            ax[0].errorbar(range(len(P0q_sc)), P0q_sc*100, yerr = P0q_sc_std*100/np.sqrt(len(q_ind0)), color ='b', alpha = 0.5)
            ax[1].errorbar(range(len(P0u_sc)), -P0u_sc*100, yerr = P0u_sc_std*100/np.sqrt(len(u_ind0)), color ='b', alpha = 0.5)
            ax[0].errorbar(range(len(P1q_sc)), P1q_sc*100, yerr = P1q_sc_std*100/np.sqrt(len(q_ind1)), color ='r', alpha = 0.5)
            ax[1].errorbar(range(len(P1u_sc)), -P1u_sc*100, yerr = P1u_sc_std*100/np.sqrt(len(u_ind1)), color ='r', alpha = 0.5)

            ax[0].errorbar(range(len(P0q_sc)), cal_q0*100, yerr = cal_q_err0, color ='b', alpha = 1)
            ax[1].errorbar(range(len(P0u_sc)), cal_u0*100, yerr = cal_u_err0, color ='b', alpha = 1)
            ax[0].errorbar(range(len(P1q_sc)), cal_q1*100, yerr = cal_q_err1, color ='r', alpha = 1)
            ax[1].errorbar(range(len(P1u_sc)), cal_u1*100, yerr = cal_u_err1, color ='r', alpha = 1)
    
            ax[0].set_ylim([-6,6])
            ax[1].set_ylim([-6,6])
            ax[0].set_xlim([40,120])
            ax[1].set_xlim([40,120])
            plt.show()
            plt.close()

        #now smooth spectra
        bs=5
        smooth_q = su.smooth_spectra(q, kernel = 'box', smooth_size=bs, rebin = True)
        smooth_u = su.smooth_spectra(u, kernel = 'box', smooth_size=bs, rebin = True)
        q_sc_sm,q_sc_med_sm,q_sc_std_sm = sigma_clipped_stats(smooth_q, sigma = 3, maxiters = 5, axis = 0)
        u_sc_sm,u_sc_med_sm,u_sc_std_sm = sigma_clipped_stats(smooth_u, sigma = 3, maxiters = 5, axis = 0)
        wlSol_smooth = su.smooth_spectra(wl_Sol, kernel = 'box', smooth_size = bs, rebin = True)
        q_sm_ind0 = smooth_q[q_ind == 0]
        q_sm_ind1 = smooth_q[q_ind == 1]
        u_sm_ind0 = smooth_u[u_ind == 0]
        u_sm_ind1 = smooth_u[u_ind == 1]
        P0q_sc_sm,P0q_sc_med_sm,P0q_sc_std_sm = sigma_clipped_stats(q_sm_ind0, sigma = 5, maxiters = 20, axis = 0)
        P0u_sc_sm,P0u_sc_med_sm,P0u_sc_std_sm = sigma_clipped_stats(u_sm_ind0, sigma = 5, maxiters = 20, axis = 0)
        P1q_sc_sm,P1q_sc_med_sm,P1q_sc_std_sm = sigma_clipped_stats(q_sm_ind1, sigma = 5, maxiters = 20, axis = 0)
        P1u_sc_sm,P1u_sc_med_sm,P1u_sc_std_sm = sigma_clipped_stats(u_sm_ind1, sigma = 5, maxiters = 20, axis = 0)


        if filt in ['J','H']:        
            cal_q0_sm,cal_u0_sm,cal_q_err0_sm,cal_u_err0_sm = calibration.calibrate_qu(wlSol_smooth, P0q_sc_sm, P0u_sc_sm,P0q_sc_std_sm/np.sqrt(len(q_sm_ind0)), P0u_sc_std_sm/np.sqrt(len(u_sm_ind0)), trace_pair=0, filter_name = filt)
            cal_q1_sm,cal_u1_sm,cal_q_err1_sm,cal_u_err1_sm = calibration.calibrate_qu(wlSol_smooth, P1q_sc_sm, P1u_sc_sm,P1q_sc_std_sm/np.sqrt(len(q_sm_ind1)), P1u_sc_std_sm/np.sqrt(len(u_sm_ind1)), trace_pair=1, filter_name = filt)
        else:
            print("-----Couldn't find band, skipping calibration----")
            cal_q0_sm=P0q_sc_sm
            cal_q1_sm=P1q_sc_sm
            cal_u0_sm=P0u_sc_sm
            cal_u1_sm=P1u_sc_sm
            cal_q_err0_sm=P0q_sc_std_sm
            cal_q_err1_sm=P1q_sc_std_sm
            cal_u_err0_sm=P0u_sc_std_sm
            cal_u_err1_sm=P1u_sc_std_sm


        
        if do_plot_qu:
            fig, ax = plt.subplots(1,2,figsize = (10,6))

            for i in range(len(q_sm_ind0)):
                ax[0].plot(q_sm_ind0[i]*100, 'b', alpha = 0.1)
                ax[1].plot(u_sm_ind0[i]*100, 'b', alpha = 0.1)
            for i in range(len(q_sm_ind1)):
                ax[0].plot(q_sm_ind1[i]*100, 'r', alpha = 0.1)
                ax[1].plot(u_sm_ind1[i]*100, 'r', alpha = 0.1)
    
            ax[0].errorbar(range(len(P0q_sc_sm)), P0q_sc_sm*100, yerr = P0q_sc_std_sm*100/np.sqrt(len(q_sm_ind0)), color ='b', alpha = 0.5)
            ax[1].errorbar(range(len(P0u_sc_sm)), P0u_sc_sm*100, yerr = P0u_sc_std_sm*100/np.sqrt(len(u_sm_ind0)), color ='b', alpha = 0.5)
            ax[0].errorbar(range(len(P1q_sc_sm)), P1q_sc_sm*100, yerr = P1q_sc_std_sm*100/np.sqrt(len(q_sm_ind1)), color ='r', alpha = 0.5)
            ax[1].errorbar(range(len(P1u_sc_sm)), P1u_sc_sm*100, yerr = P1u_sc_std_sm*100/np.sqrt(len(u_sm_ind1)), color ='r', alpha = 0.5)

            ax[0].errorbar(range(len(P0q_sc_sm)), cal_q0_sm*100, yerr = cal_q_err0_sm*100, color ='b', alpha = 1)
            ax[1].errorbar(range(len(P0u_sc_sm)), cal_u0_sm*100, yerr = cal_u_err0_sm*100, color ='b', alpha = 1)
            ax[0].errorbar(range(len(P1q_sc_sm)), cal_q1_sm*100, yerr = cal_q_err1_sm*100, color ='r', alpha = 1)
            ax[1].errorbar(range(len(P1u_sc_sm)), cal_u1_sm*100, yerr = cal_u_err1_sm*100, color ='r', alpha = 1)

            ax[0].set_ylim([-10,10])
            ax[1].set_ylim([-10,10])
            ax[0].set_xlim([40//5,120//5])
            ax[1].set_xlim([40//5,120//5])
            plt.show()
            plt.close()

        
        cal_q_sm = np.mean([cal_q0_sm, cal_q1_sm], axis = 0)
        cal_u_sm = np.mean([cal_u0_sm, cal_u1_sm], axis = 0)

        cal_q_err_sm = np.sqrt(cal_q_err0_sm**2 + cal_q_err1_sm**2)/2.
        cal_u_err_sm = np.sqrt(cal_u_err0_sm**2 + cal_u_err1_sm**2)/2.

        
        #print(cal_q_sm, cal_u_sm ,cal_q_err_sm, cal_u_err_sm)
        cal_p, p_corr, cal_p_err, theta, theta_err = source_utils.compute_p_and_pa(cal_q_sm, cal_u_sm ,cal_q_err_sm, cal_u_err_sm)

        
        #cal_p = np.sqrt(cal_q_sm**2+cal_u_sm**2)
        #cal_p_err = np.sqrt((cal_q_sm/cal_p)**2 * cal_q_err_sm**2 + (cal_u_sm/cal_p)**2 * cal_u_err_sm**2)

        
        #cal_theta = 0.5*np.degrees(np.arctan2(cal_u_sm,cal_q_sm))
        #
        #t_err=[]
        #for t in range(len(cal_theta)):
        #    test_t=np.zeros(4)
        #    test_t[0]=0.5*np.degrees(np.arctan2(cal_u_sm[t]+cal_u_err_sm[t],cal_q_sm[t]+cal_q_err_sm[t]))
        #    test_t[1]=0.5*np.degrees(np.arctan2(cal_u_sm[t]+cal_u_err_sm[t],cal_q_sm[t]-cal_q_err_sm[t]))
        #    test_t[2]=0.5*np.degrees(np.arctan2(cal_u_sm[t]-cal_u_err_sm[t],cal_q_sm[t]+cal_q_err_sm[t]))
        #    test_t[3]=0.5*np.degrees(np.arctan2(cal_u_sm[t]-cal_u_err_sm[t],cal_q_sm[t]-cal_q_err_sm[t]))
        #
        #    t_err.append((max(test_t)-min(test_t))/2.)
            
        theta[theta<0] = theta[theta<0]+np.pi
        cal_theta=np.degrees(theta)
        cal_theta_err=np.degrees(theta_err)

        #polout=np.array([wl_Sol,q_median,u_median,p_median,theta_median])
        polout=np.array([wlSol_smooth,cal_q_sm,cal_q_err_sm,cal_u_sm,cal_u_err_sm,cal_p,cal_p_err,cal_theta,cal_theta_err])
        np.save(data_dir+obj+'_'+filt+'_pol.npy', polout)



    except Exception as e:
        print("Error in Q/U calculation, skipping file {}".format(inf))
        print("Error {}".format(e))
        print(cal_q0_sm)
        print(cal_q1_sm)
        print(cal_u0_sm)
        print(cal_u1_sm)
        print(cal_q_err0_sm)
        print(cal_q_err1_sm)
        print(cal_u_err0_sm)
        print(cal_u_err1_sm)
        print(cal_q_sm)
        print(cal_u_sm)
        print(cal_q_err_sm)
        print(cal_u_err_sm)
        exit()
        #continue

    try:
        
        fig,axes = plt.subplots(2,2,figsize=(15,8))
        n_q = cal_q_sm.shape[0]

        axes[0,0].errorbar(wlSol_smooth, cal_q_sm*100, cal_q_err_sm*100, marker = 's', ls = 'None')
        axes[0,0].plot([0,5],[0,0], marker=None, ls = 'dotted', color='black')
        axes[0,1].errorbar(wlSol_smooth, cal_u_sm*100, cal_u_err_sm*100, marker = 's', ls = 'None')
        axes[0,1].plot([0,5],[0,0], marker=None, ls = 'dotted', color='black')
        axes[1,0].errorbar(wlSol_smooth, cal_p*100, cal_p_err*100, marker = 's', ls = 'None')
        axes[1,1].errorbar(wlSol_smooth, cal_theta, cal_theta_err, marker = 's', ls = 'None')

        maxp=0
        if filt=='H':
            axes[0,0].set_xlim(1.51,1.85)
            axes[0,1].set_xlim(1.51,1.85)
            axes[1,0].set_xlim(1.51,1.85)
            axes[1,1].set_xlim(1.51,1.85)
            for w in range(len(wlSol_smooth)):
                if wlSol_smooth[w]>=1.5 and wlSol_smooth[w]<=1.78:
                    if abs(cal_p[w]*100)>maxp:
                        maxp=abs(cal_p[w]*100)
                        
        elif filt=='J':
            axes[0,0].set_xlim(1.155,1.33)
            axes[0,1].set_xlim(1.155,1.33)
            axes[1,0].set_xlim(1.155,1.33)
            axes[1,1].set_xlim(1.155,1.33)
            for w in range(len(wlSol_smooth)):
                if wlSol_smooth[w]>=1.15 and wlSol_smooth[w]<=1.35:
                    if abs(cal_p[w]*100)>maxp:
                        maxp=abs(cal_p[w]*100)
                        
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
    
        if show_plot_final:
            plt.show()
        
        plt.close()
        

    except Exception as e:
        print("Error in plotting, skipping file {}".format(inf))
        print("Error {}".format(e))
        continue
