import sys
import time
import math

import Adafruit_GPIO as GPIO
import Adafruit_GPIO.I2C as I2C

address = 0x6b

class LSM6DS3:
    i2c = None
    tempvar = 0
    global accel_center_x
    accel_center_x = 0
    global accel_center_y
    accel_center_y = 0
    global accel_center_z
    accel_center_z = 0

    
    def __init__(self, address=0x6b, debug=0, pause=0.8):
        self.i2c = I2C.get_i2c_device(address)
        self.address = address
        dataToWrite = 0 #Start Fresh!
        dataToWrite |= 0x03 # set at 50hz, bandwidth
        dataToWrite |= 0x00  # 2g accel range
        dataToWrite |= 0x10 # 13hz ODR
        self.i2c.write8(0X10, dataToWrite) #writeRegister(LSM6DS3_ACC_GYRO_CTRL2_G, dataToWrite);
        
        accel_center_x = self.i2c.readS16(0X28)
        accel_center_y = self.i2c.readS16(0x2A)
        accel_center_z = self.i2c.readS16(0x2C)
    
    def readRawAccelX(self):
    	output = self.i2c.readS16(0X28)
    	return output;
    
    def readRawAccelY(self):
    	output = self.i2c.readS16(0x2A)
    	return output;
    
    def readRawAccelZ(self):
    	output = self.i2c.readS16(0x2C)
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
		return accel_angle_x;



    def readRawGyroX(self):
        output = self.i2c.readS16(0X22)
        return output;

    def readFloatGyroX(self):
        output = self.calcGyro(self.readRawGyroX())
        return output;

    def calcGyroXAngle(self):
        temp = 0
        temp += self.readFloatGyroX()
        if (temp > 3 or temp < 0):
            self.tempvar += temp
        return self.tempvar;

    def calcGyro(self, rawInput):
        gyroRangeDivisor = 245 / 125; #500 is the gyro range (DPS)
        output = rawInput * 4.375 * (gyroRangeDivisor) / 1000;
        return output;








