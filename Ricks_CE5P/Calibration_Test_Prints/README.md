# Calibration Guide

The following is a Klipper calibration guide. The goal here is to obviously get good prints. However a secondary goal is to push as many settings usually associated with slicer settings into the klipper firmware. Follow these steps in order. Some steps may need to be revisited again after a later step in the calibration sequence. Using Cura ensure the following:

* Use the START_PRINT and END_PRINT macro instead of the usual auto generated gcode
* Acceleration control OFF
* Extra Prime amount set to 0
* Coasting OFF
* Slicer Flow Multipliers are set to 100%
* Install the Printer settings plug in

Before starting calibration, if one has not calibrated velocity and accleration controls in Klipper, be sure to set these to convervative values i.e. vel = 200, accel = 900, square corner vel = 5, and max accel to decel = 450.


## Resources

* https://www.reddit.com/r/klippers/comments/mn8htd/heat_tuning_tower_write_up/
* https://teachingtechyt.github.io/calibration.html
* https://www.klipper3d.org/G-Codes.html
* https://www.klipper3d.org/Pressure_Advance.html
* https://www.klipper3d.org/Resonance_Compensation.html

## Z Offset

Z offset is the difference in height of the probe and the nozzle. In the klipper the command `PROBE_CALIBRATE` can be used help determine this. The general procedure is to adjust the Z pos (which may require changing the printer.cfg such that negative Z values are allowed) until at Z=0 the nozzle is just touching the build plate. A better way is to use a set of spark plug gappers so that at Z=.2mm the 0.2mm gapper barely slides between the nozzle and the build plate.

If your Z off set is way off, set Z-off = 0. In printer.cfg set the minimum Z height to something like -10. Then make small movements i.e. Z=-1, Z=-2, etc until close. Update printer.cfg as describe below and continue on to next paragraph.

If Z off is close. Set Z = 0.2. Use 0.2 gapper to see if the gapper slides while barely touching the nozzle. Adjust up or down in small increments, i.e. Z=0.15, Z=0.12, etc. Once youve found the right Z height that makes the gapper slide snuggly, adjust accordingly. If Z- height is less the .2, then add differences to current Z-off. Else subtract.

See [Klipper](../Klipper/) for printer name. But when Z off set is found, update the printer.cfg found in `~/<priner_name>/config/printer.cfg` under the `[bltouch]` tag. Back up cfg in git repo and firmware restart and double check your Z off again.

## Bed Leveling
**Note** before leveling ensure both Z-rods are equidistance from the buildplate. This will be automated in the future ... TBD.

**NOTE** Double check bed clip positions if they have been moved to ensure the mesh probe points do not cause the nozzle or probe to hit the clips.

**NOTE** Always save mesh as "default". This allows the start print macro to always load the latest mesh.

In klipper w/ mainsail gui simply use the HEIGHTMAP tab in the mainsail GUI. The printer.cfg file defines previous meshes and defines the mesh itself. Use the mesh calibrate routine repeadtly and bed trammers until mesh is sufficiently flat. This should be done fairly regularly as it does not take much time and a level bed is key to a good first layer. 

## PID Tuning

PID tuning calibrates the heat / cool cycle used to keep the heated elements of the printer at a constant temp. This should be done infrequently, however, it should be done if making modifcations to the, bed, hot end, or anything affecting the thermal or electrical systems of the printer.

```
PID_CALIBRATE HEATER=extruder TARGET=240
PID_CALIBRATE HEATER=heater_bed TARGET=80
```

## E Steps Calibration

To calibrate E-Steps measure some amount of filament downstream from the extruder. Extrude a given amount of material, denoted $d_c$, such that $d_c$ is a good amount less that your mark. Measure how much material was actually extruded, denoted $d_a$. Now let $r_n$ and $r_c$ be the new and current values for the extruders rotation distance value found in [printer.cfg](../Klipper/printer.cfg). Calculate $r_n$ as follows,

$$r_n =  r_c \frac{d_a}{d_c}$$

Perform this calibration step when changing filament type (PLA vs PETg) or when making any big changes to the hot end or extruder.

