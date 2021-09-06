from common_patterns import *

def hsv2points(hsvarr):
	output = [[0 for i in range(len(hsvarr))] for j in range(4)]
	i = 0
	for j in range(len(hsvarr)):
		ent = hsvarr[j]
		output[0][i] = ent[0]
		rgb = hsv2rgb(ent[1],ent[2],ent[3])
		output[1][i] = rgb[0]
		output[2][i] = rgb[1]
		output[3][i] = rgb[2]
		i = i +1
	return output

def pe_caesar(b):
	return hsv2points([[27,360-356,.77,b],\
			   [0,360-248,.62,b]])
def pe_rush(b):
	return hsv2points([[0,360-251,.83,b],\
			   [27,360-359,.71,b]])

def pe_grapefruit(b):
	return hsv2points([[0,360-275,.35,b],\
			   [13.360-20,.875,b],\
			   [27,360-12,.879,b]])
