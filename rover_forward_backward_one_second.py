import serial
import time


# The purpose of this file is to determine whether the rover can follow automated instructions

# Open a serial connection to the Sabertooth motor controller at 9600 baud
ser = serial.Serial('/dev/serial0', 9600)


# Move the motor forward for 1 second
ser.write(b'M1:10\r')  # Set motor 1 speed to 100%
ser.write(b'M2:10\r')  # Set motor 2 speed to 100%


time.sleep(1) # Wait for 1 second


ser.write(b'M1:20\r')  # Stop motor 1
ser.write(b'M2:20\r')  # Stop motor 2

time.sleep(2)
ser.close()

