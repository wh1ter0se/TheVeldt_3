#from common_patterns import *
from numpy.core.arrayprint import DatetimeFormat
from numpy.core.numeric import full
import CommonPatterns as cp
import AudioFuncs as af
import datetime, time
import Gradients
from RoomConstants import *

init = True

def unix_time(dt):
	epoch = datetime.datetime.utcfromtimestamp(0)
	return (dt-epoch).total_seconds() * 1.0

class DisplayMode():
    def __init__(self,label,func,vars=None,init_func=None,
                 uses_palette=False,palette=None,uses_MSGEQ7=False):
        self.label = label
        self.func = func
        self.vars = vars
        self.init_func=init_func
        self.uses_palette = uses_palette
        self.palette = palette
        self.iterator = [0,0,0]
        self.is_init = True
        self.uses_MSGEQ7 = uses_MSGEQ7
        self.levels = [-1,-1,-1,-1,-1,-1,-1]
        self.stale_levels = self.levels

    def run(self):
        if self.is_init:
            if self.init_func is not None:
                self.init_func(self)
            self.is_init = False
            print("init_func")
            if self.uses_MSGEQ7:
                self.vars = [af.get_serial()]
                print(self.vars)
        if self.uses_MSGEQ7:
            levels = af.read_levels(self.vars[0])
            #print(levels)
            if levels is not None:
                self.stale_levels = self.levels
                self.levels = levels
            self.iterator = self.func(iterator=self.iterator,levels=self.levels,vars=self.vars)
        else:
            self.iterator = self.func(iterator=self.iterator,vars=self.vars)
        #print('running')

class DisplayModeList():
    def __init__(self,label,dms):
        self.label = label
        self.dms = dms

class FunctionMap():
    def __init__(self,func_tuple_map,final_ts):
        funcs = []
        deltas = []
        tracklist = []
        for func, delta, tracked in func_tuple_map:
            funcs.append(func)
            deltas.append(delta)
            tracklist.append(tracked)
        self.funcs = funcs
        self.deltas = deltas
        self.tracklist = tracklist
        self.final_ts = final_ts
    
    def get_func_index(self,ts):
        dt = datetime.datetime.utcfromtimestamp(ts)
        print('Current time: ' + str(dt.hour) + ':' + str(dt.minute))
        for i in range(1,len(self.funcs)):
            end_ts = self.final_ts + self.deltas[i]
            stale_end_ts = self.final_ts + self.deltas[i-1]
            if ts >= stale_end_ts and ts < end_ts:
                return i
        first_ts = self.final_ts + self.deltas[0]
        last_ts = self.final_ts + self.deltas[len(self.deltas)-1]
        if first_ts < ts:
            return 0
        elif ts >= last_ts:
            return len(self.deltas)-1
        else:
            return -1

    def completion(self,ts):
        func_index = self.get_func_index(ts)
        if func_index == 0:
            return float(0.0)
        else:
            curr_len = ts - (self.final_ts + self.deltas[func_index])
            full_len = self.deltas[func_index] - self.deltas[func_index-1]
            return float(curr_len / full_len)

class AlarmClockDisplayMode(DisplayMode):
    def __init__(self, label, func_tuple_map): # function map should include time deltas
        self.func_tuple_map = func_tuple_map
        super().__init__(label, func=self.iter_func, init_func=self.init_func)

    def init_func(self):
        start_hr = int(input('Start hour: '))
        start_mn = int(input('Start minute: '))
        curr = datetime.datetime.now()
        final_ts = unix_time(datetime.datetime(curr.year,curr.month,curr.day,start_hr,start_mn))
        if curr.hour > start_hr:
            final_ts += 24 * 60 * 60
        self.func_map = FunctionMap(self.func_tuple_map, final_ts)
    
    def iter_func(self,iterator):
        curr_ts = unix_time(datetime.datetime.now())
        func_index = self.func_map.get_func_index(curr_ts)
        if func_index == -1:
            off()
        else:
            func = self.func_map.funcs[func_index]
            if self.func_map.tracklist[func_index]:
                progress = self.func_map.completion(curr_ts)
                print(progress)
                func(self.iterator, progress)
            else:
                func(self.iterator)

def off(iterator=None,vars=None):
    cp.solid_color(curr_house.allstrips,0,0,0)
    return iterator

dm_off = DisplayMode('Off', off)

def white_striptest(iterator,vars=None):
    cp.solid_color(House.allstrips,0,0,1)
    return iterator

dm_white_striptest = DisplayMode('White Sriptest', white_striptest)

# vars[0] = hue
def solid_color(vars,iterator=None):
    saturation = 1.0
    brightness = 1.0
    cp.solid_color(curr_house.allstrips,vars[0],saturation,brightness)

def solid_color_init(dm):
    print(" 0      60     120    180     240    300")
    print("Red   Violet   Blue   Cyan   Green  Yellow")
    # print("Red   Yellow   Green   Cyan   Blue  Violet")
    hue = int(input("Hue (0-360)"))
    dm.vars = [hue]

dm_solid_color = DisplayMode("Solid Color", solid_color, init_func=solid_color_init)

def solid_rainbow(iterator,vars=None):
    iterator[0] = cp.ftick(cp.solid_rainbow(curr_house.allstrips,iterator[0],0.5,1.0))
    return iterator

dm_solid_rainbow = DisplayMode('Solid Rainbow', solid_rainbow)

def rainbow(iterator,vars=None):
    increment = 3.0
    brightness = 1.0
    skew = 2.5
    sinA = 0.0 # amplitude
    sinK = 3.0 # frequency
    iterator[0] = cp.ftick(cp.rainbow(curr_house.allstrips,iterator[0],increment,brightness,skew,sinK))
    return iterator

