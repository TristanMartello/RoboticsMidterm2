
from machine import Pin, I2C
import ssd1306
import framebuf

# Class designed to initialize and maintain the i2c OLED display screen
#   This display posts the temperature, units, and gyroscope values

class i2cScreen:
    def __init__(self, bus=0, scl=9, sda=8, freq=100000):
        # Initialize the necessary i2c variables for the screen
        self.bus = bus
        self.scl = scl
        self.sda = sda
        self.freq = freq
        self.i2c = I2C(id=bus, sda=Pin(sda), scl=Pin(scl))
        self.display = ssd1306.SSD1306_I2C(128, 64, self.i2c)
    
    def mainDisplay(self, temp, unit, gyros):
        # Byte array of raspberry pi logo
        buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
        # Load the raspberry pi logo into the framebuffer (the image is 32x32)
        fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)

        # Clear the oled display
        self.display.fill(0)
        self.display.text('VISUAL INTERFACE', 0, 0, 1)     
        # Blit the image from the framebuffer to the oled display
        self.display.blit(fb, 50, 32)
        
        # Display the current temperature values
        self.display.text('TEMP', 8, 20, 1)
        self.display.text(str(temp), 7, 35, 1)
        self.display.text(unit, 20, 45, 1)
        
        # Display the current gyroscopic values
        self.display.text('GYRO', 90, 20, 1)
        y = 35
        for gyro in gyros:
            self.display.text(str(gyro), 95, y)
            y += 10
        
        self.display.show()
    
    def clear(self):
        # Wipe the display
        self.display.fill(0)
        self.display.show()