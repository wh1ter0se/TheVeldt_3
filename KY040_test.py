# Import the module
from pyky040 import pyky040
import I2C_LCD_driver

mylcd = I2C_LCD_driver.lcd()

# Define your callback
def my_callback(scale_position):
    #print('Hello world! The scale position is {}'.format(scale_position))
    # num_str = str(scale_position)
    # final_str = num_str
    # for i in range(20-len(num_str)):
    #     final_str += " "
    # mylcd.lcd_display_string(final_str, 1)
    mylcd.lcd_clear()
    mylcd.lcd_display_string(str(scale_position), 1)

# Init the encoder pins
my_encoder = pyky040.Encoder(CLK=17, DT=18, SW=27)

# Or the encoder as a device (must be installed on the system beforehand!)
# my_encoder = pyky040.Encoder(device='/dev/input/event0')

# Setup the options and callbacks (see documentation)
my_encoder.setup(scale_min=0, scale_max=100, step=1, chg_callback=my_callback)

# Launch the listener
my_encoder.watch()

# Mess with the encoder...
# > Hello world! The scale position is 1
# > Hello world! The scale position is 2
# > Hello world! The scale position is 3
# > Hello world! The scale position is 2
# > Hello world! The scale position is 1