dm_rainbow = DisplayMode('Rainbow', rainbow)

def rainbow_striptest(iterator,vars=None):
    increment = 3.0
    brightness = 1.0
    skew = 5.0
    sinA = 0.0 # amplitude
    sinK = 0.0 # frequency
    iterator[0] = cp.ftick(cp.rainbow(House.allstrips,iterator[0],increment,brightness,skew,sinK))
    return iterator

dm_rainbow_striptest = DisplayMode('Rainbow Striptest', rainbow_striptest)

def vert_rainbow(iterator,vars=None):
    increment = -3.0
    brightness = 1.0
    skew = 7.5
    sinA = 0.0 # amplitude
    sinK = 0.0 # frequency
    iterator[0] = cp.ftick(cp.vert_rainbow(curr_house.grid_map,iterator[0],increment,brightness,skew,sinA,sinK))
    return iterator

dm_vert_rainbow = DisplayMode('Vertical Rainbow', vert_rainbow)

def horizont_rainbow(iterator,vars=None):
    increment = -4.0
    brightness = 1.5
    skew = 5.0
    sinA = 0.0 # amplitude
    sinK = 0.0 # frequency
    iterator[0] = cp.ftick(cp.horizont_rainbow(curr_house.grid_map,iterator[0],increment,brightness,skew,sinA,sinK))
    return iterator

dm_horizont_rainbow = DisplayMode("Horizontal Rainbow", horizont_rainbow)

def diag_rainbow(iterator,vars=None):
    increment = -3.0
    brightness = 1.0
    skew = 7.5
    sinA = 0.0 # amplitude
    sinK = 0.0 # frequency
    iterator[0] = cp.ftick(cp.diag_rainbow(curr_house.grid_map,iterator[0],increment,brightness,skew,sinA,sinK))
    return iterator

dm_diag_rainbow = DisplayMode("Diagonal Rainbow", diag_rainbow)

def vert_pallete(iterator,vars=None):
    iterator[0] = cp.vert_palette(curr_house.grid_map,Gradients.pe_caesar,1.0)

dm_vert_palette = DisplayMode("Vertical Palette", vert_pallete)

# vars[0] = Serial object
def solid_rainbow_hue_pulse(iterator,levels,vars=None):
    idle_increment = 1.0
    brightness = 1.0
    pulse_intensity = .05
    iterator[0] = cp.ftick(cp.solid_rainbow_hue_pulse(curr_house.grid_map,iterator[0],levels,idle_increment,brightness,pulse_intensity))
    return iterator

dm_solid_rainbow_hue_pulse = DisplayMode('Solid Rainbow Hue Pulse',solid_rainbow_hue_pulse,uses_MSGEQ7=True)

def solid_rainbow_saturation_pulse(iterator,levels,vars=None):
    increment = 3.0
    brightness = 1.0
    saturation = 1.0
    min_saturation = .5
    pulse_intensity = .01
    iterator[0] = cp.ftick(cp.solid_rainbow_saturation_pulse(curr_house.grid_map,iterator[0],levels,increment,brightness,saturation,min_saturation,pulse_intensity))
    return iterator

dm_solid_rainbow_saturation_pulse = DisplayMode('Solid Rainbow Saturation Pulse',solid_rainbow_saturation_pulse,uses_MSGEQ7=True)

def solid_rainbow_brightness_pulse(iterator,levels,vars=None):
    increment = 3.0
    min_brightness = .5
    max_brightness = 1.0
    pulse_intensity = .01
    iterator[0] = cp.ftick(cp.solid_rainbow_brightness_pulse(curr_house.grid_map,iterator[0],levels,increment,min_brightness,max_brightness,pulse_intensity))
    return iterator

dm_solid_rainbow_brightness_pulse = DisplayMode('Solid Rainbow Brightness Pulse',solid_rainbow_brightness_pulse,uses_MSGEQ7=True)

def solid_rainbow_clock(iterator,completion):
    iterator[0] = cp.ftick(cp.solid_rainbow(curr_house.allstrips,iterator[0],0.5,completion))
    return iterator

rainbow_clock_map = {(off, -2*60*60, False),
                     (solid_rainbow_clock, 0, True),
                     (vert_rainbow, 1*60*60, False)}

dm_rainbow_clock = AlarmClockDisplayMode('Rainbow Clock', rainbow_clock_map)

mode_list = [dm_off,
             dm_white_striptest,
             dm_rainbow_striptest,
             dm_solid_rainbow,
             dm_rainbow,
             dm_vert_rainbow,
             dm_rainbow_clock]

striptest_dm_list = DisplayModeList("Striptests",
                    [dm_off,
                     dm_white_striptest,
                     dm_rainbow_striptest])

standard_dm_list = DisplayModeList("Standard patterns",
                   [dm_off,
                    dm_solid_color,
                    dm_solid_rainbow,
                    dm_rainbow])

grid_map_dm_list = DisplayModeList("Grid-map patterns",
                   [dm_vert_rainbow,
                    dm_horizont_rainbow,
                    dm_diag_rainbow])

audio_dm_list = DisplayModeList("Audio-Based Patterns",
                [dm_solid_rainbow_hue_pulse,
                 dm_solid_rainbow_saturation_pulse,
                 dm_solid_rainbow_brightness_pulse])

palette_dm_list = DisplayModeList("Palette patterns",
                  [dm_vert_palette])

dm_list_dir = [striptest_dm_list,
               standard_dm_list,
               grid_map_dm_list,
               audio_dm_list,
               palette_dm_list]