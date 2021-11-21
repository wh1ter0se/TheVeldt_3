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

opt_list = ['A','B','C','D','E','F']
# curr_index = 0

def update_list(position):
    curr_index = int(position)
    down_diff = max(curr_index - 4,0)
    mylcd.lcd_clear()
    for i in range(4):
        if curr_index == (down_diff + i):
            prefix = "  "
        else:
            prefix = "> "
        curr_line = prefix + opt_list[down_diff+i]
        mylcd.lcd_display_string(curr_line, i+1)

# Init the encoder pins
my_encoder = pyky040.Encoder(CLK=17, DT=18, SW=27)

# Or the encoder as a device (must be installed on the system beforehand!)
# my_encoder = pyky040.Encoder(device='/dev/input/event0')

# Setup the options and callbacks (see documentation)
# my_encoder.setup(scale_min=0, scale_max=100, step=1, chg_callback=my_callback)
my_encoder.setup(scale_min=0, scale_max=len(opt_list), step=.5, chg_callback=update_list)

# Launch the listener
my_encoder.watch()

# Mess with the encoder...
# > Hello world! The scale position is 1
# > Hello world! The scale position is 2
# > Hello world! The scale position is 3
# > Hello world! The scale position is 2
# > Hello world! The scale position is 1