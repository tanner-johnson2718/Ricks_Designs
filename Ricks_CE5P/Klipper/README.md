# Klipper

Klipper is used as the firmware to drive the 3D printer. It runs as a set of services on a Laptop and controls the 3D printer mainboard(s) via usb serial communication. Moonraker is used as a service to expose network APIs for the klipper firmware to a control GUI, in this case mainsail. We will set up one singular klipper instance on the Dell GPP that will drive our printer. Our Klipper instance will be set up as followed:

| Klipper Instance | MoonRaker IP | MoonRaker Port | Data Dir | Service(s) | Serial Device | 
| --- | --- | --- | --- | --- | --- |
| CE5P | 127.0.0.1 | 7125 | ~/CE5P_data/ |  klipper-CE5P.service, moonraker-CE5P.service | **Printer MCU** /dev/serial/by-id/usb-Klipper_stm32g0b1xx_190035000F50415833323520-if00       **Chamber MCU** usb-Klipper_stm32g0b1xx_46002A000B504B5735313920-if00 |

We will also set up Mainsail on the host device and have it run completely locally i.e. the only place to access the mainsail gui is on the Dell GPP laptop. Mainsial will be accessed via the browser at the local loop back ip: `127.0.0.1` or `ce5p.local` if host name is configed as shown below.

# Installation

Some key locations of files that will be created and edited during the installation process. This installation process shall be used on the Dell GPP or whatever system is running the klipper instances.

