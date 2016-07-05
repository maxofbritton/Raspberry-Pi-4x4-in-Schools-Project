import sys
import time
import math

import Adafruit_GPIO as GPIO
import Adafruit_GPIO.I2C as I2C

address = 0x53

class ADXL345:
    i2c = None
    bullshit = 0
    global accel_center_x
    accel_center_x = 0
    global accel_center_y
    accel_center_y = 0
    global accel_center_z
    accel_center_z = 0

    
    def __init__(self, address=0x53, debug=0, pause=0.8):
        self.i2c = I2C.get_i2c_device(address)
        self.address = address
        self.i2c.write8(0x2D, 0x08) #ADXL345_REG_POWER_CTL 0x2D
        
        dataToWrite = 0 #Start Fresh!
        dataToWrite |= 0b00
        self.i2c.write8(0X31, dataToWrite) #ADXL345_REG_DATA_FORMAT 0x31 2g
        
        dataToWrite = 0 #Start Fresh!
        dataToWrite |= 0b0101
        self.i2c.write8(0x2C, dataToWrite) #ADXL345_REG_DATA_FORMAT 0x31 2g
        
        accel_center_x = self.i2c.readS16(0X32)
        accel_center_y = self.i2c.readS16(0X34)
        accel_center_z = self.i2c.readS16(0X36)
    
    def readRawAccelX(self):
    	output = self.i2c.readS16(0X32) #use 0x33 alt
    	return output;
    
    def readRawAccelY(self):
    	output = self.i2c.readS16(0x34)
    	return output;
    
    def readRawAccelZ(self):
    	output = self.i2c.readS16(0x36)
    	return output;
    	
    def calcAnglesXY(self):
		#Using x y and z from accelerometer, calculate x and y angles
		x_val = 0
		y_val = 0
		z_val = 0
		result = 0
		
		x2 = 0
		y2 = 0
		z2 = 0
		x_val = self.readRawAccelX() - accel_center_x
		y_val = self.readRawAccelY() - accel_center_y
		z_val = self.readRawAccelZ() - accel_center_z

		x2 = x_val*x_val
		y2 = y_val*y_val
		z2 = z_val*z_val

		result = math.sqrt(y2+z2)
		if (result != 0):
			result = x_val/result
		accel_angle_x = math.atan(result)
		
		#Y Axis
	# 	result=sqrt(x2+z2)
# 		result=y_val/result
# 		accel_angle_y = atan(result)
		
		return accel_angle_x;