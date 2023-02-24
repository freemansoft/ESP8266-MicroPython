Freemometer test programs for various processors and peripheral configurations

This directory really belongs in another repository.  It is a hack that it is here for now :-()

## SH1106 Notes
This has been tested with the Inland IIC SPI OLED 128x64 display module that is configured for SPI.  The Inland may be an OEM module from KeyStudio because the product picture page showed a KeyStudio KS0056 silkscreen when I made my purchase. That module uses a SH1106 and can be SPI or I2C. Jumpers need to be moved to make it I2C.  There isn't any documentationa about how to do that.

The repository links to the most popular [MicroPython driver by robert-hh](https://github.com/robert-hh/SH1106) which is not yet in (micropython-lib)[https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/display]

## draw.io files
The `drawio` files can be viewed and edited with `draw.io` either the web version or local installation.

* `dials.io` Sample dials for the IKEA Dekad
* `freemometer_Pico.drawio` Schematic that expected by the Pico tests `check_fm_mp_pico.py`
* `freemometer_QTPY_esp32_s2.drawio` Schematic that expected by the Pico tests `check_fm_cp_qtpy_esp32_s2.py`
* `freemometer_Tiny2040.drawio`  Schematic that expected by the Pico tests `check_fm_mp_tiny2040.py`


## Steps - testing with the pico
Use the appropriate `check_fm` file

1. Open rshell
    ```
    rshell -p <com port>
    ```
1. Copy the necessary files over
    ```
    cp check_fm_mp_pico.py /pyboard
    cp SH1106/sh1106.py /pyboard
    ```
1. If you are going to exercise everything in the freemometer then you need `servo.py`
    ```
    cp ../servo.py /pyboard
    ```
1. Open the repl
    ```
    repl
    ```
1. Load the verification script
    ```
    from check_fm_mp_pico import *
    ```
1. verify the ssh1106 is working
    ```
    demo_sh1106()
    ```

### Checking out the RGBW Neopixels

```
import  check_fm_mp_pico
from check_fm_mp_pico import *
verify_neopixels_white_rgbw()
demo_neopixels_rgbw()

demo_servo()
demo_motor()

verify_neopixels_white_rgbw()

```