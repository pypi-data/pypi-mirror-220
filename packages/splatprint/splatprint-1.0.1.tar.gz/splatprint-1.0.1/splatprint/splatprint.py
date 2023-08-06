#!/usr/bin/env python3

#import libraries
import sys    #for quitting the program
import os     #for checking macro size
from PIL import Image
import numpy as np

from splatprint.printpost import postprint
from splatprint.macropreview import preview
from splatprint.repairpost import procrepair, genrepairarray


def main():
    #output vars
    nrm_macro_name = 'nrm_macro.txt'
    inv_macro_name = 'inv_macro.txt'
    rpr_macro_name = 'rpr_macro.txt'
    nrm_preview_name = 'nrm_preview.png'
    inv_preview_name = 'inv_preview.png'
    rpr_preview_name = 'rpr_preview.png'
    scr_name = 'proc_screenshot.png'    #1280x720 screenshot processed to 320x120

    #-----------------------------
    #Command line

    help_msg = '''Standard usage:
        img3splat -i "image.png"
    where "input.png" is the 320x120 image to print

    Repair mode:
        img3splat -i "image.png" -r "screenshot.jpg"
    "input.png" is the image to change the post to (320x120)
    "screenshot.jpg" is the post to fix (1280x720 Switch screenshot or 320x120 image)

    Save mode:
        img3splat -s "screenshot.jpg"
    where "screenshot.jpg" is the 1280x720 Switch screenshot to save as a 320x120 image

    Optional arguments:
    -d [#]: delay in seconds for print inputs (e.g. "-d 0.05"), 0.1 by default
    -c: cautious mode, prints in full columns (for unstable connections)
    -p: prints post printing instructions after macro generation
    -v: verbose, prints extra messages about generation steps
    '''

    #default values
    repair = False                #repair mode
    delay_input = ''
    delay = 0.1
    cautious = False              #cautious mode
    print_instructions = False    #show print instructions on completion
    verbose_en = False            #verbose
    save = False                  #save mode

    #CLI Args
    args = sys.argv[1:]
    #print help if no args
    if len(args) == 0:
        print(help_msg)
        sys.exit()
    #screenshot image (rpr_input)
    if '-s' in args:
        save = True
        try:
            rpr_input = args[(args.index('-s') + 1)]
        except:
            print('Error: save argument set, but screenshot not specified!')
            sys.exit()
    else:
        #input image (img_input)
        if '-i' in args:
            try:
                
                img_input = args[(args.index('-i') + 1)]
            except:
                print('Error: input argument set, but image not specified!')
                sys.exit()
        #repair image (rpr_input and repair)
        if '-r' in args:
            repair = True
            try:
                rpr_input = args[(args.index('-r') + 1)]
            except:
                print('Error: repair argument set, but repair image not specified!')
                sys.exit()

        #delay (delay_input)
        if '-d' in args:
            try:
                delay_input = args[(args.index('-d') + 1)]
            except:
                print('Error: delay argument set, but time not specified!')
                sys.exit()
        #cautious
        if '-c' in args:
            cautious = True
        #print_instructions
        if '-p' in args:
            print_instructions = True
    #verbose
    if '-v' in args:
        verbose_en = True

    #-----------------------------
    #validate inputs
    if save:
        try:
            rprimg = Image.open(rpr_input)
        except:
            print("Error: Invalid screenshot file! Image isn't recognized or doesn't exist.")
            sys.exit()
        if (rprimg.size == (1280,720)) == False:
            print('Error: Screenshot image is not 1280x720!')
            sys.exit()
        if verbose_en:
            print('Saving screenshot "' + str(rpr_input) + '"')
    else:
        try:
            if delay_input != '':
                delay = float(delay_input)
        except:
            print('Error: Invalid delay input! Not a number.')
            sys.exit()
        if delay <= 0:
            print('Error: Invalid delay input! Must be greater than 0.')
            sys.exit()
        if verbose_en:
            print('Using delay value of ' + str(delay) + 's')
        #open main image, convert to bilevel
        try:
            mainimg = Image.open(img_input).convert('1')
        except:
            print("Error: Invalid file! Image isn't recognized or doesn't exist.")
            sys.exit()
        if mainimg.size != (320,120):
            print('Error: Image is not 320x120!')
            sys.exit()
        #open repair image, check size
        if repair:
            try:
                rprimg = Image.open(rpr_input)
            except:
                print("Error: Invalid repair file! Image isn't recognized or doesn't exist.")
                sys.exit()
            if ( (rprimg.size == (1280,720)) or (rprimg.size == (320,120)) ) == False:
                print('Error: Repair image is not 1280x720 or 320x120!')
                sys.exit()
            if verbose_en:
                print('Repairing "' + str(rpr_input) + '" with "' + str(img_input) + '"')
        else:
            if verbose_en:
                print('Printing "' + str(img_input) + '"')

    #-----------------------------
    # generate 320x120 rotated image from repair image
    if repair or save:
        rpr_out = procrepair(rprimg)    #returns (rotated array, processed screenshot image)
        rprimg_ar = rpr_out[0]
        scrimg = rpr_out[1]

    #-----------------------------
    # if save, save screenshot and exit
    if save:
        scrimg.save(scr_name)
        if verbose_en:
            print('Saved processed image from screenshot!')
        sys.exit()

    #-----------------------------
    #generate np arrays from images

    #convert main image to np array, rotate 90 deg to process as columns
    mainimg_ar = np.array(mainimg)
    mainimg_ar = np.rot90(mainimg_ar, 3)

    #generate repair array, generate macro 
    if repair:
        proc_ar = genrepairarray(mainimg_ar, rprimg_ar)
        # check if proc_ar has no printable pixels, if so, terminate program
        if np.all(proc_ar == 0):
            print('Error: No pixels to repair!')
            sys.exit()

    #-----------------------------
    #generate macros

    if verbose_en:
        if cautious:
            print('Printing in cautious mode!')
        else:
            print('Printing in fast mode!')

    #generate repair macro
    if repair:
        rpr_printtime, rpr_printtime_str = postprint(proc_ar, rpr_macro_name, False, delay, True, cautious)
        if verbose_en:
            print('Generated repair macro!')

    #generate normal/inverse macros
    else:
        nrm_printtime, nrm_printtime_str = postprint(mainimg_ar, nrm_macro_name, False, delay, False, cautious)
        if verbose_en:
            print('Generated macro!')
        inv_printtime, inv_printtime_str = postprint(mainimg_ar, inv_macro_name, True, delay, False, cautious)
        if verbose_en:
            print('Generated inverse macro!')

    #------------------------------
    #run preview script
    if repair:
        preview(rpr_macro_name, rpr_preview_name, False, True, scrimg)
        if verbose_en:
            print('Generated repair macro preview!')
    else:
        preview(nrm_macro_name, nrm_preview_name, False, False, False)
        if verbose_en:
            print('Generated macro preview!')
        preview(inv_macro_name, inv_preview_name, True, False, False)
        if verbose_en:
            print('Generated inverse macro preview!')

    #------------------------------
    #closing messages

    #show/compare print times
    if repair:
        print('Repair print time: ' + rpr_printtime_str)
    else:
        if nrm_printtime < inv_printtime:
            print('Normal macro likely has shorter print time.')
            print('(' + nrm_printtime_str + ' vs. ' + str(inv_printtime_str) + ')')
        elif nrm_printtime > inv_printtime:
            print('Inverse macro likely has shorter print time.')
            print('(' + inv_printtime_str + ' vs. ' + nrm_printtime_str + ')')
        else:
            print('Both macros have the exact same size (' + nrm_printtime_str + ').')

    if print_instructions:
        print('''To print, open a blank plaza post (or all black if inverse),
    then press the "sync" button on your controller to disconnect it.
    Make sure your Switch is in handheld mode to prevent desyncs.''')
        if repair:
            print('''Then, run this command to start the print:
        sudo nxbt macro -c "rpr_macro.txt" -r''')
        else:
            print('''Then, run one of these commands to start the print:
        sudo nxbt macro -c "nrm_macro.txt" -r
        sudo nxbt macro -c "inv_macro.txt" -r''')
        print('Woomy! くコ:彡   Ｃ:。ミ')