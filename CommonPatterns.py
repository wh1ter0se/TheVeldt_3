import opc, time, math, itertools, numpy
import RoomConstants as rc
from numpy import polyfit, polyval

pixels = [(0,0,0)] * 512

client_port = 'localhost:7892'

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

# positions zero indexed to the order of RGB
def flip_channels(rgb,pos1,pos2):
	temp = rgb[pos1]
	rgb[pos1] = rgb[pos2]
	rgb[pos2] = temp
	return rgb[0], rgb[1], rgb[2]

def reorder_channels(rgb,RGB_order):
	a = RGB_order[0]
	b = RGB_order[1]
	c = RGB_order[2]
	return rgb[a], rgb[b], rgb[c]

def hsvpos2rgb(h,s,v,pos):
	r, g, b = hsv2rgb(h,s,v)
	#if rc.curr_house.check_invert(pos):
	#	r, g, b = flip_channels([r,g,b],0,1)
	RGB_order = rc.curr_house.get_RGB_order(pos)
	r, g, b = reorder_channels([r,g,b],RGB_order)
	return r, g, b

def points2pal(entries,fit,res):
	x_vals = entries[0]
	yR_vals = entries[1]
	yG_vals = entries[2]
	yB_vals = entries[3]
	if   fit == 0: # linear
		deg = 1
	elif fit == 1: # polynomial
		deg = len(entries)-1
	Rfit = polyfit(x_vals,yR_vals,deg)
	Gfit = polyfit(x_vals,yG_vals,deg)
	Bfit = polyfit(x_vals,yB_vals,deg)
	output = [(0,0,0)] * res
	for i in range(res):
		output[i] = (polyval(Rfit,i),polyval(Gfit,i),polyval(Bfit,i))
	return output

def pal2rgb(palette,palette_pos):
	return palette[palette_pos]

def palpos2rgb(palette,palette_pos,LED_pos):
	r, g, b = pal2rgb(palette,palette_pos)
	#if rc.curr_house.check_invert(LED_pos):
	#	r, g, b = flip_channels([r,g,b],0,2)
	RGB_order = rc.curr_house.get_RGB_order(LED_pos)
	r, g, b = reorder_channels([r,g,b],RGB_order)
	return r, g, b

def tick(iter,floor,ceil,increment):
	iter += increment
	if iter > ceil:
		iter = floor
	return iter

def ftick(tickdata):
	return tick(tickdata[0],tickdata[1],tickdata[2],tickdata[3])

def solid_rainbow(line_map,iter,increment,brightness):
	client = opc.Client(client_port)
	for x in line_map:
		pixels[x] = hsvpos2rgb(iter,1.0,brightness,x)
	client.put_pixels(pixels)
	return [iter,0,360,increment]

def solid_color(line_map,hue,saturation,brightness):
	client = opc.Client(client_port)
	for x in line_map:
		pixels[x] = hsvpos2rgb(hue,saturation,brightness,x)
	client.put_pixels(pixels)

def rainbow(line_map,iter,increment,brightness,skew,sinK):
	client = opc.Client(client_port)
	indx = line_map
	delta = 0
	for i in indx:
		pixels[i] = hsvpos2rgb((iter+skew*delta+math.sin(i)*sinK)%360,1.0,brightness,i)
		delta += 1
	client.put_pixels(pixels)
	return [iter,0,360,increment]

def vert_rainbow(grid_map,iter,increment,brightness,skew,sinA,sinT):
	client = opc.Client(client_port)
	for j in range(len(grid_map[0])):
		for i in range(len(grid_map)):
			# if isinstance(type(grid_map[i][j]),list):
			# 	for indx in grid_map[i][j]:
			# 		if indx >= 0:
			# 			pixels[indx] = hsvpos2rgb((iter+skew*j+math.sin(iter*sinA)*sinT)%360,1.0,brightness,grid_map[i][j])
			# elif isinstance(type(grid_map[i][j]),int) and grid_map[i][j] != -1:
			# 	pixels[grid_map[i][j]] = hsvpos2rgb((iter+skew*j+math.sin(iter*sinA)*sinT)%360,1.0,brightness,grid_map[i][j])
			if grid_map[i][j] >= 0:
				pixels[grid_map[i][j]] = hsvpos2rgb((iter+skew*j+math.sin(iter*sinA)*sinT)%360,1.0,brightness,grid_map[i][j])
	client.put_pixels(pixels)
	return [iter,0,360,increment]

