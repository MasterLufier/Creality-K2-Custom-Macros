# Creality-K2-Custom-Macros
Creality K2 Plus macros for better ORCA Slicer compatibility and other improvements\
Based on ideas: https://github.com/jamincollins great thanks!\
Special thanks: https://github.com/Tartarianec for Creality libs functions extraction \
GPL-3.0 license\
Author: Mikhail Ivanov masluf@gmail.com 
> [!NOTE]
> Only for Creality K2 Plus. For K2 and K2 PRO, you need to make some changes and tests.\
> Macros tested on 1.1.3.13 Printer firmware and 1.1.3 CFS Firmware.\
> Tool.cfg does not work with the 1.1.4.8 firmware. But this firmware has a lot of bugs, and I do not recommend installing it.

> [!WARNING]
> Using custom macros could damage your printer and void your warranty, or cause unexpected behavior.

## Key Features:
### main.cfg
- Fix the exhaust fan to improve Orca's (and Creality Print) "Activate Air Filtration" function.
- Implement dynamic control of the exhaust fan for improved heating, cooling, and air filtration.
- Bed mesh store for different bed temperatures
- Better start printing with an additional fast start option for printing the same model (through the virtual pin). This would be useful for printing smaller parts or testing and soak time up to 10 minutes (through virtual pins as well) for better bed stabilization and the best first layer for large parts or printing many parts at once.
- The toolhead moves quickly after RESUME printing to prevent oozing.
- `AUTO_MESH` is a macro that creates a mesh for each desired temperature set under `variable_bed_mesh_temps` in `main.cfg`. Just fill comma separated list, save, push the button and wait. 

### overrides.cfg
- Increased accuracy of Z_TILT_ADJUST
- Default bed mesh calibration is turned off after printer restart
- Disabled prtouch console flood
- Max bed temp increased to 140c
- Heater fan speed increased to full. It's ok for heating but you can get best result with my Ultimate Exhaust system https://www.crealitycloud.com/model-detail/67c9f8b07f0b8c17944c377b?source=22
- prtouch tuned for accuracy \
!!!REMOVE ALL BED MESHES AFTER INSTALL THIS COMPONENT, OR USE AUTO_MESH WITH ALL BED TEMPERATURES BEFORE FIRST PRINT!!!

### graphite_pre.cfg and garaphite.cfg
- special overrides for R3MEN graphite bed \
  include graphite_pre.cfg after mai.cfg and garaphite.cfg after overrides.cfg
  
### tool.cfg
> [!NOTE]
> I am not sure about all the commands in this module, as they are the result of reverse engineering and require a lot of testing. But I have been using these features for a year and they work well most of the time.

