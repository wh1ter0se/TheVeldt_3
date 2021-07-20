import opc, time, math, itertools, numpy
from numpy import polyfit, polyval

pixels = [(0,0,0)] * 512


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

#def linear_fit(x,a,b

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

def pal2rgb(palette,pos):
	return palette[pos]

def tick(iter,floor,ceil,increment):
	iter += increment
	if iter > ceil:
		iter = floor
	return iter

def ftick(tickdata):
	return tick(tickdata[0],tickdata[1],tickdata[2],tickdata[3])

def solid_rainbow(line_map,iter,increment,brightness):
	client = opc.Client('localhost:7890')
	for x in line_map:
		pixels[x] = hsv2rgb(iter,1.0,brightness)
	client.put_pixels(pixels)
	return [iter,0,360,increment]

def solid_color(line_map,hue,saturation,brightness):
	client = opc.Client('localhost:7890')
	for x in line_map:
		pixels[x] = hsv2rgb(hue,saturation,brightness)
	client.put_pixels(pixels)

def rainbow(line_map,iter,increment,brightness,skew,sinK):
	client = opc.Client('localhost:7890')
	indx = line_map
	delta = 0
	for i in indx:
		pixels[i] = hsv2rgb((iter+skew*delta+math.sin(i)*sinK)%360,1.0,brightness)
		delta += 1
	client.put_pixels(pixels)
	return [iter,0,360,increment]

def vert_rainbow(grid_map,iter,increment,brightness,skew,sinA,sinT):
	client = opc.Client('localhost:7890')
	for j in range(len(grid_map[0])):
		for i in range(len(grid_map)):
			if grid_map[i][j] >= 0:
				#print(grid_map[i][j])
				pixels[grid_map[i][j]] = hsv2rgb((iter+skew*j+math.sin(iter*sinA)*sinT)%360,1.0,brightness)
	client.put_pixels(pixels)
	return [iter,0,360,increment]

def diag_rainbow(grid_map,iter,increment,brightness,skew,sinA,sinT):
        client = opc.Client('localhost:7890')
        for j in range(len(grid_map[0])):
                for i in range(len(grid_map)):
                        if grid_map[i][j] >= 0:
                                #print(grid_map[i][j])
				d = math.sqrt(i**2 + j**2)
                                pixels[grid_map[i][j]] = hsv2rgb((iter+skew*d+math.sin(iter*sinA)*sinT)%360,1.0,brightness)
        client.put_pixels(pixels)
        return [iter,0,360,increment]

def vert_palette(grid_map,palette,brightness):
	client = opc.Client('localhost:7890')
	for j in range(len(grid_map[0])):
		for i in range(len(grid_map)):
			if grid_map[i][j] >= 0:
				pixels[grid_map[i][j]] = brightness * pal2rgb(palette,j)
	client.put_pixels(pixels)