def horizont_rainbow(grid_map,iter,increment,brightness,skew,sinA,sinT):
	client = opc.Client(client_port)
	for j in range(len(grid_map[0])):
		for i in range(len(grid_map)):
			if grid_map[i][j] >= 0:
				#print(grid_map[i][j])
				pixels[grid_map[i][j]] = hsvpos2rgb((iter+skew*i+math.sin(iter*sinA)*sinT)%360,1.0,brightness,grid_map[i][j])
	client.put_pixels(pixels)
	return [iter,0,360,increment]

def diag_rainbow(grid_map,iter,increment,brightness,skew,sinA,sinT):
	client = opc.Client(client_port)
	for j in range(len(grid_map[0])):
		for i in range(len(grid_map)):
			if grid_map[i][j] >= 0:
				d = math.sqrt(i**2 + j**2)
				pixels[grid_map[i][j]] = hsvpos2rgb((iter+skew*d+math.sin(iter*sinA)*sinT)%360,1.0,brightness,grid_map[i][j])
	client.put_pixels(pixels)
	return [iter,0,360,increment]

def vert_palette(grid_map,palette,brightness):
	client = opc.Client(client_port)
	for j in range(len(grid_map[0])):
		for i in range(len(grid_map)):
			if grid_map[i][j] >= 0:
				pixels[grid_map[i][j]] = brightness * palpos2rgb(palette,j,grid_map[i][j])
	client.put_pixels(pixels)

def solid_rainbow_hue_pulse(line_map,iter,levels,stale_levels,idle_increment,brightness,pulse_intensity):
	client = opc.Client(client_port)
	#print(levels)
	if levels[0] == -1:
		print("MISSING AUDIO DATA")
		levels[0] = 0
	bass = levels[0]
	stale_bass = stale_levels[0]
	bass_push = pulse_intensity * (bass-stale_bass)
	#print("Bass push: " + str(bass_push) + ', Bass: ' + str(bass))
	iter += bass_push
	iter %= 360
	for x in line_map:
		pixels[x] = hsvpos2rgb((iter)%360,1.0,brightness,x)
	client.put_pixels(pixels)
	return [iter,0,360,idle_increment]

def solid_rainbow_brightness_pulse(line_map,iter,levels,increment,min_brightness,max_brightness,pulse_intensity):
	client = opc.Client(client_port)
	#print(levels)
	if levels[0] == -1:
		print("MISSING AUDIO DATA")
		levels[0] = 0
	bass = levels[0]
	bass_push = pulse_intensity * bass
	#print("Bass push: " + str(bass_push) + ', Bass: ' + str(bass))
	brightness = max(min_brightness+bass_push,max_brightness)
	for x in line_map:
		pixels[x] = hsvpos2rgb(iter,1.0,brightness,x)
	client.put_pixels(pixels)
	return [iter,0,360,increment]

def solid_rainbow_saturation_pulse(line_map,iter,levels,increment,brightness,saturation,min_saturation,pulse_intensity):
	client = opc.Client(client_port)
	#print(levels)
	if levels[0] == -1:
		print("MISSING AUDIO DATA")
		levels[0] = 0
	bass = levels[0]
	bass_push = pulse_intensity * bass
	#print("Bass push: " + str(bass_push) + ', Bass: ' + str(bass))
	saturation = min(saturation-bass_push,min_saturation)
	for x in line_map:
		pixels[x] = hsvpos2rgb(iter,saturation,brightness,x)
	client.put_pixels(pixels)
	return [iter,0,360,increment]

def two_color_pulse(line_map,levels,stale_bass,decay_rate,brightness,hueA,hueB,similarity_theshold,pulse_intensity):
	client = opc.Client(client_port)
	if levels[0] == -1:
		print("MISSING AUDIO DATA")
		levels[0] = 0
	bass = float(levels[0])
	bass = max(stale_bass-decay_rate,bass)
	state = min(pulse_intensity * bass,1)
	if state < similarity_theshold:
		state = 0
	hue = (state * hueB) + ((1-state) * hueA)
	for x in line_map:
		pixels[x] = hsvpos2rgb(hue,1.0,brightness,x)
	client.put_pixels(pixels)
	return bass