## First Layer Test

At this point one can see how well a simple single layer print will adhere to the bed. Print a single square  at the center of the plate. Look for rough top surface finish (too close) or gaps between lines (too far). Use reasonable first estimates of temp, retraction, speed, and  other slicer settings. Keep things conservative and air on the side of slow and precise. For PETg one can do 240 nozzle, 80 buildplate, 6mm w/ 40mm/s retractions, 25mm/s init layer print speed, 80mm/s print speed, 125mm/s init layer travel speed, 200mm/s travel speed.

## XYZ Calibration Cube
Print the 20mmx20mmx20mm calibratoin cube found in `xyzCalibration_cube.stl`. This will illuminate several potential issues or places where prints can be improved. Print with the same settings used on the first layer test. This print will also serve as a control for when we futher tune the printer.

## Extrusion Factor

Contruct a hollow box with no top or bottom of a single layer of thickness. An STL for a 0.4mm nozzle / line thickness is provided (`Extrusion_Box_.4mm.stl`). Slice with same parameters as above and ensure SLICER flow compensation is set to 100%. Measure the thickness of the walls. Let $d_e$ be the line width or expected wall depth. Let $d_a$ be the actual width of the walls (take average of all 4 sides). Then the correct flow multiplier is simply $d_e / d_a$. If the current FIRMWARE flow factor is not 100%, then multiple the value calculated by the current FIRMWARE flow multiplier.

To save flow multiplier values in klipper, modify the START_PRINT macro with `M221 S<FLOW%>`.

Would be wise to revist this test after pressure advance is dialed. However it is a chicken and egg situation where each will affect the other.

## Temp Tower

Slice `TemperatureTower230-250.stl` using the settings established in all previous tests. Run the print and execute the command below as it starts.

```
TUNING_TOWER 
    COMMAND='SET_HEATER_TEMPERATURE HEATER=extruder'
    PARAMETER=TARGET
    START=252.5
    SKIP=1
    BAND=10
    FACTOR=-0.5
```

To select an appropiate temperature, look at the quality of the overhangs, layer lines, etc. Choose the highest temperature with the most acceptable print quality.

##  Retraction Calibration

We will be using firmware retractions.  In Cura, under the Printer Settings tab enable Firmware retractions. This will replace E value based retractions with G10 and G11 gcode commands. In printer.cfg add the following lines:

```
[firmware_retraction]
retract_length: 2
retract_speed: 25
unretract_extra_length: 0
unretract_speed: 25
```

Starting with the above parameters, we will use the file `Retraction_Spikes.stl`. Slice and print. On the first print verify that the firmware retractions have been implemented and functioning correctly. Start by dialing in the retraction length. While it is printing, visually observe the retraction process. If retraction distance is too short one should observe excessive stringing and should see that not all the filament is sucked back into the nozzle. If too long, one should observe that there is a time delay after a unretarction to when filament starts being pushed out the nozzle. Pick the mininum retraction distance that miinimizes stringing and other retraction artifacts. One can adjust retraction settings real time via the command:

```
SET_RETRACTION 
    [RETRACT_LENGTH=<mm>] 
    [RETRACT_SPEED=<mm/s>] 
    [UNRETRACT_EXTRA_LENGTH=<mm>] 
    [UNRETRACT_SPEED=<mm/s>]
```

Next, we can dial in unretract_extra_length. The extra extrusion lentght should be 0, however, if one always notices a time delay between unretractions and continued extrusion, increment this by small values i.e. 0.1 to push a little extra filamant after an unretraction.

Finally speeds can be tuned. For simplicity, set retract and unretract speed to be the same. Set as high as possible, without extruder slippage and such that filament is actually retracted. Too fast can cause a discontinuity to form in the filament. 

**TODO**
* unretract extra lenght
* differing retract and unretract speed
* Z-Hop doc and play with

### Retraction Tower

The above works for small iterative changes. However, if one has no good starting parameters or is not seeing enough of delta when perturbing settings, the following retraction tower can be used. Slice the file `Retraction_Tower.stl` using the same parameters used above. Then same as the temp tower use the following tuning tower command to vary the retraction distance, fixing the other params

