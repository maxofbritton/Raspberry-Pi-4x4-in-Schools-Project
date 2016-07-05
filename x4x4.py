from TSL2561 import TSL2561
# from LSM6DS3 import LSM6DS3
from ADXL345 import ADXL345

import time
import RPi.GPIO as GPIO

tsl = TSL2561()
# lsm = LSM6DS3()
adx = ADXL345()

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led1Pin = 16
led2Pin = 20
buzzerPin = 21
GPIO.setup(led1Pin,GPIO.OUT)
GPIO.setup(led2Pin,GPIO.OUT)
GPIO.setup(buzzerPin,GPIO.OUT)

maxLight = tsl.readFull()
minLight = tsl.readFull()

def headlights(setting):
	if (setting == 0):
		GPIO.output(led1Pin,GPIO.LOW)
		GPIO.output(led2Pin,GPIO.LOW)
	if (setting == 1):
		GPIO.output(led1Pin,GPIO.HIGH)
		GPIO.output(led2Pin,GPIO.HIGH)
		
def buzzer(setting):
	if (setting == 0):
		GPIO.output(buzzerPin,GPIO.LOW)
	if (setting == 1):
		GPIO.output(buzzerPin,GPIO.HIGH)

while True:
	#uncomment if using LSM6DS3
# 	angle = lsm.calcAnglesXY()
# 	angle = (int) (angle * 1000)
	
	angle = adx.readRawAccelX()
	angle = (int) (angle * 3.3)
	
	light = tsl.readFullCustom()
	print angle, light
	
	
	if (light > maxLight):
		maxLight = light
	if (light < minLight):
		minLight = light
	if ((maxLight - minLight) > 500):
		medianLight = (maxLight + minLight) / 2
		if (light < medianLight):
			headlights(1)
		else:
			headlights(0)
	print medianLight
	
	if (angle < -500 or angle > 500):
		buzzer(1)
	if (angle > -500 and angle < 500):
		buzzer(0)
	time.sleep(0.1)