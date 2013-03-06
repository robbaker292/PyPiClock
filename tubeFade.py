import RPi.GPIO as GPIO
import time
import tubeFunctions
GPIO.setmode(GPIO.BCM)

GPIO.setup(11, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(4, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(17, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(18, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(21, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(22, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(23, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(24, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(10, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(25, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)

values = [1,2,3,4,5,6,7,9,13,18,25,32,37,41,46,52,57,63]

def output(data, red=False, blue=False, green=False):
	tubeFunctions.off()
	GPIO.output(25, True)

	#set colours
	if blue:
		GPIO.output(10, True)
	if green:
		GPIO.output(24, True)

	#set data
	if (data & 1) == 1:
		GPIO.output(4, True)
	if (data & 2) == 2:
		GPIO.output(17, True)
	if (data & 4) == 4:
		GPIO.output(18, True)
	if (data & 8) == 8:
		GPIO.output(21, True)
	if (data & 16) == 16:
		GPIO.output(22, True)
	if (data & 32) == 32:
		GPIO.output(23, True)
	
	#clock
	GPIO.output(11, False)
	GPIO.output(11, True)


while True:
	wait = 0.1
	longWait = 0.2

	output(red=True, data=0)
	output(green=True, data=63)
	output(blue=True, data=0)	

	i = 0
	while i < 18:
		output(red=True, data=values[i])
		#output(green=True, data=63-i)
		time.sleep(wait)
		i = i + 1

	time.sleep(longWait)
	
	i = 0
	while i < 18:
		output(red=True, data=63-values[i])
		#output(green=True, data=i)
		time.sleep(wait)
		i = i + 1

	time.sleep(longWait)
