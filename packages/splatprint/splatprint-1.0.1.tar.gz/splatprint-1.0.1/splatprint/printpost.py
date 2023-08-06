import numpy as np

def postprint(array, inputfname, inverse, delay, repair, cautious):
    #open input file
    inputfile = open(inputfname, 'w')
    #universal vars
    printtime = 0
    delaystr = str(delay) + 's'
    inputrpt = 3    #input repeat, number of extra inputs to send at the end of a line
    move_down = '\nDPAD_DOWN ' + delaystr + '\n' + delaystr
    move_up = '\nDPAD_UP ' + delaystr + '\n' + delaystr
    move_right = '\nDPAD_RIGHT ' + delaystr + '\n' + delaystr
    ink = '\nA ' + delaystr + '\n' + delaystr
    erase = '\nB ' + delaystr + '\n' + delaystr

    #invert normal array (to allow for np.nonzeros?) white == True and skip white so swap colors
    if inverse == False and repair == False:
        array = np.invert(array)

    #set up initial delay and A press on connect screen
    inputfile.write('3.0s')
    inputfile.write('\nA ' + delaystr)
    inputfile.write('\n5.0s')
    printtime += delay + 8

    #move to top left, switch to smallest brush
    inputfile.write('\nL ' + delaystr + '\n' + delaystr)
    inputfile.write('\nL ' + delaystr + '\n' + delaystr)
    inputfile.write('\nL ' + delaystr + '\n' + delaystr)
    inputfile.write('\nL ' + delaystr + '\n' + delaystr)
    inputfile.write('\nL ' + delaystr + '\n' + delaystr)
    inputfile.write('\nL_STICK@-100+100 5s' + '\n' + delaystr)
    printtime += (11 * delay) + 5


    #---------------------
    #Fast mode
    if cautious == False:
        #define funcs
        def movetopixel(cursor_index, pixel_index, printtime_mtp):
            if pixel_index < cursor_index:			#pixel is below cursor
                #move cursor
                while cursor_index != pixel_index:
                    inputfile.write(move_down)                 #rotating image 90 degrees clockwise, end of column array is top of image
                    printtime_mtp += delay * 2
                    cursor_index -= 1               #move cursor down
                if cursor_index == 0:               #align if cursor moved to bottom of column
                    for i in range(inputrpt):
                        inputfile.write(move_down)
                        printtime_mtp += delay * 2
            elif pixel_index > cursor_index:			#pixel is above cursor
                while cursor_index != pixel_index:
                    inputfile.write(move_up)
                    printtime_mtp += delay * 2
                    cursor_index += 1
                if cursor_index == 119:             #align if cursor moved to top of column
                    for i in range(inputrpt):
                        inputfile.write(move_up)
                        printtime_mtp += delay * 2
            return cursor_index, printtime_mtp
            
        def printpixel(current_row, cursor_index, repair, inverse, printtime_pp):
            if repair:
                pixel_val = current_row[cursor_index]
                if pixel_val == 1:
                    inputfile.write(erase)
                    printtime_pp += delay * 2
                elif pixel_val == 2:
                    inputfile.write(ink)
                    printtime_pp += delay * 2
            elif inverse:    #printpixel() should only be called for nonzero pixels
                inputfile.write(erase)
                printtime_pp += delay * 2
            else:
                inputfile.write(ink)
                printtime_pp += delay * 2
            return printtime_pp

        #vars
        cursor_index = 119    #cursor y value (given bottom left is (0,0))

        #process array
        for crtrow in array:    #row of 90 degree rotated array, so each column
            printablepx = np.nonzero(crtrow)     #number of printable pixels in row
            printpxlen = np.size(printablepx)    #how many printable pixels are in the column

            if printpxlen == 0:                  #blank column
                inputfile.write(move_right)      #move to next column
                printtime += delay * 2

            if printpxlen == 1:                  #if 1 pixel
                (cursor_index, printtime) = movetopixel(cursor_index, printablepx[0], printtime)
                printtime = printpixel(crtrow, cursor_index, repair, inverse, printtime)
                inputfile.write(move_right)
                printtime += delay * 2
            
            #if more than 2+
            if printpxlen > 1:
                #find whether the top or bottom pixel is closest to the cursor y value
                max_index = np.max(np.nonzero(crtrow))
                min_index = np.min(np.nonzero(crtrow))
                if cursor_index == min_index:
                    closest_index = min_index
                    furthest_index = max_index
                    printdir = 1                           #1 == printing upwards, -1 == downwards
                elif cursor_index == max_index:
                    closest_index = max_index
                    furthest_index = min_index
                    printdir = -1
                elif min_index > cursor_index and max_index > cursor_index:    #cursor is below pixels to print
                    closest_index = min_index
                    furthest_index = max_index
                    printdir = 1
                elif min_index < cursor_index and max_index < cursor_index:    #cursor is above pixels to print
                    closest_index = max_index
                    furthest_index = min_index
                    printdir = -1
                else:                                                          #cursor is in middle
                    if cursor_index - min_index > (max_index - min_index)/2:
                        closest_index = max_index
                        furthest_index = min_index
                        printdir = -1
                    else:
                        closest_index = min_index
                        furthest_index = max_index
                        printdir = 1
                #move cursor, print pixels in column
                (cursor_index, printtime) = movetopixel(cursor_index, closest_index, printtime)
                while cursor_index != furthest_index:
                    if np.any((np.isin(printablepx, cursor_index))):    #if cursor location has printable pixel
                        printtime = printpixel(crtrow, cursor_index, repair, inverse, printtime)
                    if printdir == -1:
                        inputfile.write(move_down)
                        printtime += delay * 2
                        cursor_index -= 1
                    else:
                        inputfile.write(move_up)
                        printtime += delay * 2
                        cursor_index += 1
                #at end of line
                if np.any((np.isin(printablepx, cursor_index))):
                    printtime = printpixel(crtrow, cursor_index, repair, inverse, printtime)
                if cursor_index == 0 and printdir == -1:      #cursor is at bottom of column, printing downwards
                    for i in range(inputrpt):                 #so dropped inputs don't botch the whole thing, just to be safe
                        inputfile.write(move_down)
                        printtime += delay * 2
                elif cursor_index == 119 and printdir == 1:   #cursor is at top of column, printing up
                    for i in range(inputrpt):                 
                        inputfile.write(move_up)
                        printtime += delay * 2
                inputfile.write(move_right)                   #move to next column
                printtime += delay * 2


    
    
    #---------------------
    #Cautious mode (kinda wack code but if it works)
    if cautious:
        #vars
        cur_mv_down = True    #T = cursor is moving from top to bottom, F = cursor is moving from bottom to top
        arypos = 0    #current array y pos, this needs to be tracked manually (since extracting line by line)
        move_dir = move_down    #direction string, either "DPAD_DOWN [delay]s" or "DPAD_UP [delay]s" + delay
        #process the image array
        for crtrow in array: #this iterates for every row in the 2d array
            #skip empty lines
            skip_line = False    #reset on new line
            if np.all(crtrow==0):     #if row is all non-printing (0 for repair, False for nrm/inv)
                skip_line = True
            if skip_line:
                inputfile.write(move_right)            #skip, move to next column
                printtime += delay * 2
            #print the column
            if skip_line == False:    #skip extra processing if skipping line
                if cur_mv_down:    #if moving top to bottom, need to flip the row
                    procrow = crtrow[::-1]    #flip current row, save as processed row
                else:
                    procrow = crtrow    #if flipping isn't needed, make intact row the processed row
                for x in procrow:    #iterate over the row
                    if repair:
                        if x == 1:
                            inputfile.write(erase)
                            printtime += delay * 2
                        elif x == 2:    #2 == ink
                            inputfile.write(ink)
                            printtime += delay * 2
                    elif inverse:    #if inverse, erase when True (white)
                        if x:
                            inputfile.write(erase)
                            printtime += delay * 2
                    else:    #normal mode, ink when True (since flipped array)
                        if x:
                            inputfile.write(ink)
                            printtime += delay * 2
                    inputfile.write(move_dir)
                    printtime += delay * 2
            #runs at the end of the line
            if skip_line == False:
                for i in range(inputrpt):    #send extra directional inputs to make sure cursor is at the edge
                    inputfile.write(move_dir)
                    printtime += delay * 2
                inputfile.write(move_right)    #move to next column
                printtime += delay * 2
                arypos += 1
                if cur_mv_down:    #reverse input direction
                    cur_mv_down = False
                    move_dir = move_up
                else:
                    cur_mv_down = True
                    move_dir = move_down

    #---------------------

    #move cursor to top, capture
    inputfile.write('\nL_STICK@-100+100 5s' + '\n' + delaystr)
    inputfile.write('\nCAPTURE ' + delaystr + '\n' + delaystr)
    printtime += (delay * 3) + 5

    #save image and close file
    inputfile.write('\nMINUS ' + delaystr + '\n' + delaystr + '\n5.0s')
    printtime += (delay * 2) + 5
    inputfile.close()

    #process print time
    printtime_div_ms = divmod(printtime, 60)    #divmod = divide w/ remainder
    printtime_div_hm = divmod(printtime_div_ms[0], 60)
    printtime_div = (printtime_div_hm[0], printtime_div_hm[1], printtime_div_ms[1])
    printtime_str = ("{0:.0f}h {1:.0f}m {2:.2f}s".format(*printtime_div))    #{0}, {1}, etc. reference elements of unpacked tuple (*), :#f means # number precision fixed-point number

    return printtime, printtime_str