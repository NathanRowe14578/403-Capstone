import time
import serial
import csv


# The purpose of this code is to test whether or not the rover can be given instructions from a .csv file



ser = serial.Serial('/dev/serial0', 9600)

# Define a function to execute motor commands based on direction and time
def execute_command(direction, duration):

    if direction == "fwd":
        ser.write(b'\x7F\xE3')
        time.sleep(duration)
    elif direction == "back":
        ser.write(b'\x01\x00\x32\x00')
        time.sleep(duration)
    elif direction == "right":
        ser.write(b'\x00\x64')
        time.sleep(0.0088*duration)  # Calculate the time it takes to turn right by x degrees
    elif direction == "left":
        ser.write(b'\x02\x0A\x01\x0A')
        time.sleep(0.0088*duration)  # Calculate the time it takes to turn left by x degrees
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


