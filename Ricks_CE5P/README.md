# Ricks CE5P (Custom Ender 5 Plus)

**ABANDONED** We have thrown this project to the quantum way side. Its parts will be used in future projects. More importantly its lessons learned will forever charished and applied in ever increasingly cool projects.

Ricks CE5P, the best ender 5 plus in the central finite curve. This repo will contain the config, docs, and scripts for a CE5P. The goal is to get a printer capable and specializing in Engineering filaments such as Nylon, PC, PP, and more. A secondary goal is a 3D printer testbed. Modifications should not only move the printer towards higher perfomance measured by ability to print these galactic filaments from the multiverse, but also add degrees of modularity so that we can quickly test and experiment with various 3D printer settings, parts, etc.

## Firmware Versions Used

* Kiauh for managing klipper installation
    * Klipper    v0.11.0
    * Moonraker  v0.8.0
    * Mainsail   v2.6.0

## Modifications, Current Hardware, and project directory

### Modifications and Project Directory

| Project Component | Comment |
| --- | --- |
|  [Slicer Settings, Calibration, and Test Prints](Calibration_Test_Prints) | Holds documentation on settings/configurations (both firmware and slicer settings). Also has test prints and procedures for calibrating the printer. |
| [Electronics Enclosure](Printer_Mods/Electronic_Enclosure) | Custom electronics enclosure to support printer customization and additional components. Contains the CAD files for electronics housing and doc on how all the electronics are assembled and physically conntected  |
| :heavy_check_mark: [Klipper and GPP](Klipper) | Using Klipper firmware w/ moonraker and mainsail. Klipper is installed on both the printer MCU and a general purpose computer that runs the MCU. Here lies the doc for installing and cofiguring this set up |
| :heavy_check_mark: [Designs](Designs) | FreeCad Scripts and generic designs, images, and models used for 3D printing and likely to be used in more than a singular project. Also contains misc. 3D printed projects that are not big enough to get their own repo. |
| :heavy_check_mark: [Z-Axis Upgrades](./Printer_Mods/Z-Axis/) | Dual Z stepper drivers on second board, upgraded lead screws, Z-stabilizers, and Z-tilt auto leveling | 
| :heavy_check_mark: [Cable Track Wire Management System](Printer_Mods/Cable_Track) | [Stole from Reddit](https://www.reddit.com/r/ender5plus/comments/so2ulf/ender_5_plus_cable_chain_solution/) |
| :heavy_check_mark: [Linear Rail Conversion Kit](Printer_Mods/Linear%20Rails/)  | [Thingiverse](https://www.thingiverse.com/thing:3960105) |
| :x: [MEME Controller](MEME_CTLR) | G code sender, print monitor, and general controller / interface for whole printer and peripherals. **DEPRICATED**, Klipper implemented many features this was going to have.  |
| :x: [Filament Dehydrator](Printer_Mods/Dehydrator/) | DIY filament dehydrator. 150W PTC heater placed in a dry box. Chamber MCU cotrols the heater and fans in the box. 3D printed housing and mounts to hold heater, fans and filament spools. **DEPRICATED**, Heat didn't distribute well enough. This required setting the PTC heater to a very high temp whih melted the PVC spool holder. Will convert to a dry box not activatly heated, add the bowden tube couplers and make it dry box that you can print from. Will purchase a filament drier. |  


### Current Hardware
| Component | Date Installed | Comment |
| --- | --- | --- |
| MCU Main (Printer) | Jan 2023 | SKR Mini E3 V3. [Pinout](DataSheets/BTT%20E3%20SKR%20MINI%20V3.0_PIN.3D_ToolChainpdf). [MCU](DataSheets/stm32g0b1cc-2042221.pdf) |
| MCU Secondary (Chamber) | Jan 2023 | SKR Mini E3 V3. [Pinout](DataSheets/BTT%20E3%20SKR%20MINI%20V3.0_PIN.pdf). [Block Diagram](DataSheets/BTT%20E3%20SKR%20MINI%20V3.0_SCH.pdf). [MCU](DataSheets/stm32g0b1cc-2042221.pdf) |
| GPP | June 2023 | Random Dell Latitude 7350 laptop to host klipper and the multiple MCUs on the system. Acts as touch screen tablet interface. |
| PSU | - | [Stock Meanwell RSP-500-24](DataSheets/MeanWell_500_Datasheet.pdf) |
| Extruder | Sept 2022 | Creality All metal Extruder https://www.amazon.com/dp/B07ZMFP2L8?psc=1&ref=ppx_yo2ov_dt_b_product_details |
| Steppers | - | Stock |
| Bowden Tube | Sept 2022 | Capicorn XS https://www.captubes.com |
| Base Hot end | Nov 2022 | Micro Swiss All metal hot end https://store.micro-swiss.com/collections/all-metal-hotend-kits/products/all-metal-hotend-kit-for-cr-10 |
| Hot end Thermistor | Jan 2023 | https://www.amazon.com/dp/B0714MR5BC?psc=1&ref=ppx_yo2ov_dt_b_product_details. Has JST quick Connect. |
| Heater Cartridge | - | Stock 40W, Adding standard 20 AWG quick connects to make changing hotend faster. |
| Hot end fan and part cooler | Jan 2023 | https://www.amazon.com/gp/product/B08N8YDQCD/ref=ppx_yo_dt_b_asin_title_o00_s01?ie=UTF8&psc=1. Adding JST male and female at hot end. |
| Hot end fan shroud | Jan 2023 | [Fan Shroud](Printer_Mods/EB_FAN_SHROUD_20200523.stl) | 
| External Bed Mosfett | Nov 2022 | Mosfet FYSETC https://www.amazon.com/dp/B07C4PGXFK?psc=1&ref=ppx_yo2ov_dt_b_product_details |
| Part Cooler | - | Stock |
| ABL | - | Stock BL Touch |
| X Gantry (Adding Linear Rails and adapter plate [here](Printer_Mods/Linear%20Rails/)) | Feb 2023 | MGN 450mm Linear rail mounted on stock X gantry |
| Y Guides | - | Stock |
| [Z Axis](./Printer_Mods/Z-Axis/) | Sept 2022 | Stock w/ Z axis POM Lead nut and spring https://www.amazon.com/dp/B07XYR3F4C?psc=1&ref=ppx_yo2ov_dt_b_product_details. Also use second MCU to drive each Z stepper independatly. Z-axis stabilizers |

## TODO
* Finish Z axis doc
* Dual printer enclosure
* Dehydrator (buy)
* GPP:
    * Gcode file points to USB
    * Make a docking station for Dell Laptop
* Power / Wiring
    * 2nd PSU
    * Full Enclosure
    * Finish electronics enclosure
    * Rewire and clean wiring
    * Add Full wire diagram
    * Have end connectors documented for Board to end componetent pieces
    * Better Wire Trays
* General Upgrades
    * Y Linear rails
    * v6 for ender? 
    * hermit crab?
    * New Build Plate
    * new POM lead screws
    * Z-stabalizers
    * Filament sponges