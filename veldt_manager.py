import time, datetime
#from itertools import chain
from common_patterns import *
from gradientts import *
#from audio_funcs import *

displayMode = 1

strips = [64,29,64,20,10,9,0,0]
skyA = list(range(0,30))
skyB = list(range(30,54))
skyC = list(range(65,103))
sky = skyA+skyB+skyC
splashA = list(range(64*2,64*2+20))
splashB = list(range(64*2+20,64*2+27))
splashC = list(range(64*2+27,64*2+45))
splashD = list(range(64*3+36,64*3+32,-1))
splashE = list(range(64*3+11,64*3-1,-1))
splashF = list(range(64*3+32,64*3+23,-1))
splashG = list(range(64*3+23,64*3+12,-1))
splash = splashA+splashB+splashC+splashD+splashE+splashF+splashG
#splash = list(chain(range(64*2,64*2+45),range(64*3+36,64*3+32,-1),\
#	       range(64*3+11,64*3-1,-1),range(64*3+32,64*3+11,-1)))
bed = list(range(64*4,64*4+35))
desk = list(range(64*5,64*5+40))
grnd = desk + bed
#allstrips = chain(sky,splash,desk,bed)
allstrips = sky + splash + grnd
grid_map = [[-1 for x in range(32)] for y in range(128)]

levels = [-1,-1,-1,-1,-1,-1,-1,-1]

def unix_millis(dt):
	epoch = datetime.datetime.utcfromtimestamp(0)
	return (dt-epoch).total_seconds() * 1000.0

def add_strip_to_grid_map(strip,start_pos,direction_uvec,rev):
	if rev:
		strip = reversed(strip)
	count = 0
	for indx in strip:
		new_pos = [start_pos[0]+count*direction_uvec[0], \
			   start_pos[1]+count*direction_uvec[1]]
		#print[new_pos]
		grid_map[new_pos[0]][new_pos[1]] = indx
		count += 1

def init_grid_map():
	add_strip_to_grid_map(skyC,[4,0],[1,0],True)
	add_strip_to_grid_map(skyB,[42,0],[1,0],True)
	add_strip_to_grid_map(skyA,[76,0],[1,0],True)
	add_strip_to_grid_map(splashA,[67,6],[0,1],True)
	add_strip_to_grid_map(splashB,[66,5],[-1,0],False)
	add_strip_to_grid_map(splashC,[59,6],[0,1],False)
	add_strip_to_grid_map(splashD,[58,13],[-1,0],False)
	add_strip_to_grid_map(splashE,[54,15],[0,1],False)
	add_strip_to_grid_map(splashF,[53,13],[-1,0],False)
	add_strip_to_grid_map(splashG,[69,15],[0,1],False)
	add_strip_to_grid_map(desk[:7],[60,25],[1,0],False)
	add_strip_to_grid_map(desk[7:],[68,25],[1,0],False)
	add_strip_to_grid_map(bed,[0,27],[1,0],True)
init_grid_map()
iterator = [0,0,0]
while True:
	if   displayMode == 0: # off
		solid_color(allstrips,0,0,0)
	elif displayMode == 1: # solid_rainbow
		iterator[0] = ftick(solid_rainbow(allstrips,iterator[0],0.5,1.0))
	elif displayMode == 2: # rainbow
		iterator[0] = ftick(rainbow(allstrips,iterator[0],3.0,1.0,2.5,3.0))
	elif displayMode == 3: # vertical rainbow
		iterator[0] = ftick(vert_rainbow(grid_map,iterator[0],-3.0,1,7.5,0.0,0.0))
	elif displayMode == 4:
		iterator[0] = ftick(diag_rainbow(grid_map,iterator[0],-2.0,0.3125,7.5,1.0,1.0))
	elif displayMode == 5:
		brightness = .2
		sinA = .05
		sinT = 40.0
		speed_amp = 1.5
		top = hsv2rgb(iterator[0],.8,brightness)
		mid = hsv2rgb(iterator[1]+math.sin(iterator[1]*(sinA))*sinT,1.0,brightness)
		bot = hsv2rgb((iterator[2] + 120)%360,1.0,brightness)
		pe_r2b = [[0,14,28],[top[0],mid[0],bot[0]],\
				 [top[1],mid[1],bot[1]],\
				 [top[2],mid[2],bot[2]]]
		#pe_r2b = [[0,27],[top[0],bot[0]],\
		#		 [top[1],bot[1]],\
		#		 [top[2],bot[2]]]
		p_r2b = points2pal(pe_r2b,0,28)
		vert_palette(grid_map,p_r2b,1)
		iterator[0] = tick(iterator[0],0,360,-4*speed_amp)
		iterator[1] = tick(iterator[1],0,360,2*speed_amp)
		iterator[2] = tick(iterator[2],0,360,-2*speed_amp)
	elif displayMode == 6:
		brightness = 1.0
		p_grapefruit = points2pal(pe_grapefruit(brightness),0,28)
		vert_palette(grid_map,p_grapefruit,1)
	elif displayMode == 7:
		brightness = 1.0
		line = sampleLevels(25)
		if isValid(line):
			levels = decay(levels,line,.5)
