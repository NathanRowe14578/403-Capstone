import time
import serial
import csv
import RPi.GPIO as GPIO
# The purpose of this code is to test whether or not the rover can be given instructions from a .csv file
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)#front left
GPIO.setup(17, GPIO.OUT)#front middle
GPIO.setup(27, GPIO.OUT)#front right
GPIO.setup(22, GPIO.OUT)#left front
GPIO.setup(5, GPIO.OUT)#left back
GPIO.setup(6, GPIO.OUT)#right front
GPIO.setup(13, GPIO.OUT)#right back
GPIO.setup(19, GPIO.OUT)#back middle

GPIO.setup(18, GPIO.IN)#Front left
GPIO.setup(23, GPIO.IN)#front Middle
GPIO.setup(24, GPIO.IN)#Front Right
GPIO.setup(25, GPIO.IN)#Left Front
GPIO.setup(12, GPIO.IN)#Left Back
GPIO.setup(16, GPIO.IN)#Right Front
GPIO.setup(20, GPIO.IN)#Right Back
GPIO.setup(21, GPIO.IN)#Back middle


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

ser = serial.Serial('/dev/serial0', 9600)

def avoidF(distanceFL, distanceFM, distanceFR):
    if distanceFL > distanceFR:
        execute_command(left, 90)
        execute_command(fwd, 1)
        execute_command(right, 90)
        execute_command(fwd,2)
        execute_command(right, 90)
        execute_command(fwd, 1)
        execute_command(left, 90)
    elif distanceFL < distanceFR:
        execute_command(right, 90)
        execute_command(fwd, 1)
        execute_command(left, 90)
        execute_command(fwd,2)
        execute_command(left, 90)
        execute_command(fwd, 1)
        execute_command(right, 90)
    else:
        print("cannot move forward, please pick up")
    
    
# Define a function to execute motor commands based on direction and time
def execute_command(direction, duration):

    if direction == "fwd":
        ser.write(b'\x7F\xE3')
        x=duration
        while duration > 0:
            distanceFL = measure_distance(4, 18)
            distanceFM = measure_distance(17, 23)
            distanceFR = measure_distance(27, 24)
            if distanceFL or distanceFM or distanceFR < 50:
            if distanceFM < 50:
                ser.write(b'\x00\x00')
                print("Object detected within operation: forwards")
                avoidF(distanceFL, distanceFM, distanceFR)
            time.sleep(0.1)
            duration -= 0.1
        
    elif direction == "back":
        ser.write(b'\x01\x00\x32\x00')
        x=duration
        while duration > 0:
            distanceBM = measure_distance(19, 21)#use different gpio pins for back
            if distanceBM < 50:
                ser.write(b'\x00\x00')
                print("Object detected within operation: backwards")
            duration -= 0.1
            time.sleep(0.1)
    elif direction == "right":
        ser.write(b'\x00\x64')
        duration = 0.0088*duration  # Calculate the time it takes to turn right by x degrees
        x=duration
        while duration > 0:
            distanceRF = measure_distance(6, 16)
            distanceRB = measure_distance(13, 20)
            if distanceRF or distanceRB < 50:
                ser.write(b'\x00\x00')
                print("Object detected within operation: turn right")
            duration -= 0.1
            time.sleep(0.1)
    elif direction == "left":
        ser.write(b'\x02\x0A\x01\x0A')
        duration = 0.0088*duration  # Calculate the time it takes to turn left by x degrees
        x=duration
        while duration > 0:
            distanceLF = measure_distance(22, 25)
            distanceLB = measure_distance(5, 12)
            if distanceLF or distanceLB < 50:
                ser.write(b'\x00\x00')
                print("Object detected within operation: turn left")
            duration -= 0.1
            time.sleep(0.1)
    else:
        print("Invalid direction command: {}".format(direction))

#Open the CSV file and read each line
with open('instruction.csv') as csvfile:
       reader = csv.reader(csvfile)
       for row in reader:
           direction = row[0]
           duration = int(row[1])
           execute_command(direction, duration)

# Stop the motors and close the serial connection
##ser.write(b'\x02\x0A\x02\xB4')
##ser.write(b'\x00\x64')#motors run in opposite directions
##ser.write(b'\x7F\xE3')#both forward
##ser.write(b'\x01\x00\x32\x00')##backwards
##ser.write(b'\x01\x00\x10\x00')
##time.sleep(3)
ser.write(b'\x00\x00')#stop
ser.close()


