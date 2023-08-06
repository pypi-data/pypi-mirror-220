# Splatprint
Splatprint is a post printer for Splatoon 3 that allows you to print images without a specialized microcontroller, only requiring a Linux machine with a Bluetooth connection (or a Windows/Mac machine with an external Bluetooth adapter running a Linux VM). More specifically, splatprint generates macros for [NXBT](https://github.com/Brikwerk/nxbt), which handles the actual printing process. Splatprint is heavily inspired by (but wholly independent from) [img2splat](https://github.com/JonathanNye/img2splat), but fixes some issues and allows misprints to be repaired from a screenshot.

## How to print
1. Install [JonathanNye's fork of NXBT](https://github.com/JonathanNye/nxbt/tree/experiment/busy-wait) via:

        sudo pip install https://github.com/JonathanNye/nxbt/archive/experiment/busy-wait.zip

    Although splatprint does work with [NXBT's main branch](https://github.com/Brikwerk/nxbt), the fork is very highly recommended as it fixes major timing issues. If you have errors on NXBT installation, make sure to check the "Troubleshooting" portion of NXBT's README.md.

    If installing on a VM, [read the installation instructions here](https://github.com/Brikwerk/nxbt/blob/master/docs/Windows-and-macOS-Installation.md) (but make sure you clone the fork, not the main NXBT repo).

2. Run NXBT's test function to make sure the virtual controller connects and syncs properly:

        sudo nxbt demo

3. Install splatprint via:

        pip install splatprint

4. Create a 320x120 horizontal image to serve as your plaza post. Images don't necessarily have to be 2-bit grayscale, as they will be automatically converted based on luminance, but dithering *will not* be applied. Processing such images to grayscale beforehand is highly recommended. Any format readable by `Pillow` is supported.

5. Run splatprint:

        splatprint -i "image.png"

    Additional flags are listed under "Usage" below.

    Splatprint creates macros for printing on blank canvases (`nrm_macro.txt`) and all-black canvases (`inv_macro.txt`). Depending on post contents, one may be significantly faster than the other; splatprint will suggest which macro to use by comparing the print times of both.

    Previews of macro prints are generated as `nrm_preview.png` and `inv_preview.png`. Blue pixels represent pixels the cursor passes over but doesn't print, while black/white (depending on macro type) indicates any printed pixels.

6. Open the Splatoon post interface in horizontal mode. If using the inverse macro, manually paint the canvas black (touchscreen with largest brush size); otherwise, clear the canvas by pressing on the left joystick. The macro will automatically set the brush to the smallest size and move the cursor to the top left, so cursor size/position doesn't matter. 

7. Undock your Switch, as any change in HDMI input will drop inputs for a short period. If using a longer macro, you may want to remove the USB-C cable from the dock and plug it directly into the Switch.

8. Press the sync button on your controller(s) and wait until the screen shows the "Press L+R on the controller." menu. Then, run the NXBT macro via:

        sudo nxbt macro -c "nrm_macro.txt" -r
    
    or

        sudo nxbt macro -c "inv_macro.txt" -r

    The macro will automatically press - to save the image on completion.
    
9. If you run into any errors with your print, or if you want to make tweaks to the image after the fact, you can run splatprint in *repair mode*, which automatically detects wrong pixels from an in-game screenshot. Running a print macro will automatically save a screenshot to the Switch's album to use with repair mode.

    If you're transferring the screenshot via the Switch's "Send to Smartphone" feature, make sure to **save the image to your phone's camera roll** rather than copying it to your phone's clipboard. Transferring the image by copying the image to clipboard introduces significant JPG compression, interfering with image recognition (at least on iOS).

        splatprint -i "image.png" -r "screenshot.jpg"

    The "screenshot" input accepts either a 1280x720 (Switch screenshot size) or a 320x120 image (original printed post). The second option is useful for making tweaks to a properly printed post.

    Repair mode generates the repair macro `rpr_macro.txt` and the `rpr_preview.png` macro preview. In the repair mode preview, A/B inputs are represented with lighter and darker shades of red rather than black and white.

    Do note that due to cursor interference, repair mode *will not* repair the top left 2x2 pixels of the post.

10. Like before, disconnect your controllers with the post open. Then, run the repair macro via:

        sudo nxbt macro -c "rpr_macro.txt" -r

    The repair macro will also take a screenshot and press - to save after printing.

## Why Splatprint?
Splatprint is designed for higher reliability when printing complex posts, minimizing the need for manual touchups.

- In fast mode (default), splatprint scans the contents of each column to minimize the amount of inputs used when printing. To reduce the effects of dropped inputs, if the last pixel in a column is located at the top or bottom of the canvas, it also sends extra up/down inputs to ensure the cursor is at the proper location.
- Splatprint can also print in cautious mode, printing in full columns to minimize the effects of dropped inputs. Printing in columns rather than rows reduces the area of effect of dropped inputs. 
- In case of errors, splatprint supports taking a screenshot of the Splatoon post interface to generate a repair macro that fixes any incorrect pixels. This feature can also be used to tweak the original image without printing the image from scratch.
    
- Splatprint can also save the post contents of a screenshot to a 320x120 image, allowing you to rough out a post on the touchscreen and polish it in an image editor (useful if you don't have a drawing tablet).

## Demonstration

[insert images here]

## Usage
### Arguments

You can view the help message by running `splatprint` without any arguments.

Standard usage of splatprint is as follows:

    splatprint -i "input.png"

- `-i "input.png"`: Input image, with `"input.png"` being a 320x120 image of the post you want to print. Splatprint will convert the image to black and white automatically (based on luminance), but will not apply dithering for any RGB/grayscale images. This can be in any format supported by `Pillow`, but a lossless format (like `.png`) is recommended.

- `-d [#]` (optional): Delay, in seconds. Indicates the amount of time a button is pressed, as well as the amount of time the macro waits before inputting another button press. If not specified, will use the default value of 0.1.

    Lowering this value will increase the speed of macro execution at the risk of more dropped inputs. If you're printing longer macros and have a stable connection, it may be useful to start with a smaller delay to print the bulk of the post and do a second pass in repair mode with the default value (this hasn't been tested, though).

- `-c` (optional): Cautious. If enabled, splatprint will pass the cursor through the entire column of any columns that contain printable pixels rather than moving to the next column after reaching the last printable pixel. This reduces the effects of any dropped inputs, as splatprint sends extra inputs at the end of a column to ensure the cursor is aligned with the top/bottom of the image, but usually significantly increases print time. However, enabling this does significantly reduce macro generation time.

- `-v` (optional): Verbose. If enabled, splatprint will print messages when the program generates a macro file or macro preview file. Splatprint will still recommend a macro to use with this flag disabled.

- `-p` (optional): Print instructions. If enabled, splatprint will print post printing instructions after generating the macros, including post setup and the commands for running the macro file with NXBT.

Repair mode usage is as follows:

    splatprint -i "input.png" -r "screenshot.jpg"

- `-i "input.png"`: Input image, with `"input.png"` being the 320x120 image that splatprint will correct the post to. Usually the original image used to generate the macro in normal operation. Supported formats and color space are identical to standard operation.

- `-r "screenshot.jpg"`: Runs splatprint in repair mode. This generates a macro file that targets any pixels that were inputted incorrectly in-game. `screenshot.jpg` is the image of the in-game post that needs to be corrected. Must be either a 1280x720 screenshot of the post interface, taken with the Switch's capture button, or a 320x120 image of the post. The images saved to the Switch's album after publishing a post are not supported.

    Screenshots should be taken with the canvas set horizontally, the brush size set to smallest, and the cursor placed in the top left. However, manual screenshots usually aren't needed; macros generated by splatprint will automatically save an appropriate screenshot at the end of execution. See "How to print" above for some details on how to best transfer the screenshot to your computer while minimizing compression.

- `-c`, `-v`, and `-p` (optional): Function identically to standard operation.

    If the initial macro suffered from several dropped inputs due to an unstable connection, cautious mode (`-c`) is recommended.

Save mode usage is as follows:

    splatprint -s "screenshot.jpg"

- `-s "screenshot.jpg"`: Save screenshot, with `"screenshot.jpg"` being a 1280x720 screenshot of the post interface, taken with the Switch's capture button. Saves the detected 320x120 post from the 1280x720 screenshot of the post interface as `proc_screenshot.png`. Useful if you want to edit a post made in-game on the computer.

    Unfortunately, pixels around the in-game cursor will not be detected properly. To minimize the cursor's interference with detection operations, it's recommended to set the cursor to the smallest brush size and place it in the corner of the canvas. Improper usage of the Switch's "Sent to Smartphone" feature may also introduce extra JPG compression that interferes with detection; see "How to print" above for details.

- `-v` (optional): Functions identically to standard operation.

Save mode cannot be used in conjunction with the macro generation modes.

### Outputs
- `nrm_macro.txt` and `inv_macro.txt`: Macro files generated when running the program normally. `nrm_macro.txt` is intended for printing on a blank canvas, and `inv_macro.txt` is intended for printing on an all-black canvas.
- `rpr_macro.txt`: Macro file generated when running in repair mode.
- `nrm_preview.png`, `inv_preview.png`, and `rpr_preview.png`: Previews of macro execution. Blue pixels represent pixels the cursor will pass over but not print. For `nrm_preview.png`, pixels to be printed are marked in black, while untouched pixels are marked in white; for `inv_preview.png`, pixels are marked the opposite color. For `rpr_preview.png`, untouched pixels are marked by their color in the original post while printed pixels are marked in lighter and darker shades of red.

## Dependencies
Splatprint uses `NumPy` and `Pillow`, both of which should be automatically installed on splatprint installation.

Additionally, to run the generated macros, you also need [JonathanNye's NXBT fork](https://github.com/JonathanNye/nxbt/tree/experiment/busy-wait) (highly recommended to fix timing issues) or the standard version of [NXBT](https://github.com/Brikwerk/nxbt). As splatprint doesn't need NXBT to run (and installation of it requires root privileges), it is not included as a dependency.
