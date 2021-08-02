#from common_patterns import *
from numpy.core.arrayprint import DatetimeFormat
from numpy.core.numeric import full
import common_patterns as cp
import datetime
from RoomConstants import *

init = True

def unix_time(dt):
	epoch = datetime.datetime.utcfromtimestamp(0)
	return (dt-epoch).total_seconds()

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

def off(iterator=None):
    cp.solid_color(allstrips,0,0,0)
    return iterator

dm_off = DisplayMode('Off', off)

def solid_rainbow(iterator):
    iterator[0] = cp.ftick(cp.solid_rainbow(allstrips,iterator[0],0.5,1.0))
    return iterator

dm_solid_rainbow = DisplayMode('Solid Rainbow', solid_rainbow)

def rainbow(iterator):
    iterator[0] = cp.ftick(cp.rainbow(allstrips,iterator[0],3.0,1.0,2.5,3.0))
    return iterator

dm_rainbow = DisplayMode('Rainbow', rainbow)

def vert_rainbow(iterator):
    iterator[0] = cp.ftick(cp.vert_rainbow(grid_map,iterator[0],-3.0,1,7.5,0.0,0.0))
    return iterator

dm_vert_rainbow = DisplayMode('Vertical Rainbow')

def diag_rainbow(iterator):
    iterator[0] = cp.ftick(diag_rainbow(grid_map,iterator[0],-2.0,0.3125,7.5,1.0,1.0))
    return iterator

class FunctionMap():
    def __init__(self,func_tuple_map,final_ts):
        funcs = []
        deltas = []
        for func, delta in func_tuple_map:
            funcs.append(func)
            deltas.append(delta)
        self.funcs = funcs
        self.deltas = deltas
        self.final_ts = final_ts
    
    def get_func_index(self,ts):
        for i in range(1,len(self.funcs)):
            end_ts = self.final_ts + self.deltas[i]
            stale_end_ts = self.final_ts + self.deltas[i-1]
            if unix_time(ts) >= unix_time(stale_end_ts) and unix_time(ts) < unix_time(end_ts):
                return i
        first_ts = self.final_ts + self.deltas[0]
        last_ts = self.final_ts + self.deltas[len(self.deltas)]
        if unix_time(first_ts) < unix_time(ts):
            return 0
        elif unix_time(ts) >= unix_time(last_ts):
            return len(self.deltas)-1
        else:
            return -1

    def completion(self,ts):
        func_index = self.get_func_index(ts)
        if func_index == 0:
            return 0.0
        else:
            curr_len = ts - (self.final_ts + self.deltas[func_index])
            full_len = self.deltas[func_index] - self.deltas[func_index-1]
            return curr_len / full_len

class AlarmClockDisplayMode(DisplayMode):
    def __init__(self, label, func_tuple_map): # function map should include time deltas
        self.func_tuple_map = func_tuple_map
        super().__init__(label, func=self.iter_func, init_func=self.init_func)

    def init_func(self):
        start_hr = input('Start hour: ')
        start_mn = input('Start minute: ')
        curr = datetime.datetime.now()
        final_ts = unix_time(datetime.datetime(curr.year,curr.month,\
					                      curr.day,start_hr,start_mn))
        if curr.hour > start_hr:
            final_ts += 24 * 60 * 60
        self.func_map = FunctionMap(self.func_tuple_map, final_ts)
    
    def iter_func(self):
        curr_ts = unix_time(datetime.datetime.now())
        func_index = self.func_map.get_func_index(curr_ts)
        if func_index == -1:
            off()
        else:
            func = self.func_map.funcs[func_index]
            func(self.func_map.completion(curr_ts))

def solid_rainbow_clock(iterator,completion):
    iterator[0] = cp.ftick(cp.solid_rainbow(allstrips,iterator[0],0.5,completion))
    return iterator
rainbow_clock_map = {(off, -2*60*60),
                     (solid_rainbow_clock, 0),
                     (vert_rainbow, 1*60*60)}
dm_rainbow_clock = AlarmClockDisplayMode('Rainbow Clock', rainbow_clock_map)

mode_list = {('Off',off),
             ('Solid Rainbow',solid_rainbow),
             ('Rainbow',rainbow),
             ('Vertical Raimbow',vert_rainbow),
             ('Diagonal Rainbow',diag_rainbow)}