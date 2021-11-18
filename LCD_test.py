import I2C_LCD_driver
import sys
from time import *

mylcd = I2C_LCD_driver.lcd()

mylcd.lcd_display_string(sys.argv[1], 1)