```
TUNING_TOWER 
    COMMAND='SET_RETRACTION'
    PARAMETER=RETRACT_LENGTH
    START=1.5
    SKIP=1
    BAND=5
    FACTOR=.2
```

The above will vary retraction length every 5mm by 1, surveying 2mm to 12mm retraction distance. Once final retraction settings are found, update the printer.cfg file. This same command can be used to vary retract and unretract speed by changing the appropiate command inputs (use the `SET_RETRACT_SPEEDS` macro as the command, parameter = TEMP, start = 17.5, skip = 1, band = 5, and factor = 1 to survey 20-70 mm/s, incrementing 5mm/s every 5mm). Once a pattern emerges one can use the first routine shown above to fine tune retraction settings. Note if changing the command to shrink the survyed windowed, remember to subtract half an increment from the starting value.

## Acceleration and Resonance

The Klipper provided documentation on this is more than satisfactory: https://www.klipper3d.org/Resonance_Compensation.html. 

## Pressure Advance

Before starting pressure advance tuning, print an XYZ calibration cube and print one after as a tracker of this settings improvement in print quality. The documentation provided by Klipper is more than satisfactory on this particular setting, therefor we just provide a link to be followed: https://www.klipper3d.org/Pressure_Advance.html. Upon completing this calibration step, it is advisable to revist temp, flow, and extrusion calibration. Keep in mind that if one changes these settings one will need to do pressure advanced calibration again as a final step, as pressure advanced should always be done as the last major calibration step.

## Speed Test and Max Flow Rates

Just Keep Flow under 10 mm3/s and print speeds low and slow for now. More to follow

## Square Corner Velocity

Just keep at 5 per klipper reccomendations.

## Surface Quality Considerations

* Fuzzy Skin
* Ironing
    * https://all3dp.com/2/prusaslicer-ironing-simply-explained/
* Types of top surface layer pattern
* Anchor solid infill

# Manual Extrusion Tests and Calculations

In the event one wishes to construct some useful GCODE files and macros to calibrate very speicific printing patterns one can use the following to calculate the proper amount of extruded material. To do this we need to specify the following values:

