
import RPi.GPIO as GPIO
import time
import tubeFunctions
import rainbow
import datetime
import updateTime

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
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#values = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,17,19,21,23,25,27,29,31,34,37,40,43,46,50,54,58,62]

#Gaps of 1, 2, 4, 8
values = 	[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,
		34,36,38,40,42,44,46,48,50,52,54,56,60,62,64,
		68,72,76,80,84,88,92,96,100,104,108,112,116,120,124,128,
		136,144,152,160,168,176,184,192,200,208,216,224,232,240,248,255]



longwait = 0.2
fadeWait = 0.006
it = len(values)
tube = 0
digit = 0
mode = 0
ct = 0
colon = False

HourLsb =13
HourMsb =13
MinLsb =13
MinMsb =13
SecLsb =13
SecMsb =13
oldHourLsb =12
oldHourMsb =12
oldMinLsb =12
oldMinMsb =12
oldSecLsb =12
oldSecMsb =12

onoffmode = 1

# 0 is sleep
# 1 is power up
# 2 is run
# 3 is power down

duration = 30
FirstTime = True

# **** Get the time ******
updateTime.updateTime()



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


# Switch all tubes off
for t in range(6):
	for d in range(10):
		rainbow.toutput(t, d, 0)

 

output(red=True, data=0)
output(green=True, data=0)
output(blue=True, data=0)	
	
endTime = datetime.datetime.now() + datetime.timedelta(minutes=duration)

while True:

	if (onoffmode == 0):
		#************************* Sleep Mode ***************************************
		while GPIO.input(7) == 1:
			output(red=True, data=0)
			output(blue=True, data=0)
			output(green=True, data=0)
			
		endTime = datetime.datetime.now() + datetime.timedelta(minutes=duration)		

		onoffmode = 1
		#************************* End Sleep Mode ***********************************



	if (onoffmode == 1):
		#************************* Power Up Mode ************************************
		# Switch on HVPS
