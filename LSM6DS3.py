#!/usr/bin/python
# Code sourced from AdaFruit discussion board:
# https://www.adafruit.com/forums/viewtopic.php?f=8&t=34922

import sys
import time
import math

import Adafruit_GPIO as GPIO
import Adafruit_GPIO.I2C as I2C

address = 0x6b

class LSM6DS3:
    i2c = None
    bullshit = 0
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
		
# 		print x_val,accel_center_x,y_val,accel_center_y,z_val,accel_center_z
		
		#Work out the squares 
		x2 = x_val*x_val
		y2 = y_val*y_val
		z2 = z_val*z_val
		
		#X Axis
		result = math.sqrt(y2+z2)
# 		print result
		if (result != 0):
			result = x_val/result
# 		print result
		accel_angle_x = math.atan(result)
		
		#Y Axis
	# 	result=sqrt(x2+z2)
# 		result=y_val/result
# 		accel_angle_y = atan(result)


		
		return accel_angle_x;
	
	
	

	

       #  readU16(&dataToWrite, 0x13); 0x13
# 		dataToWrite &= ~((uint8_t)LSM6DS3_ACC_GYRO_BW_SCAL_ODR_ENABLED); 0x80
# 		if ( settings.accelODROff == 1) {
# 			dataToWrite |= LSM6DS3_ACC_GYRO_BW_SCAL_ODR_ENABLED; 
# 		}
# 		write8(LSM6DS3_ACC_GYRO_CTRL4_C, dataToWrite);
# Set up gryo
        # dataToWrite = 0 #Start Fresh!
		#         dataToWrite |= 0x00 # dataToWrite |= LSM6DS3_ACC_GYRO_FS_G_500dps;
		#         dataToWrite |= 0x10 # dataToWrite |= LSM6DS3_ACC_GYRO_ODR_G_104Hz;
		#self.i2c.write8(0X11, dataToWrite) #writeRegister(LSM6DS3_ACC_GYRO_CTRL2_G, dataToWrite);


    def readRawGyroX(self):
        #output = self.i2c.readU16(0X22)
        #try this instead, supposed to be signed
        output = self.i2c.readS16(0X22)
        # OK this bit is in two's compliment, so i need to look at the bianary for this.
        
        # if (output & (1 << (output - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
#             output = output - (1 << bits)        # compute negative value
#         print output
        
        #magnitude = self.i2c.readU8(0X0B) # 0X0B register for which way it is, = or -, need bit 3 from bye
        # print magnitude
        return output;

    def readFloatGyroX(self):
        output = self.calcGyro(self.readRawGyroX())
        return output;

    def calcGyroXAngle(self):
        temp = 0
        temp += self.readFloatGyroX()
        if (temp > 3 or temp < 0):
            self.bullshit += temp
        return self.bullshit;

    def calcGyro(self, rawInput):
        gyroRangeDivisor = 245 / 125; #500 is the gyro range (DPS)
        output = rawInput * 4.375 * (gyroRangeDivisor) / 1000;
        return output;

#   def readFloatGyroX(self):
#       return self.calcGyro(self.readRawGyroX())
#
#   def calcGyro(self, input):
#       gyroRangeDivisor = 2000 / 125 #settings.gyroRange = 2000; //Max deg/s.
#       Can be: 125, 245, 500, 1000, 2000 output = input * 4.375 *
#       (gyroRangeDivisor) / 1000 return output








#define LSM6DS3_ACC_GYRO_OUTX_L_XL  			0X28
#define LSM6DS3_ACC_GYRO_OUTX_H_XL  			0X29
#define LSM6DS3_ACC_GYRO_OUTY_L_XL  			0X2A
#define LSM6DS3_ACC_GYRO_OUTY_H_XL  			0X2B
#define LSM6DS3_ACC_GYRO_OUTZ_L_XL  			0X2C
#define LSM6DS3_ACC_GYRO_OUTZ_H_XL  			0X2D



#Check the settings structure values to determine how to setup the device
	# uint8_t dataToWrite = 0;  //Temporary variable
# 
# 	//Begin the inherited core.  This gets the physical wires connected
# 	status_t returnError = beginCore();
# 
# 	//Setup the accelerometer******************************
# 		//First patch in filter bandwidth
# 			dataToWrite |= LSM6DS3_ACC_GYRO_BW_XL_50Hz; 0x03
# 			dataToWrite |= LSM6DS3_ACC_GYRO_BW_XL_100Hz;
# 			dataToWrite |= LSM6DS3_ACC_GYRO_BW_XL_200Hz;
# 			dataToWrite |= LSM6DS3_ACC_GYRO_BW_XL_400Hz; // Default
# 		
# 		//Next, patch in full scale
# 
# 			dataToWrite |= LSM6DS3_ACC_GYRO_FS_XL_2g; 0x00
# 			dataToWrite |= LSM6DS3_ACC_GYRO_FS_XL_4g;
# 			dataToWrite |= LSM6DS3_ACC_GYRO_FS_XL_8g;
# 			dataToWrite |= LSM6DS3_ACC_GYRO_FS_XL_16g;
# 			
# 		//Lastly, patch in accelerometer ODR
# 			dataToWrite |= LSM6DS3_ACC_GYRO_ODR_XL_13Hz; 0x10
# 			dataToWrite |= LSM6DS3_ACC_GYRO_ODR_XL_26Hz;
# 			dataToWrite |= LSM6DS3_ACC_GYRO_ODR_XL_52Hz;
# 			dataToWrite |= LSM6DS3_ACC_GYRO_ODR_XL_104Hz; // Default 0x40
# 			dataToWrite |= LSM6DS3_ACC_GYRO_ODR_XL_208Hz;
# 			dataToWrite |= LSM6DS3_ACC_GYRO_ODR_XL_416Hz;
# 			dataToWrite |= LSM6DS3_ACC_GYRO_ODR_XL_833Hz;
# 			dataToWrite |= LSM6DS3_ACC_GYRO_ODR_XL_1660Hz;
# 			dataToWrite |= LSM6DS3_ACC_GYRO_ODR_XL_3330Hz;
# 			dataToWrite |= LSM6DS3_ACC_GYRO_ODR_XL_6660Hz;
# 			dataToWrite |= LSM6DS3_ACC_GYRO_ODR_XL_13330Hz;
# 
# 	//Now, write the patched together data
# 	writeRegister(LSM6DS3_ACC_GYRO_CTRL1_XL, dataToWrite); 0x10
# 
# 	//Set the ODR bit
# 	readRegister(&dataToWrite, LSM6DS3_ACC_GYRO_CTRL4_C);
# 	dataToWrite &= ~((uint8_t)LSM6DS3_ACC_GYRO_BW_SCAL_ODR_ENABLED);
# 	if ( settings.accelODROff == 1) {
# 		dataToWrite |= LSM6DS3_ACC_GYRO_BW_SCAL_ODR_ENABLED;
# 	}
# 	writeRegister(LSM6DS3_ACC_GYRO_CTRL4_C, dataToWrite);







