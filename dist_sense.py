import RPi.GPIO as GPIO
import time

# set up GPIO pins
TRIG_PIN = 18
ECHO_PIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# function to measure distance
def measure_distance(TRIG_PIN, ECHO_PIN):
    # send a pulse to the sensor
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # measure the time it takes for the pulse to bounce back
    start_time = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        if time.time() - start_time > 0.1:
            return -1
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        if time.time() - start_time > 0.1:
            return -1
        pulse_end = time.time()

    # calculate distance in inches
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 13503.9
    distance = round(distance, 2)

    return distance

    
    
while True:
    distance = measure_distance(18, 24)
    if distance > 0 and distance <100:
        print("Object detected at ", distance, " cm")
    else:
        print("Closest object at", distance, " cm")
    time.sleep(0.1)