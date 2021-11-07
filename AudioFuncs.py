import time, datetime, sys
from serial import Serial
#import matplotlib.pyplot as plt
#from veldt_manager import unix_millis
#ser = Serial('/dev/ttyUSB0',115200,timeout=1)
#ser.flush()
#ser = None

def get_serial():
	print("init serial")
	ser = Serial('/dev/ttyUSB0',115200,timeout=1)
	ser.flush()
	return ser

def unix_millis(dt):
	epoch = datetime.datetime.utcfromtimestamp(0)
	return (dt-epoch).total_seconds() * 1000.0

def read_levels(serial_obj):
	levels = [-1,-1,-1,-1,-1,-1,-1]
	#while(ser.in_waiting<1):
	#	pass
	if(serial_obj.in_waiting>0):
		line = serial_obj.readline().decode('utf-8')+ ' ' # .decode('utf-8')
		print(line)
		indx = 0
		for i in range(7):
			levels[i] = int(line[indx:line.find(' ',indx)])
			indx = line.find(' ',indx)+3
		if isValid(levels):
			return levels
		# else:
		# 	return levels

def isValid(levels):
	for i in range(7):
		try:
			if int(levels[i]) < 0:
				return False
		except ValueError:
			return False
		except TypeError:
			return False
	return True

def sample_levels(serial_obj,windowms):
	start = unix_millis(datetime.datetime.now())
	sums = [0,0,0,0,0,0,0]
	valid = 0
	while unix_millis(datetime.datetime.now()) < start + windowms:
		line = read_levels(serial_obj)
		if isValid(line):
			for i in range(7):
				sums[i] = sums[i] + int(line[i])
			valid = valid + 1
	output = [-1,-1,-1,-1,-1,-1,-1,windowms]
	if valid > 0:
		for j in range(7):
			output[j] = sums[j] / valid
	return output

# downrate is in ticks per ms
def decay(oldLevels,newLevels,downrate):
	out = newLevels
	untimed = False
	try:
		dr = downrate * newLevels[7]
	except IndexError:
		dr = downrate * 25
	except TypeError:
		return oldLevels
	for i in range(7):
		if newLevels[i] < (oldLevels[i] - dr):
			out[i] = oldLevels[i] - dr
	return out

def smooth(oldLevels,newLevels,down,up):
	out = newLevels
	for i in range(7):
		if newLevels[i] < (oldLevels[i]-down):
			out[i] = oldLevels[i] - down
		elif newLevels[i] > (oldLevels[i]+up):
			out[i] = oldLevels[i] + up
		out[i] = min(1024,max(0,out[i]))
	return out

def getBand(levels,start,stop):
	out = 0
	for i in range(start,stop):
		out += levels[i]
	out = out / (stop+1-start)
	return out

def print_levels(levels):
	if levels is not None:
		output = ""
		for i in range(7):
			output += str(levels[i]) + " "
		print(output)

def plotLevels(levels):
	scalar = (20/1024)
	for i in range(7):
		line = str(i+1) + ' '
		#line += str(levels[i])
		bars = levels[i]/51.2
		for j in range(int(bars)):
			line +=  '-'
		print(line)



if len(sys.argv) > 1:
	ser = Serial('/dev/ttyUSB0',115200,timeout=1)
	ser.flush()
	#levels = sample_levels(ser,2000)
	while 42:
		#levels = decay(levels,sampleLevels(150),0.75)	
		levels = read_levels(ser)
		#print_levels(levels)
		#plotLevels(levels)
		#plotLevels(levels)
