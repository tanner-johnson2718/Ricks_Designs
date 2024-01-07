# Z-Axis Upgrades

We made pretty signicant changes to the z-axis and thus we docment these changes here.

# Dual Z Firmware support

We run our Z-axis steppers and BL touch off the secondary MCU chamber. This so that each stepper motor has its own stepper driver. This allows each motor to be driven independatnly which gives us the ability to automatically sync the steppers and make sure the Z axis lead screws are at the same height. Below is the firmware config that must be added to the printer.cfg to enable this. We use the following physical connections:

* Z1 stepper -> chamber board X
* Z2 stepper -> chamber board Y
* White Wire BL Touch -> chamber board Z Stop PC2
* Black Wire BL Touch -> chamber board Z Stop Ground
* Red Wire BL Touch -> chamber board Z probe PA1
* Dark Red Wire BL Touch -> chamber board Z probe PWR
* Brown Wire BL Touch -> chamber board Z probe Ground

```
[bltouch]
sensor_pin: ^chamber_board:PC2
control_pin: chamber_board:PA1
x_offset: -44
y_offset: -5
z_offset: 2.46
speed: 3.0
pin_up_touch_mode_reports_triggered: False

# Z-stepper hooked up to chamber board x
[stepper_z]
step_pin: chamber_board:PB13
dir_pin: !chamber_board:PB12
enable_pin: !chamber_board:PB14
microsteps: 16
rotation_distance: 4
endstop_pin: probe:z_virtual_endstop
position_max: 350
position_min: 0.0
homing_speed: 10.0

[tmc2209 stepper_z]
uart_pin: chamber_board:PC11
tx_pin: chamber_board:PC10
uart_address: 0
run_current: 0.580
stealthchop_threshold: 999999

# Z-stepper hooked up to chamber board y

[stepper_z1]
step_pin: chamber_board:PB10
dir_pin: !chamber_board:PB2
enable_pin: !chamber_board:PB11
microsteps: 16
rotation_distance: 4
endstop_pin: probe:z_virtual_endstop

[tmc2209 stepper_z1]
uart_pin: chamber_board:PC11
tx_pin: chamber_board:PC10
uart_address: 2
run_current: 0.580
stealthchop_threshold: 999999
```

## Klipper Z-Tilt

# Physical Upgrades and Considerations

* POM Lead backlash nuts
* Top Z stabilizers
* Aligning Linear Couplers
