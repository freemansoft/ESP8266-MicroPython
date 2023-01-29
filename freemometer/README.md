
This directory really belongs in another repository.  It is a hack that it is here for now :-()

## SH1106 Notes
I'm playing with the Inland IIC ISP OLED 128x64 display module at the time of this note. This was origianlly built as the KeyStudio KS0056. That module is built SH1106.  It is configured as ISP.  Jumpers need to be moved to make it I2C and I don't know what those are so ISP it is.  

The repository links to the most popular [MicroPython driver by robert-hh](https://github.com/robert-hh/SH1106) which is not yet in (micropython-lib)[https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/display]

## Steps
1. Open rshell 
    ```
    rshell -p <com port>
    ```
1. Copy the necessary files over
    ```
    cp checkfreemometer.py /pyboard
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
    from checkfreemometer import *
    ```
1. verify the ssh1106 is working
    ```
    demo_sh1106()
    ```