#		rainbow.toutput(0, 10, 3)

		mode =0
		ct=0

		# Cycle through digits
		offdigit = 9
		for digit in range(10):
			for tube in range(6):
				rainbow.toutput(tube, digit, 3)
				rainbow.toutput(tube, offdigit, 0)
			time.sleep(0.3)	
			offdigit = digit	
		
		for tube in range(6):
			rainbow.toutput(tube, 9, 0)

		updateTime.updateTime()
 
		FirstTime=True
		output(red=True, data=255)

		onoffmode = 2
		#************************* End Power Up *************************************



	if (onoffmode == 2):
		#************************** Run Mode Main Loop *******************************

		#******** Wait for next tick ************************************

		currentTime= datetime.datetime.now()

		while (currentTime.microsecond > 5000):
			currentTime= datetime.datetime.now()
			# Check for movement
			if (GPIO.input(7) == 0):
				endTime = datetime.datetime.now() + datetime.timedelta(minutes=duration)
					


		#******************** LEDs ***************************************


		#***** Red fading down, Green fading up ************
	#	if (mode==0):
	#		if (ct < it):
	#			output(red=True, data=values[(it-1)-ct])
	#			output(green=True, data=values[ct])
	#			ct = ct + 1
	#		else:
	#			ct = 0
	#			mode = 1

		#***** Green fading up ******************
		if (mode==0):
			if (ct < it):
				output(green=True, data=values[ct])
				ct = ct + 1
			else:
				ct = 0
				mode = 10

		#**** Red fading down *******
		if (mode==10):
			if (ct < it):
				output(red=True, data=values[(it-1)-ct])
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

		# Set PWM Fader to zero
		output(fader=True, data=0)

		# split out hour
		oldHourLsb = HourLsb
		oldHourMsb = HourMsb
		hour = currentTime.hour
		HourLsb = hour %10
		HourMsb = hour /10

		# split out minutes
		oldMinLsb = MinLsb
		oldMinMsb = MinMsb
		minute = currentTime.minute
		MinLsb = minute %10
		MinMsb = minute /10

		# split out seconds
		oldSecLsb = SecLsb
		oldSecMsb = SecMsb
		second = currentTime.second
		SecLsb = second %10
		SecMsb = second /10
	
		if (FirstTime):
			FirstTime = False
			oldHourLsb=12
			oldHourMsb=12
			oldMinLsb=12
			oldMinMsb=12
			oldSecLsb=12
			oldSecMsb=12	

		#** Wire up digits to the fader **
		if (oldHourMsb != HourMsb):
			rainbow.toutput(5, oldHourMsb, 2)
			rainbow.toutput(5, HourMsb, 1)

		if (oldHourLsb != HourLsb):
			rainbow.toutput(4, oldHourLsb, 2)
			rainbow.toutput(4, HourLsb, 1)

		if (oldMinMsb != MinMsb):
			rainbow.toutput(3, oldMinMsb, 2)
			rainbow.toutput(3, MinMsb, 1)

		if (oldMinLsb != MinLsb):
			rainbow.toutput(2, oldMinLsb, 2)
			rainbow.toutput(2, MinLsb, 1)

		if (oldSecMsb != SecMsb):
			rainbow.toutput(1, oldSecMsb, 2)
			rainbow.toutput(1, SecMsb, 1)

		if (oldSecLsb != SecLsb):
			rainbow.toutput(0, oldSecLsb, 2)
			rainbow.toutput(0, SecLsb, 1)
 
		#** Fade Digits ***
		z=0
		while z<it:
			output(fader=True, data=values[z])
			time.sleep(fadeWait)
			z = z + 1

		#** Hard Wire Digits on or off ***
		if (oldHourMsb != HourMsb):
			rainbow.toutput(5, oldHourMsb, 0)
			rainbow.toutput(5, HourMsb, 3)

		if (oldHourLsb != HourLsb):
			rainbow.toutput(4, oldHourLsb, 0)
			rainbow.toutput(4, HourLsb, 3)

		if (oldMinMsb != MinMsb):
			rainbow.toutput(3, oldMinMsb, 0)
			rainbow.toutput(3, MinMsb, 3)

		if (oldMinLsb != MinLsb):
			rainbow.toutput(2, oldMinLsb, 0)
			rainbow.toutput(2, MinLsb, 3)

		if (oldSecMsb != SecMsb):
			rainbow.toutput(1, oldSecMsb, 0)
			rainbow.toutput(1, SecMsb, 3)

		if (oldSecLsb != SecLsb):
			rainbow.toutput(0, oldSecLsb, 0)
			rainbow.toutput(0, SecLsb, 3)
	

		# Ensure unused digits really are off

		for digit in range(10):
			if (digit != HourMsb):
				rainbow.toutput(5, digit, 0)
			else:
				rainbow.toutput(5, digit, 3)


			if (digit != HourLsb):
				rainbow.toutput(4, digit, 0)
			else:
				rainbow.toutput(4, digit, 3)


			if (digit != MinMsb):
				rainbow.toutput(3, digit, 0)
			else:
				rainbow.toutput(3, digit, 3)


			if (digit != MinLsb):
				rainbow.toutput(2, digit, 0)
			else:
				rainbow.toutput(2, digit, 3)


			if (digit != SecMsb):
				rainbow.toutput(1, digit, 0)
			else:
				rainbow.toutput(1, digit, 3)


			if (digit != SecLsb):
				rainbow.toutput(0, digit, 0)
			else:
				rainbow.toutput(0, digit, 3)



		
		#************* Colons **************

		if (colon == True):
			rainbow.toutput(1, 10, 0)
			rainbow.toutput(2, 10, 0)
			rainbow.toutput(3, 10, 0)
			rainbow.toutput(4, 10, 0)
			colon = False
		else:
			rainbow.toutput(1, 10, 3)
			rainbow.toutput(2, 10, 3)
			rainbow.toutput(3, 10, 3)
			rainbow.toutput(4, 10, 3)
			colon = True

		# Check for Motion
#		if (GPIO.input(7) == 0):
#			endTime = datetime.datetime.now() + datetime.timedelta(minutes=duration)
#			print "Event "

		# Check for Time Out
		if currentTime > endTime:
			onoffmode = 3


		#********************** End of Run Mode *************************************



	if (onoffmode == 3):
		#********************** Power Down Mode ************************************
		# HVPS off
#		rainbow.toutput(0, 10, 0)

		# tubes off
		for tube in range(6):
			for digit in range(10):
				rainbow.toutput(tube, digit, 0)

		# Neons off
		for tube in range(4):
			rainbow.toutput(tube+1, 10, 0)

		# LEDs off
		output(red=True, data=0)
		output(green=True, data=0)
		output(blue=True, data=0)
		
		onoffmode = 0
		#********************** End Power Down *************************************
		
