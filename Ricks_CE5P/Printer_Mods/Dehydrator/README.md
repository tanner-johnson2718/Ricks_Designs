# Dehyrator

Here we describe our DIY filament dehydrator. The base design is a small off the shelf water tight tote big enough to house two spools and the heater and fans. Across the center of the box is a .5 inch PVC rod to act as a filament spool holder. In the middle is a 150W PTC heater with a fan heating the box. 4 4010 fans are used to evenly heat the box. A standard EPCOS 100K thermistor is placed directly at the output of the PTC heater to measure the heat output of the heater such that the heat added to the system is held constant. Note the thermistor is not an accurate measure of the heat of the box. Finally, Bowden couplers will be added to allow printing from dehydrator. Filament sponge holder and printed clamps to keep roll in place are possible add ons

# Firmware Additions

```
[mcu chamber_board]
serial: /dev/serial/by-id/usb-Klipper_stm32g0b1xx_46002A000B504B5735313920-if00

[heater_generic drier]
sensor_type: EPCOS 100K B57560G104F
sensor_pin: chamber_board:PA0
min_temp: 0
max_temp: 180
gcode_id: 2
control = pid
pid_kp = 72.312
pid_ki = 1.035
pid_kd = 1263.646
heater_pin: chamber_board:PC9

[heater_fan drier_fan]
pin: chamber_board:PB15
heater: drier
heater_temp: 10
fan_speed: 1.0

# generic temp probe for testing
[temperature_sensor test_sensor]
sensor_type: EPCOS 100K B57560G104F
sensor_pin: chamber_board:PC4
```

# Testing Results

* PID tuning
    * Target = 70
    * Kp = 22.651
    * Ki = 1.573
    * Kd = 81.545
* Max temp
    * Gets to 70 very quick with a ~10s cycle of off / on
    * At 80 it has a near constant duty cycle of 35%
    * At 90 constant duty cycle of 40%
    * At 100 constant duty cycle of 45%
    * ...
    * At 130 constant duty cycle of 55%
    * ...
* safety
    * Set max temp to 180 plus klippers built in safety mechanisms
    * Since the Thermistor is placed driectly at the outut of the heater, the temp set limits how hot the heater can get. This mitigates a run away heater being placed on a full duty cycle while we wait for the heat to reach the thermistor off in the corner
* Tempature correlation
    * Placed a thermistor at mid height in a filament roll
    * Appears that temp the filament feels is about 50% of the temp of the heater
    * This implies we need to up our max temp to 180 and set to 140 for a environment temp of 70.
    * At 150 Drier temp, the environ temp is around 65. **150 for PETg drying**.
* Idle timeout issues
    * To keep the heater from turning off we set the idle timeout to 14400 seconds or 4 hours. Ideally we would just have our filament heater ignore the idle status but thats difficult and the only potential downside is accidently wasting energy. All klipper saftey features are still in play:
        * 
```
[idle_timeout]
timeout: 14400
```