* $d_f$ : Diameter of filament (usually 1.75mm)
* $w$ : Line width (usually nozzle diameter, see [below](#slicer-setting))
* $h$ : Layer height
* $L$ : The length of the linear movement

Assume a rectangluar cross section as Cura does (other slicers such as Slic3r uses a different cross section [calculation](https://manual.slic3r.org/advanced/flow-math)). Now the amount of material we need to extrude, $E$ is calculated as the following.


$$\pi \frac{d_f^2}{4} E = wh(L - w)$$

This simply states the volume of the material inputed through the extruder needs to equal the volume of the line we intend to draw. The term $(L-w)$ is to compensate for the fact that the nozzle does travel the entire length of the extruded line, it starts and stop half a line width away from the limits of the line. So,

$$ E = \frac{4wh(L-w)}{\pi d_f^2} $$

Now we can execute the following gcode to test a single line extrusion. Assume have the following inputs)

* T_b is the temp of the bed
* T_n is the temp of the nozzle
* X_i is the x pos of the start of the line
* X_f is the x pos of the start of the line
* Y_i is the y pos of the start of the line
* Y_f is the y pos of the start of the line
* V_t is the travel velocity in mm/s
* V_p is the printing velocity in mm/s
* V_r is the retraction velocity
* R is the retraction distance

```
G28     ;Home

BED_MESH_PROFILE LOAD="default"

M140 S{T_b}  ;Set Bed Temp
M104 S{T_n}  ;Set Nozzle Temp
M190 S{T_b}  ;Wait for bed to reach temp
M109 S{T_n}  ;Wait for Nozzle to reach temp

M82    ;absolute extrusion mode
G92 E0 ;Reset extrusion counter
G0 X{X_i +- w/2} Y{Y_i +- w/2} Z{LAYER_HEIGHT} F{60*V_t} ;Determine +- based on travel direction
G1 X{X_f -+ w/2} Y{Y_f -+ w/2} E{E} F{60*V_p}
G1 E{E-R} F{60*V_r}

G91
G0 X5 Y5 Z5
G90
G0 X180 Y25 Z10
```

# Calibration and Settings

## Slicer Setting

The following settings are usually set in the slicer and will change from print to print and material to material. **Currently Targeting PETg.** The settings high lighted are the key ones to look at and are sub divided into Print settings, Filament Settings, and Printer Settings (this is how SuperSlicer organizes its settings).

### Print Settings

| Parameter | Description | Value Ranges | Current Values | Comments |
| --- | --- | --- | --- | --- |
| Perimeters | Number of wall lines | 2-5 | 4 | Take the line width and multiply by number of walls to get wall width in mm |
| Horizontal Shells | Number of top and bottom lines | 2-5 | 5 | Take the layer height and multiply by number of walls to get wall width in mm |
| Fuzzy Skin | Adds rough surface texture | Yes or no |  Depends | See above as there are sveral sub params |
| Layer Height | Height of individual layer of plastic | .1mm - .32mm | .20mm| Affects quality and is a function of the nozzle size |
| Infill Type | The pattern used to create infill | Alot | Rectilinear | - |
| Infill Percent | How desne the infill pattern is | 20 - 100 | 100 | - |
| Skirt and Brim | Various methods to improve build plate adhesion | skirt or brim | Depends | Always a slirt unless a brim is needed |
| Ironing Mode | smooths over outer surface | yes or no | depends | - |
| Print Speed | Speed while extruding | 10mm/s - 200mm/s | 60mm/s | - |
| Infill Speed | - | - | 60mm/s | - |
| Wall Speed | - | - | 30mm/s | - |
| Travel Speed | Speed while not extruding (traveling) | 50mm/s - 250mm/s | 150mm/s | - |
| Init Layer Print Speed | Speed while extruding on first layer | 5mm/s - 40mm/s | 20mm/s | - |
| Init Layer Travel Speed | Speed while not extruding on first layer | 5mm/s - 200mm/s | 150mm/s | On prints with long travels, if this value is too low it can cause oozing |
| Top / Bottom Print Speed | Speed on top and bottom layers | - | 30mm/s | - |
| Top Surface Speed | - | - | 20mm/s | - |
| Number of Slow Layers | Ramp up to full speed | - | 3 | - |

| Nozzle Diameter | Not a parameter but size of nozzle is good to track | .2mm - 1.0mm | .4mm | Hardened Mk8 nozzle |

| Line Width | How wide each line of plastic is | +/- 50% of nozzle size | .4mm or .6mm for large prints| Can be used to get the affect of smaller / larger nozzle sizes without actually changing nozzles. When line width > nozzle diameter, increasing temp and flow rate can help |
| Nozzle Temp | Depends on material. Current values for PETg | 220 - 260 | 240C | Lower end gives better retraction but worse inital layer bed adhesion and under extrusion. Goal is to print as hot as possible w/o detrimental affects |
| Bed Temp | Temp of heated bed | 50 - 80 | 80 | PLA 50-60, PETg 70-80 | 
| Retract at Layer Change | helps with blobs on corners | yes or no | Yes | - |




| Combing Mode | Limits movement during travel to already printed areas | Several | OFF  | - |




### Filament Settings

### Printer Settings


## Firmware Settings

With Klipper all firmware settings are found in [printer.cfg](../Klipper/printer.cfg).

## Starter G-Code

In Klipper the prefered way of starter GCODE is a macro located in the [printer.cfg](../Klipper/printer.cfg). 

```
START_PRINT
```

## Ending G-Code
```
END_PRINT
```

# Calibration Macros

Klipper Macros allow one to automate several tasks and simplify slicer profiles. This can be found in [printer.cfg](../Klipper/printer.cfg).

| Macro Name | Inputs | Comments |
| --- | --- | --- |
| START_PRINT | NONE | Load bed mesh, home, and purge. Place in slicer profile as starter GCODE |
| END_PRINT | NONE | Turn off relavent systems, wipe out nozzle and restract, and disable steppers |