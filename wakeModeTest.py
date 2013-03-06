import RPi.GPIO as GPIO
import time
import datetime
import tubeFunctions
import updateTime

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

tubeFunctions.off()
tubeFunctions.ledStatus(False)

#set the end time for wakemode
endTime = datetime.datetime.now()

#wake mode duration in minutes
duration = 20

#enters wake Mode. Cycles through digits until time expires or more movement is detected
def wakeMode():
	global endTime
	global duration
	#adjust end time
	endTime = datetime.datetime.now() + datetime.timedelta(minutes=duration)
	
	#print "wakemode entered. Now:",datetime.datetime.now()," Endtime:",endTime
	while datetime.datetime.now() < endTime:
		tubeFunctions.ledStatus(True)
		loopDigits(1,1)
	
	tubeFunctions.ledStatus(False)
	tubeFunctions.off()
	#print "leaving wakemode. Time is now",datetime.datetime.now()
	updateTime.updateTime()


#Loop through all digits in order with wait gap between digits & for iteration number times. Also checks if movement occurs during cycling
def loopDigits(wait, iterations):
	i= 0
	global endTime
	global duration
	while i < iterations:
		for n in range(10):
			#tubeFunctions.outputDigit(n)
			if GPIO.input(25) == 0:
				endTime = datetime.datetime.now() + datetime.timedelta(minutes=duration)
				#print "endTime is now",endTime
			#time.sleep(wait)
			nextSecond = datetime.datetime.now() + datetime.timedelta(seconds=1)
			while datetime.datetime.now() < nextSecond:
				currentTime = datetime.datetime.now()
				hour = currentTime.hour
				hourMsb = hour / 10
				hourLsb = hour % 10				
				tubeFunctions.outputDigit(hourMsb)
				time.sleep(0.25)
				tubeFunctions.off()
				time.sleep(0.1)
				tubeFunctions.outputDigit(hourLsb)
				time.sleep(0.25)
				tubeFunctions.off()
				time.sleep(0.25)
				min = currentTime.minute
				minMsb = min / 10
				minLsb = min % 10
				tubeFunctions.outputDigit(minMsb)
				time.sleep(0.25)
				tubeFunctions.off()
				time.sleep(0.1)
				tubeFunctions.outputDigit(minLsb)
				time.sleep(0.25)
				tubeFunctions.off()
				time.sleep(0.25)
				sec = currentTime.second
				secMsb = sec / 10
				secLsb = sec % 10
				tubeFunctions.outputDigit(secMsb)
				time.sleep(0.25)
				tubeFunctions.off()
				time.sleep(0.1)
				tubeFunctions.outputDigit(secLsb)
				time.sleep(0.25)
				tubeFunctions.off()
				time.sleep(1.5)
		i = i + 1


updateTime.updateTime()
while True:
	if GPIO.input(25) == 0:
		wakeMode()
