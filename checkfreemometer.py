from machine import Pin, PWM
import time
import machine, neopixel

# neopixels
neopixel_pin_num = 16
num_neopixels = 2
motor_pin_1_num = 18
motor_pin_2_num = 19
# The face servo moter control pin
servo_pin_num = 22


np = neopixel.NeoPixel(machine.Pin(neopixel_pin_num), num_neopixels)
# We could have grounded one of the DRV8833 inputs but instead hook this up as if it is a reversable motor
motor1a = Pin(motor_pin_1_num, Pin.OUT)
motor1b = Pin(motor_pin_2_num, Pin.OUT)

led = machine.Pin.board.LED
led.value(1)

print("show some pretty colors")
# fade in/out
for i in range(0, 4 * 256, 4):
    # set all pixels
    for j in range(num_neopixels):
        if (i // 256) % 2 == 0:
            val = i & 0xFF
        else:
            val = 255 - (i & 0xFF)
        np[j] = (val, 0, 255 - val)
    np.write()
    time.sleep_ms(10)

# clear
for i in range(num_neopixels):
    np[i] = (0, 0, 0)

np.write()

# go motor go - they need to be opposite values
print("Motor like a bat out of hell")
motor1a.value(0)
motor1b.value(1)
time.sleep(1)

# stop motor stop
print("Motor off")
motor1a.value(0)
motor1b.value(0)
time.sleep(1)

# lets try motor speed control with PWM
pwm1a = PWM(motor1b)
pwm1a.freq(10000)
print("Motor 10000/65000")
np[0] = (64, 0, 0)  # set to red, full brightness
np.write()
pwm1a.duty_u16(10000)  # out of 65000
time.sleep(1)
print("Motor 25000/65000")
np[0] = (64, 64, 0)  # set to red, full brightness
np.write()
pwm1a.duty_u16(25000)  # out of 65000
time.sleep(1)
print("Motor 45000/65000")
np[0] = (0, 64, 0)  # set to red, full brightness
np.write()
pwm1a.duty_u16(45000)  # out of 65000
time.sleep(1)
print("Motor 00000/65000")
np[0] = (0, 64, 64)  # set to red, full brightness
np.write()
pwm1a.duty_u16(00000)  # out of 65000
time.sleep(1)
pwm1a.deinit()
np[0] = (0, 0, 64)  # set to red, full brightness
np.write()
time.sleep(1)
np[0] = (0, 0, 0)  # set to red, full brightness
np.write()

# off
print("both leds off")
np[0] = (0, 0, 0)
np[1] = (0, 0, 0)
np.write()
time.sleep(1)

from servo import Servo

servo = Servo(Pin(servo_pin_num, Pin.OUT))
print("servo 0")
servo.write_angle(0)
time.sleep(1)
print("Servo 80")
servo.write_angle(80)
time.sleep(1)
print("servo 160")
servo.write_angle(160)
time.sleep(1)
servo.write_us(0)
