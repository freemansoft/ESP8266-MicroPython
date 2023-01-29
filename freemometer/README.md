
This directory really belongs in another repository.  It is a hack that it is here for now :-()

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