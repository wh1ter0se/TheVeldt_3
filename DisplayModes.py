#from common_patterns import *
from numpy.core.arrayprint import DatetimeFormat
from numpy.core.numeric import full
import CommonPatterns as cp
import datetime
from RoomConstants import *

init = True

def unix_time(dt):
	epoch = datetime.datetime.utcfromtimestamp(0)
	return (dt-epoch).total_seconds() * 1.0

class DisplayMode():
    def __init__(self,label,func,vars=None,init_func=None):
        self.label = label
        self.func = func
        self.init_func=init_func
        self.iterator = [0,0,0]
        self.is_init = True

    def run(self):
        if self.init_func is not None and self.is_init:
            self.init_func()
            self.is_init = False
        self.iterator = self.func(self.iterator)
        print('running')

def off(iterator=None):
    cp.solid_color(curr_house.allstrips,0,0,0)
    return iterator

dm_off = DisplayMode('Off', off)

def solid_rainbow(iterator):
    iterator[0] = cp.ftick(cp.solid_rainbow(curr_house.allstrips,iterator[0],0.5,1.0))
    return iterator

dm_solid_rainbow = DisplayMode('Solid Rainbow', solid_rainbow)

def rainbow(iterator):
    iterator[0] = cp.ftick(cp.rainbow(curr_house.allstrips,iterator[0],3.0,1.0,2.5,3.0))
    return iterator

dm_rainbow = DisplayMode('Rainbow', rainbow)

def rainbow_striptest(iterator):
    iterator[0] = cp.ftick(cp.rainbow(House.allstrips,iterator[0],3.0,1.0,2.5,3.0))
    return iterator

dm_rainbow_striptest = DisplayMode('Rainbow Striptest', rainbow_striptest)

def vert_rainbow(iterator):
    iterator[0] = cp.ftick(cp.vert_rainbow(curr_house.grid_map,iterator[0],-3.0,1,7.5,0.0,0.0))
    return iterator

dm_vert_rainbow = DisplayMode('Vertical Rainbow', vert_rainbow)

def diag_rainbow(iterator):
    iterator[0] = cp.ftick(diag_rainbow(curr_house.grid_map,iterator[0],-2.0,0.3125,7.5,1.0,1.0))
    return iterator

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

def solid_rainbow_clock(iterator,completion):
    iterator[0] = cp.ftick(cp.solid_rainbow(curr_house.allstrips,iterator[0],0.5,completion))
    return iterator

rainbow_clock_map = {(off, -2*60*60, False),
                     (solid_rainbow_clock, 0, True),
                     (vert_rainbow, 1*60*60, False)}
dm_rainbow_clock = AlarmClockDisplayMode('Rainbow Clock', rainbow_clock_map)

mode_list = [dm_off,
             dm_solid_rainbow,
             dm_rainbow,
             dm_vert_rainbow,
             dm_rainbow_clock]