| Important Artifact | Location | Comment |
| --- | --- | --- |
| Klipper Instance Local Install | ~/CEP_data | Used to store local configs per klipper instance |
| printer.cfg | ~/CEP_data/config | The firware config file used to configure firmware running the printer. See [here](https://www.klipper3d.org/Config_Reference.html) |
| moonraker.conf | ~/CE5P_data/config | Containts configuration for moonraker. Specifically houses the IP to bind too. See [here](https://moonraker.readthedocs.io/en/latest/configuration/) |
| mainsail.cfg | ~/CE5P_data/config | Mainsail config. Mostly used to change the search directory for gcode files mainsail uses |
| Systemd service env files | ~/CE5P_data/sytemd | Contains the .env files that configure and are used to run the klipper and moonraker services. |
| G-Code Search DIR | ~/CE5P_data/gcodes | - |
| Systemd services def | ~/etc/systemd/system | Contains the `klipper-CE5P.service` and `moonraker-CE5P.service` service def files |
| Start up service | ~/etc/systmd/system/multi-user.target.wants/ | Sym links to serice def files to be ran on start up. Should have link to our service files, `klipper-CE5P.service` and `moonraker-CE5P.service` |


## Laptop Set up
* git clone https://github.com/th33xitus/KIAUH
* cd KIAUH/
* ./kiauh.sh
* Select install then install klipper w/ 1 instance `CE5P`
* Install Moonraker (1 instance `CE5P`)
* Install mainsail`CE5P`
    * change `~/CE5P_data/config/moonraker.conf` so that the `host` attribute under `[server]` is `127.0.0.1`
* **NOTE** Installs outputs to `~/`
* Also can use kiauh to set local host name to `ce5p` this will allow the user to open mainsail with `ce5p.local` as the domain name.
* Create Firefox Profile and Boot at start up:
    * `firefox -ProfileManager`
    * Use gui to create a profile called `firefox_profile` in the `CE5P_data` dir.
        * Create firefox profile at `~/CE5P_data/<rand_sig>.firefox_profile
    * `xulustore.json` in firefox profile dir contains the screen info. Which should have entires:
        * `"width":"1920"`
        * `"height":"1080"`
        * `"sizemode":"fullscreen"`
    * While in firefox in full screen, do not exit fullscreen or re-enter fullscreen before exiting
    * Launch mainsail w/ `firefox -P firefox_profile ce5p.local`
    * Make launch script to run firefox at boot
        * `echo 'firefox -P firefox_profile ce5p.local' > ~/CE5P_data/CE5P_gui_launch.sh`
        * `chmod +x ~/CE5P_data/CE5P_gui_launch.sh`
        * Copy to desktop to be opened when system boots.

### Klipper CFG Updates
To update the klipper config, first make sure this repo is intalled in the home diretory of the user hosting the klipper servies. Create an update script as shwon below and place it on the desktop.

```
cd ~/3D_ToolChain
git pull
cp ./Klipper/printer.cfg ~/CE5P_data/config/printer.cfg
```

## Firmware Set up
* Use as guide: https://www.klipper3d.org/Installation.html.
* Used https://github.com/Klipper3d/klipper/blob/master/config/generic-bigtreetech-skr-mini-e3-v3.0.cfg as an intial template
* Updated Endstops and other physical stepper parameters using https://github.com/Klipper3d/klipper/blob/master/config/printer-creality-ender5plus-2019.cfg
* Copied BL touch, safe z home, and mesh leveling fields over as well
    * Updated pins for BLtouch) sensor_pin: ^PC2 and control_pin: PA1
    * Updated heater bed sensor type to EPCOS 100K B57560G104F
    * x_offset: -44, y_offset: -5, z_offset: -2.37
    * Heatbreak fan -> PB15
    * fan -> PC6
    * serial: /dev/serial/by-id/usb-Klipper_stm32g0b1xx_190035000F50415833323520-if00
    * Invert Z-axis pin 0> dir_pin: !PC5
* To build:
    * cd ~/klipper/
    * make menuconfig
    * Set STM32G0B1 with a "8KiB bootloader" and USB communication.
    * Save and exit
    * make
    * copy out/klipper.bin to SD and rename firmware.bin
    * Insert and power on SKR. Veryify file is renamed FIRMWARE.CUR
* The configuration file [printer.cfg](printer.cfg) is stored under the data directory for the given printer and replaces Marlins Firmware settings.
    * When making changes to this, restart the associated klipper service for changes to be uploaded

## Mainsail
* Creates config folder at ~/mainsail-config
* in printer.cfg add `[include mainsail.cfg]`
* Gcode folder is under ~/printer.../gcodes

# GCODE and Commands

Klipper only supports a basic set of Gcode commands. These are:

* Move: G0 and G1
* Dwell: G4 P<milliseconds>
* Move to origin: G28 [X] [Y] [Z]
* Turn off motors: M18 or M84
* Wait for current moves to finish: M400
* Use absolute/relative distances for extrusion: M82, M83
* Use absolute/relative coordinates: G90, G91
* Set position: G92 [X<pos>] [Y<pos>] [Z<pos>] [E<pos>]
* Set speed factor override percentage: M220 S<percent>
* Set extrude factor override percentage: M221 S<percent>
* Set acceleration: M204 S<value> OR M204 P<value> T<value>
    * Note: If S is not specified and both P and T are specified, then the acceleration is set to the minimum of P and T. If only one of P or T is specified, the command has no effect.
* Get extruder temperature: M105
* Set extruder temperature: M104 [T<index>] [S<temperature>]
* Set extruder temperature and wait: M109 [T<index>] S<temperature>
    * Note: M109 always waits for temperature to settle at requested value
* Set bed temperature: M140 [S<temperature>]
* Set bed temperature and wait: M190 S<temperature>
    * Note: M190 always waits for temperature to settle at requested value
* Set fan speed: M106 S<value>
* Turn fan off: M107
* Emergency stop: M112
* Get current position: M114
* Get firmware version: M115

For complicated GCODE, klipper perfers human readable commands. All can be found [here](https://www.klipper3d.org/G-Codes.html#additional-commands).

# Macros

* https://www.klipper3d.org/Command_Templates.html
* https://github.com/jschuh/klipper-macros
* See [README.md](../Calibration_Test_Prints/README.md) for currently implemented ones.
* Macros are placed in the printer.cfg file