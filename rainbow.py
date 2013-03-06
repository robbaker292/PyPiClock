import RPi.GPIO as GPIO
import tubeFunctions
GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(17, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(18, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(21, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(22, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(23, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(24, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(10, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(9, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(25, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(11, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)

def toutput(tube, cathode, data):
	tubeFunctions.off()
	GPIO.output(25, False)

	#set tube addres

	if (tube & 1) == 1:
		GPIO.output(24, True)
	if (tube & 2) == 2:
		GPIO.output(10, True)
	if (tube & 4) == 4:
		GPIO.output(9, True)

	#set cathode

	if (cathode & 1) == 1:
		GPIO.output(18, True)
	if (cathode & 2) == 2:
		GPIO.output(21, True)
	if (cathode & 4) == 4:
		GPIO.output(22, True)
	if (cathode & 8) == 8:
		GPIO.output(23, True)

	#set data
	if (data & 1) ==1:
		GPIO.output(4, True)
	if (data & 2) == 2:
		GPIO.output(17, True)

	
	#clock
	GPIO.output(11, False)
	#time.sleep(1)
	GPIO.output(11, True)
	#time.sleep(1)
	GPIO.output(11, False)




