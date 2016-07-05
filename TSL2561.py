import sys
import time

import Adafruit_GPIO as GPIO
import Adafruit_GPIO.I2C as I2C

address = 0x39

class TSL2561:
    i2c = None

    def __init__(self, address=0x39, debug=0, pause=0.8):
    
        self.i2c = I2C.get_i2c_device(address)
        self.address = address
        self.pause = pause
        self.debug = debug
        self.gain = 0 # no gain preselected
        self.i2c.write8(0x80, 0x03)     # enable the device


    def setGain(self,gain=1):
        """ Set the gain """
        if (gain != self.gain):
            if (gain==1):
                self.i2c.write8(0x81, 0x02)     # set gain = 1X and timing = 402 mSec
                if (self.debug):
                    print "Setting low gain"
            else:
                self.i2c.write8(0x81, 0x12)     # set gain = 16X and timing = 402 mSec
                if (self.debug):
                    print "Setting high gain"
            self.gain=gain;                     # safe gain for calculation
            time.sleep(self.pause)              # pause for integration (self.pause must be bigger than integration time)


    def readWord(self, reg):
        """Reads a word from the I2C device"""
        try:
            wordval = self.i2c.readU16(reg)
            newval = ((wordval << 8 & 0xFF00) | (wordval >> 8 & 0X00FF))
#             newval = self.i2c.reverseByteOrder16(wordval)
            if (self.debug):
                print("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" % (self.address, wordval & 0xFFFF, reg))
            return newval
        except IOError:
            print("Error accessing 0x%02X: Check your I2C address" % self.address)
            return -1


    def readFull(self, reg=0x8C):
        """Reads visible+IR diode from the I2C device"""
        return self.readWord(reg);
        
    def readFullCustom(self):
    	reg1=0x8C
    	reg2=0x8D
    	result = self.i2c.readU16(reg2)
    	return result