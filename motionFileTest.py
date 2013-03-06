import RPi.GPIO as GPIO
import time
from datetime import datetime
import tubeFunctions

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

tubeFunctions.off()

while True:
	if GPIO.input(25) == 0:
		now = str(datetime.now())
		print now
		tubeFunctions.ld(0.1,1)
		tubeFunctions.off()	
		f = open('motionLog','a')
		f.write(now + "\n")
		f.close
		time.sleep(30)
