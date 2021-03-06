from CommonPatterns import *
import numpy as np

class Gradient():
	def __init__(self,label,points,blend="poly"):
		self.label = label
		self.points = points
		self.blend = blend

	# between 0 and 1
	def get_color(self,pos):
		for j in range(len(self.points)):
			if self.points[j][0] == pos:
				return self.points[j][1], self.points[j][2], self.points[j][3]
			if self.blend == "poly":
				points = np.array(self.points)
				poly = np.polyfit(points[:,0],points[:,1:])
				r, g, b = np.polyval(poly,pos)
				return r, g, b
			elif self.blend == "linear":
				if self.points[j][0] <= pos and pos < self.points[j+1][0]:
					progress = (pos - self.points[j][0]) / (self.points[j+1][0] - self.points[j][0])
					r = ((1-progress)*self.points[j][1] + progress*self.points[j+1][1])/2
					g = ((1-progress)*self.points[j][2] + progress*self.points[j+1][2])/2
					b = ((1-progress)*self.points[j][3] + progress*self.points[j+1][3])/2
					return r, g, b
				

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

grad_caesar = Gradient('Caesar', pe_caesar)

def pe_rush(b):
	return hsv2points([[0,360-251,.83,b],\
			   [27,360-359,.71,b]])

grad_rush = Gradient('Rush', pe_rush)

def pe_grapefruit(b):
	return hsv2points([[0,360-275,.35,b],\
			   [13.360-20,.875,b],\
			   [27,360-12,.879,b]])

grad_grapefruit = Gradient('Grapefruit', pe_grapefruit)

grad_list = [grad_caesar,
			 grad_rush,
			 grad_grapefruit]