from PIL import Image
import numpy as np


#set up vars
def preview(macroname, output, inverse, repair, repairimg):
    macro = open(macroname, 'r')
    curx = 0 #cursor x value
    cury = 0 #cursor y value

    #color options
    BG_clr_nrm = (255,255,255)
    BG_clr_inv = (0,0,0)
    A_clr_nrm = (0,0,0)
    B_clr_inv = (255,255,255)
    A_clr_rpr = (123,0,0)
    B_clr_rpr = (255,200,200)
    skip_clr_nrm = (200,200,255)
    skip_clr_inv = (0,85,215)
    skip_clr_rpr = (123,123,255)
    #set colors based on mode
    if repair:
        skip_clr = skip_clr_rpr
        A_clr = A_clr_rpr
        B_clr = B_clr_rpr
    elif inverse:
        BG_clr = BG_clr_inv
        skip_clr = skip_clr_inv
        B_clr = B_clr_inv
    else:
        BG_clr = BG_clr_nrm
        skip_clr = skip_clr_nrm
        A_clr = A_clr_nrm

    #set up canvas
    if repair:
        img = repairimg.convert('RGB')
    else:
        img = Image.new(mode="RGB", size=(320, 120), color=BG_clr)
    img_array = np.array(img)

    #iterate across image
    with open(macroname, 'r') as f:
        for x in range(3):
            next(f)
        for l_no, line in enumerate(f):
            if line.startswith("A"):
                img_array[cury][curx] = A_clr
            if line.startswith("B"):
                img_array[cury][curx] = B_clr
            if 'LEFT' or 'RIGHT' or 'UP' or 'DOWN' in line:
                if repair:
                    if (img_array[cury][curx][0] == A_clr[0] and        #ugly, but if it works it works
                          img_array[cury][curx][1] == A_clr[1] and
                          img_array[cury][curx][2] == A_clr[2]) == False:
                        if (img_array[cury][curx][0] == B_clr[0] and
                              img_array[cury][curx][1] == B_clr[1] and
                              img_array[cury][curx][2] == B_clr[2]) == False:
                            img_array[cury][curx] = skip_clr
                elif inverse:
                    if (img_array[cury][curx][0] == B_clr[0] and
                              img_array[cury][curx][1] == B_clr[1] and
                              img_array[cury][curx][2] == B_clr[2]) == False:
                        img_array[cury][curx] = skip_clr
                else:
                    if (img_array[cury][curx][0] == A_clr[0] and
                          img_array[cury][curx][1] == A_clr[1] and
                          img_array[cury][curx][2] == A_clr[2]) == False:
                        img_array[cury][curx] = skip_clr
            if 'LEFT' in line:
                curx = max(curx - 1, 0)
            if 'RIGHT' in line:
                curx = min(curx + 1, 319)
            if 'UP' in line:
                cury = max(cury - 1, 0)
            if 'DOWN' in line:
                cury = min(cury + 1, 119)
            if 'MINUS' in line:
                break

    #cleanup + output
    macro.close()
    output_image = Image.fromarray(img_array)
    output_image.save(output)


# #debug
# splat_macro = 'inv_macro.txt'
# splat_output = 'test_preview.png'
# preview(splat_macro, splat_output, True, False)