- added Toolhead buttons for manual load and unload filaments. T17 for unload any. Do NOT press any buttons except T17 to unload filaments. \
![изображение](https://github.com/user-attachments/assets/afea66c2-4f16-4baf-859d-b6a7c3ac8330)
- Unloading CFS filament is disabled after printing. This is great for reusing the same filament.
- Spoolholder can be used from ORCA without unplugging CFS and feed filament through buffer! Just add +1 filament to your project (if you have 1 CFS connected - fifth, if 2 CFS-ninth etc.), set it for parts and push print! \
![изображение](https://github.com/user-attachments/assets/f3d3497c-8c7c-4c29-9110-13ea197c1ac1)
- All loading and purging parameters, such as temperature and velocity, are used from the slicer, and not from the printer's filament database or printer's on-screen menu.
- Added pressure stabilization to the last purging step. This allows you to print without a skirt, a brim, a priming tower, or any other garbage objects. However, in some cases, such as when changing filament types or opposite colours changes, you may want to add a priming tower for better print quality.
- Loading and unloading CFS filament as quickly as possible.
- Added custom logic for material autorefilling. All information such as filament type and color is taken from macro parameters, not from printer settings.\
  How autorefill works:
0. In the tool.cfg file CHECK_REFILL gcode_macro:
- Set up the pipe length using the `variable_cfs_pipe_length`. It is the full length from the CFS input pipe to the toolhead input pipe! (including pipes inside the CFS).
- Set up EXCLUDES line role `variable_refill_roles`. By default ["Perimeter", "ExternalPerimeter", "OverhangPerimeter"] to minimize artefacts around the perimeters. For all role types, see the slicer's gcode templates reference.
1. Load two (or more) of the same material with the same color into the CFS.
2. In the slicer, choose the same materials and colors for these slots.
  <img width="659" height="410" alt="image" src="https://github.com/user-attachments/assets/7a129a63-0483-4023-952c-5842f753539c" /> \
3. When the first filament runs out of the CFS slot, you will see a red indicator. That's OK.
4. Then the filament runs out and you hear the CFS motor running for about 3 seconds. That's OK.
5. Scripts try to resove different tasks:
  - Minimize waste and keep printing (depends on pipe length variable) when filament in pipes. You can increase or decrease the waste by slightly decreasing or increasing the pipe length variable in the cfg. (The inverse relationship)
  - Refill on infills, not on perimeters (except vase mod). You can setup whitch line roles will need to excludes in cfg.
  - Keep refills with no gaps.
> [!NOTE]
> If autorefill fails (simply pause when filament runs out), reduce the pipe length variable.  

To start printing from the spool holder after using the CFS, follow these steps:
1. Open the Fluidd web interface.
2. Press the T17 button or type the T17 command into the console and press Enter (see screenshot below). The CFS filament will be unloaded. 
3. If you don't have a Y-splitter, disconnect the CFS tube and connect the spoolholder tube. 
4. Manually load filament from the spoolholder. 
5. Go to the filament tab in the printer screen. 
6. Set the right filament type for the spoolholder. 
7. Press the "Extrude" button. 
8. Push filament to the extruder for a better catch.

![изображение](https://github.com/user-attachments/assets/ba56b4d1-2272-4d52-b366-ec12b5d96024) 

To start printing from the CFS after the spool holder:
1. Open the Fluidd web interface.
2. Press the "T17" button or type "T17" into the console and press "Enter". The spool holder filament will be unloaded.
3. Manually retract the filament from the extruder and tubes.
4. If you do not have a Y-splitter, disconnect the spool holder tube and connect the CFS tube.

> [!WARNING]
> !!! DO NOT USE RETRACT BUTTON IN PRINTER SCREEN FOR UNLOADING FILAMENT!!! USE ONLY T17 FOR IT !!!

## Installation:

### Install these scripts to your K2

> [!NOTE]
> Before using main.cfg, please open it, read the comments on the user-defined section, set the desired values, save, and restart firmware.
> Before using tool.cfg, please open it, read the comments on the `[gcode_macro CHECK_REFILL]`, set the desired values, save, and restart firmware. 
> Also, there is an explanation of each virtual pins in the comments in main.cfg.

 1. Copy files from `/extras/` dir to you printer `/usr/share/klipper/klippy/extras/` via SSH (find the SSH password from touch UI > Cogwheel > General > Root account Information)
 2. Upload the `custom` directory of this repo to your printer using the Fluidd web interface.
 3. Edit your `printer.cfg`:
     1. Add after the `[includes ...]` block at the top:
        ```diff
        ...
         [include sensorless.cfg]
         [include gcode_macro.cfg]
         [include printer_params.cfg]
         [include box.cfg]
        +[include custom/main.cfg]
        +#if you upgrade you bed to R3MEN Graphite bed
        +[include custom/graphite_pre.cfg]

        ...
        ```
     1. Add a the bottom, just before the `SAVE_CONFIG` commented section:
        ```diff
        ...
        
        +[include custom/tool.cfg] # optional
        +[include custom/overrides.cfg]
        +#if you upgrade you bed to R3MEN Graphite bed
        +[include custom/graphite.cfg]

         #*# <---------------------- SAVE_CONFIG ---------------------->
         #*# DO NOT EDIT THIS BLOCK OR BELOW. The contents are auto-generated.
         ...
        ```

Note: `tool.cfg` is optional.

### Update your slicer settings

You need change some start g-codes in slicer. \
If you DO NOT use Tool.cfg:

  - Machine start g-code:
    ```
    START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single] CHAMBER_TEMP=[overall_chamber_temperature]
    ```

If you use Tool.cfg:
  - Machine start g-code:
    ```
    START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single] CHAMBER_TEMP=[overall_chamber_temperature]
    T[initial_no_support_extruder] TEMP=[first_layer_temperature] MAX_FLOWRATE=[filament_max_volumetric_speed] FILAMENT_TYPE=[filament_type] TYPES=[filament_type_0]|[filament_type_1]|[filament_type_2]|[filament_type_3] [filament_colour_0]|[filament_colour_1]|[filament_colour_2]|[filament_colour_3]
    ```

  - (Machine) Change filament g-code:
    ```diff
    G1 E-[old_retract_length] F2400
    G2 Z{z_after_toolchange + 0.4} I0.86 J0.86 P1 F10000 ; spiral lift a little from second lift
    G1 X10 Y350 F30000
    T[next_extruder] TEMP=[first_layer_temperature] MAX_FLOWRATE=[filament_max_volumetric_speed] FILAMENT_TYPE=[filament_type] TYPES=[filament_type_0]|[filament_type_1]|[filament_type_2]|[filament_type_3] [filament_colour_0]|[filament_colour_1]|[filament_colour_2]|[filament_colour_3]
    ```
  - (Machine) Change extrusion role g-code:
    ```
    CHECK_REFILL ROLE=[extrusion_role]
    ```
    
  - In Multimaterial tab in Printer settings you need to switch on *Manual Filament Change*
    ![изображение](https://github.com/user-attachments/assets/c69695b4-2daa-42a4-8690-5e2150cb7631)   

  - In Filament start and end g-codes remove all.
> [!WARNING]
> Keep all original G-code formatting, such as whitespace and line breaks!

## For developers:
Extraction of `box_wrapper.cpython-39.so` attributes here:  
https://docs.google.com/spreadsheets/d/16-dBGIGJ-zMNRc8hM-vnQLuDPJgmWSqQlyrfId-jeRs/edit?usp=sharing  

Extraction of `filament_rack_wrapper.cpython-39.so` attributes here:  
https://docs.google.com/spreadsheets/d/1BUP6k6tMjnTPiEdz6MP2wp-nE-Sxzs840_5d1FgZd7s/edit?usp=sharing  
