#portion of the full reduction script that just does the flat/dark
#corrections and spits out claibrated fits frames

import wirc_drp.wirc_object as wo
from wirc_drp.utils import calibration
from wirc_drp.masks import *

import astropy.io.ascii as asci
import os

#wircpol_dir = os.environ['WIRC_DRP'] # Your WIRCPOL_DRP directory (with a "/" at the end!)
data_dir='./'

### Get the file list 
os.chdir(data_dir)
dark_list1s_fn = "dark_1s_list.dat" #The file name for your list of dark files
dark_list1s = (asci.read(dark_list1s_fn, format = 'fast_no_header'))['col1'] #Read in the list

dark_list5s_fn = "dark_5s_list.dat" #The file name for your list of dark files
dark_list5s = (asci.read(dark_list5s_fn, format = 'fast_no_header'))['col1'] #Read in the list

dark_list30s_fn = "dark_30s_list.dat" #The file name for your list of dark files
dark_list30s = (asci.read(dark_list30s_fn, format = 'fast_no_header'))['col1'] #Read in the list



### Create the master dark and a bad pixel map.
### This function creates a new fits file based on the last filename in your dark_list and appends "_master_dark.fits"
### The hot pixel map will be the same, except with a "_bp_map.fits" suffix. 
dark_name1s, bp_name_1 = calibration.masterDark(dark_list1s) # The output of this function is the filename 
                                                         # of the master dark and bad pixel maps

dark_name5s, bp_name_5 = calibration.masterDark(dark_list5s) # The output of this function is the filename 
                                                         # of the master dark and bad pixel maps
dark_name30s, bp_name_30 = calibration.masterDark(dark_list30s) # The output of this function is the filename 
                                                         # of the master dark and bad pixel maps


### Get the file list 

flat_H_PG_list_fname = "flat_H_PG_list.dat" #The file name for your list of flat files
flat_H_PG_list = (asci.read(flat_H_PG_list_fname, format = 'fast_no_header'))['col1']
flat_J_PG_list_fname = "flat_J_PG_list.dat" #The file name for your list of flat files
flat_J_PG_list = (asci.read(flat_J_PG_list_fname, format = 'fast_no_header'))['col1']

### Create the master dark and a bad pixel map. You will need the filename 
### This function creates a new fits file based on the last filename in your flat list and appends "_master_flat.fits"

#flat_H_name, bp_H_name = calibration.masterFlat(flat_H_list, dark_name1s, hotp_map_fname = None) 
#flat_J_name, bp_J_name = calibration.masterFlat(flat_J_list, dark_name1s, hotp_map_fname = None) 

#  ^*^
#need the min_flux=100 here or else all the frames get dropped because the mean flux wasn't >1000 per pix
flat_J_PG_name, bp_J_PG_name = calibration.masterFlat(flat_J_PG_list, dark_name5s, hotp_map_fname = None,min_flux=100) 
flat_H_PG_name, bp_H_PG_name = calibration.masterFlat(flat_H_PG_list, dark_name5s, hotp_map_fname = None,min_flux=100)


#loop here

TEST=False
TEST2=False
do_plot = False

obslists=os.popen("ls "+data_dir+"*_list.dat").readlines()

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
    if params[2]=='PG':
        if filt=='H':
            flat_fn = data_dir+flat_H_PG_name
            bp_fn = data_dir+bp_H_PG_name
        elif filt=='J':
            flat_fn = data_dir+flat_J_PG_name
            bp_fn = data_dir+bp_J_PG_name
        else:
            print("\n\nFailure, bad filter in file: ",list_fn)
            exit()
    else:
        if filt=='H':
            flat_fn = data_dir+flat_H_name
            bp_fn = data_dir+bp_H_name
        elif filt=='J':
            flat_fn = data_dir+flat_J_name
            bp_fn = data_dir+bp_J_name
        else:
            print("\n\nFailure, bad filter in file: ",list_fn)
            exit()
    if etime=="1s":            
        dark_fn = data_dir+dark_name1s
    elif etime=="5s":            
        dark_fn = data_dir+dark_name5s
    elif etime=="15s":            
        dark_fn = data_dir+dark_name15s
    elif etime=="30s":            
        dark_fn = data_dir+dark_name30s
    else:
        print("\n\nFailure, bad time in file: ",list_fn)
        exit()


    #calibrated_list = np.array([]) #This is a list of the calibrated files.

    #Read in the file names
    fnames  = (asci.read(inf.rstrip() , format = 'fast_no_header'))['col1']

    if TEST2:
        fnames  = (asci.read(inf.rstrip() , format = 'fast_no_header'))['col1'][0:4]

    for i, fn in enumerate(fnames):

        print("  Extracting from file {} of {}".format(i+1, len(fnames)))
        raw_fn =data_dir+fn            
        #file name of the calibrated file
        outname = raw_fn.split('.fits')[0]+'_calib.fits'
        
        try:
            #if the calibrated file already exists, skip that part
            data = wo.wirc_data(wirc_object_filename=outname)
        except:
            raw_data = wo.wirc_data(raw_filename=raw_fn, flat_fn = flat_fn, dark_fn = dark_fn, bp_fn = bp_fn)
            #run the calibration
            #raw_data.calibrate(mask_bad_pixels=False)
            raw_data.calibrate()
            #add to the list and save it
            #calibrated_list = np.append(calibrated_list, outname)
            raw_data.save_wirc_object(outname)
            data = wo.wirc_data(wirc_object_filename=outname)

