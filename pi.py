import RPi.GPIO as GPIO
from time import sleep
from sys import exit
import os
from jenkins_status.Jenkins import Jenkins

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

tri = {"red":25, "green":24, "blue":18}
leds = {"event":{"red":23}, "tri":tri}
RED = 23
TRI_BLUE = 18
TRI_GREEN = 24
TRI_RED = 25

for led, colors in leds.items():
    for color, pin in colors.items():
        GPIO.setup(pin, GPIO.OUT)

def red_led(val):
    GPIO.output(RED,val)

def tri_led(led, r,g,b):
    GPIO.output(led["red"],  r)
    GPIO.output(led["blue"], g)
    GPIO.output(led["green"],b)

def set_led(name, color):
    led = leds[name]
    if color == "red":
        tri_led(led, 1,0,0)
    elif color == "green":
        tri_led(led, 0,1,0)
    elif color == "blue":
        tri_led(led, 0,0,1)
    elif color == "off":
        tri_led(led, 0,0,0)
    else:
        raise ValueError

def get_pins(led):
    for key,val in led.items():
        yield val

def get_led(name):
    return leds[name]

def blink(t):
    red_led(1)
    sleep(t)
    red_led(0)
    sleep(t)

def blink_loop(n = 8):
    for i in range(n):
        blink(0.1)

if __name__ == "__main__":
    jenkins = Jenkins(input_file = "/home/olehermanse/new_jobs.json", verbose = True)
    while True:
        sleep(1)
        if os.path.exists("/home/olehermanse/ready"):
            changes = jenkins.update()
            status = jenkins.get_job_status("testing-enterprise-pr")
            status = jenkins.get_job_status("bootstrap-community-nightly-master")
            if "blue" in status:
                set_led("tri", "blue")
            elif "red" in status:
                set_led("tri", "red")
            else:
                set_led("tri", "off")
            os.remove("/home/olehermanse/ready")
            if changes:
                jenkins.print_running_jobs()
                blink_loop()
