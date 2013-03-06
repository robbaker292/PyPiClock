import RPi.GPIO as GPIO
import time
import tubeFunctions
import rainbow
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
GPIO.setup(9, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(8, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)

#values = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,17,19,21,23,25,27,29,31,34,37,40,43,46,50,54,58,62]

#Gaps of 1, 2, 4, 8
values = 	[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,
		34,36,38,40,42,44,46,48,50,52,54,56,60,62,64,
		68,72,76,80,84,88,92,96,100,104,108,112,116,120,124,128,
		136,144,152,160,168,176,184,192,200,208,216,224,232,240,248,255]

longwait = 0.48
it = len(values)
tube = 0
digit = 0
mode = 0
ct = 0
colon = False

def output(data, red=False, blue=False, green=False, fader=False):
	tubeFunctions.off()
	GPIO.output(25, True)

	#set colours
	if red:
		GPIO.output(10, False)
		GPIO.output(24, False)
	if blue:
		GPIO.output(10, True)
		GPIO.output(24, False)
	if green:
		GPIO.output(10, False)
		GPIO.output(24, True)
	if fader:
		GPIO.output(10, True)
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
	if (data & 64) == 64:
		GPIO.output(9,True)
	if (data & 128) == 128:
		GPIO.output(8,True)
	

	#clock
	GPIO.output(11, True)
	GPIO.output(11, False)

#print "here"

 

output(red=True, data=0)
output(green=True, data=0)
output(blue=True, data=0)	
	

while True:

#************************** Main Loop *******************************

	time.sleep(longwait)

	#***** Red fading down, Green fading up ************
	if (mode==0):
		if (ct < it):
			output(red=True, data=values[(it-1)-ct])
			output(green=True, data=values[ct])
			ct = ct + 1
		else:
			ct = 0
			mode = 1

	#***** Green fading down, Blue fading up **********
	if (mode==1):
		if (ct < it):
			output(blue=True, data=values[ct])
			output(green=True, data=values[(it-1)-ct])
			ct = ct + 1
		else:
			ct = 0
			mode = 2
		
	#***** Blue stays on and Red fades up **************
	if (mode==2):
		if (ct < it):
			output(red=True, data=values[ct])
			ct = ct +1
		else:
			ct = 0
			mode = 3
	
		#**** Red stays on and Blue fades out *************
	if (mode==3):
		if (ct < it):
			output(blue=True, data=values[(it-1)-ct])
			ct = ct + 1
		else:
			ct = 0
			mode = 0


	#*********** Tubes ************
	offdigit = digit-1
	if (digit == 0):
		offdigit = 9

	output(fader=True, data=0)
	rainbow.toutput(tube, offdigit, 2)
	rainbow.toutput(tube, digit, 1)
	z=0
	while z<256:
		output(fader=True, data=z)
		time.sleep(0.002)
		z = z + 1

	rainbow.toutput(tube, offdigit, 0)
	rainbow.toutput(tube, digit, 3)
	tube = tube + 1
	if (tube == 6):
		tube = 0
		digit = digit + 1
		if (digit == 10):
			digit = 0
		
#************* Colons **************

	if (colon == True):
		rainbow.toutput(1, 10, 0)
		rainbow.toutput(2, 10, 0)
		rainbow.toutput(3, 10, 0)
		rainbow.toutput(4, 10, 0)
#		rainbow.toutput(5, 10, 0)
		colon = False
	else:
		rainbow.toutput(1, 10, 3)
		rainbow.toutput(2, 10, 3)
		rainbow.toutput(3, 10, 3)
		rainbow.toutput(4, 10, 3)
#		rainbow.toutput(5, 10, 3)
		colon = True		
