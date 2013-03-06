import os

def updateTime():
	#os.system('sudo ntpd -qg')
	os.system('sudo /etc/init.d/ntp restart > /dev/null')
