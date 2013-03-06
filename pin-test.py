import RPi.GPIO as GPIO

#Set up GPIO channel as output
GPIO.setup(26, GPIO.OUT)

#op to pin 7
GPIO.output(26, False)