#		plotLevels(levels);
		bass = ((levels[0]+levels[1])/2) *.005
		mid = ((levels[2]+levels[3])/2) *.0025
		#bass = int(float(20*bass) / 1024.0)
		#print(bass)
		#treble = int(float(20*treble) / 1024.0)
		#treble *= 20
#		print(treble)
		#print(str(bass) + ',' + str(treble))
		top = hsv2rgb(iterator[1],.75,0.5+mid)
		bot = hsv2rgb(iterator[0],1,0.5+bass)
		pe_sr =[[0,28],[top[0],bot[0]],\
			       [top[1],bot[1]],\
			       [top[2],bot[2]]]
		p_sr = points2pal(pe_sr,0,28)
		vert_palette(grid_map,p_sr,1)
		iterator[0] = tick(iterator[0],0,360,-2)
		iterator[1] = tick(iterator[1],0,360,2)
	elif displayMode == 8:
		solid_color(allstrips,0,1,1)
	elif displayMode == 13: # morning glow (90min fade in at time)
		#solid_color(bed,0,0,0)
		#solid_color(sky,60,0.6,1.0)
		#solid_color(desk,355,0.85,0.75)
		#solid_color(splash,342,0.82,0.9)
		#iterator[0] = ftick(rainbow(splash,iterator[0],5.0,1.0,1.5,1.0))

		hr = 8
		mn = 30
		fadeMillis = 90*60*1000
		cur = datetime.datetime.now()
		start = datetime.datetime(cur.year,cur.month,cur.day,hr,mn)
		if unix_millis(cur) < unix_millis(start):
			solid_color(allstrips,0,0,0)
		elif unix_millis(cur) < unix_millis(start) + fadeMillis:
			brightness = (unix_millis(cur) - unix_millis(start)) / fadeMillis
			solid_color(bed,0,0,0)
			solid_color(sky,60,0.6,brightness)
			solid_color(desk,355,0.85,75*brightness)
			solid_color(splash,342,0.82,brightness)
		else:
			displayMode = 5
			#solid_color(bed,0,0,0)
                        #solid_color(sky,60,0.6,1)
                        #solid_color(desk,355,0.85,0,75)
                        #solid_color(splash,342,0.82,1)
			#iterator[0] = solid_rainbow(splash,iterator[0],0.5,1.0)
	elif displayMode == 14:
		solid_color(bed,0,0,0)
                solid_color(sky,60,0.6,1.0)
                solid_color(desk,355,0.85,0,75)
                solid_color(splash,342,0.82,1.0)
	elif displayMode == 15: # rainbow (30min fade in at time)
		hr = 8
		mn = 15
		fadeMillis = 60 * 60 * 1000
		curr = datetime.datetime.now()
		start = datetime.datetime(curr.year,curr.month, \
			curr.day,hr,mn)
		if unix_millis(curr) < unix_millis(start):
			solid_color(allstrips,0,0,0)
		elif unix_millis(curr) < unix_millis(start) + fadeMillis:
			brightness = (unix_millis(curr) - unix_millis(start))/fadeMillis
			iterator[0] = ftick(solid_rainbow(allstrips,iterator[0],1.0,brightness))
		else:
			displayMode = 3
	elif displayMode == 16: # morning sun (2hr fade in at time)
		hr = 8
		mn = 45
		fadeMillis = 300 * 60 * 100
		curr = datetime.datetime.now()
		start = datetime.datetime(curr.year,curr.month,\
					 curr.day,hr,mn)
		if unix_millis(curr) < unix_millis(start):
			solid_color(allstrips,0,0,0)
			#solid_color(splash,0,0,0)
			#solid_color(sky,0,0,0)
			#solid_color(desk,0,0,0)
			#iterator[0] = ftick(rainbow(grnd,iterator[0],1.0,0.375,1,0))
		elif unix_millis(curr) < unix_millis(start) + fadeMillis:
			brightness = (unix_millis(curr) - unix_millis(start))/fadeMillis
			p_grapefruit = points2pal(pe_grapefruit(brightness),0,28)
	                vert_palette(grid_map,p_grapefruit,1)
		else:
			displayMode = 6
#	schedule.run_pending()
	#time.sleep(.01)
