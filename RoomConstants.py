import numpy as np

class House():
	RGB_map = [[0,1,2],
			   [0,1,2],
			   [0,1,2],
			   [0,1,2],
			   [0,1,2],
			   [0,1,2],
			   [0,1,2],
			   [0,1,2]]

	sky = []
	splash = []
	grnd = []
	allstrips = list(range(0,64*8))

	grid_map = np.array([[-1 for x in range(32)] for y in range(128)],dtype=object)

	def add_strip_to_grid_map(self,strip,start_pos,direction_uvec,rev):
		if rev:
			strip = reversed(strip)
		count = 0
		for indx in strip:
			new_pos = [start_pos[0]+count*direction_uvec[0], \
				start_pos[1]+count*direction_uvec[1]]
			if self.grid_map[new_pos[0]][new_pos[1]] == -1:
				self.grid_map[new_pos[0]][new_pos[1]] = indx
			else:
				if not isinstance(self.grid_map[new_pos[0]][new_pos[1]],list):
					self.grid_map[new_pos[0]][new_pos[1]] = [self.grid_map[new_pos[0]][new_pos[1]]]
				self.grid_map[new_pos[0]][new_pos[1]].append(indx)
			count += 1

	def __init__(self,init_grid_map):
		init_grid_map()

	def get_RGB_order(self,position):
		i = 0
		match = -1
		for RGB in self.RGB_map:
			start = i * 64
			stop = (i+1)*64
			if position >= start and position < stop:
				match = i
				break
			i += 1
		if match == -1:
			return -1
		return self.RGB_map[match]		


class Washington(House):
	#strips = [64,29,64,20,10,9,0,0]
	skyA = list(range(0,30))
	skyB = list(range(30,54))
	skyC = list(range(65,103))

	splashA = list(range(64*2,64*2+20))
	splashB = list(range(64*2+20,64*2+27))
	splashC = list(range(64*2+27,64*2+45))
	splashD = list(range(64*3+36,64*3+32,-1))
	splashE = list(range(64*3+11,64*3-1,-1))
	splashF = list(range(64*3+32,64*3+23,-1))
	splashG = list(range(64*3+23,64*3+12,-1))

	bed = list(range(64*4,64*4+35))
	desk = list(range(64*5,64*5+40))

	def init_grid_map(self):
		super().add_strip_to_grid_map(self.skyC,[4,0],[1,0],True)
		super().add_strip_to_grid_map(self.skyB,[42,0],[1,0],True)
		super().add_strip_to_grid_map(self.skyA,[76,0],[1,0],True)
		super().add_strip_to_grid_map(self.splashA,[67,6],[0,1],True)
		super().add_strip_to_grid_map(self.splashB,[66,5],[-1,0],False)
		super().add_strip_to_grid_map(self.splashC,[59,6],[0,1],False)
		super().add_strip_to_grid_map(self.splashD,[58,13],[-1,0],False)
		super().add_strip_to_grid_map(self.splashE,[54,15],[0,1],False)
		super().add_strip_to_grid_map(self.splashF,[53,13],[-1,0],False)
		super().add_strip_to_grid_map(self.splashG,[69,15],[0,1],False)
		super().add_strip_to_grid_map(self.desk[:7],[60,25],[1,0],False)
		super().add_strip_to_grid_map(self.desk[7:],[68,25],[1,0],False)
		super().add_strip_to_grid_map(self.bed,[0,27],[1,0],True)

	def __init__(self):
		self.sky = self.skyA + self.skyB + self.skyC

		self.splash =  self.splashA + self.splashB + self.splashC + \
			self.splashD + self.splashE + self.splashF + self.splashG
		
		self.grnd = self.desk + self.bed

		self.allstrips = self.sky + self.splash + self.grnd

		super().__init__(self.init_grid_map)

class State(House):

	RGB_map = [[2,0,1],
			   [0,1,2],
			   [2,0,1],
			   [0,1,2],
			   [2,0,1],
			   [2,0,1],
			   [0,1,2],
			   [0,1,2]]

	splashA = list(range(0,29))
	splashB = list(range(64,64+47))
	splashC = list(range(64*3,64*3+27))
	splashD = list(range(64*4,64*4+23))
	splashE = list(range(64*5,64*5+23))

	desk = list(range(64*2,64*2+37+23))

	def init_grid_map(self):
		print('init grid map')
		super().add_strip_to_grid_map(self.splashA[:19],[0,20],[0,-1],False)
		super().add_strip_to_grid_map(self.splashA[20:],[1,0],[1,0],False)
		super().add_strip_to_grid_map(self.splashB[:19],[10,20],[0,-1],False)
		super().add_strip_to_grid_map(self.splashB[20:26],[11,0],[1,0],False)
		super().add_strip_to_grid_map(self.splashB[27:],[18,1],[0,1],False)
		super().add_strip_to_grid_map(self.splashC[:19],[26,20],[0,-1],False)
		super().add_strip_to_grid_map(self.splashC[20:],[25,0],[-1,0],False)
		super().add_strip_to_grid_map(self.splashD[:15],[34,20],[0,-1],False)
		super().add_strip_to_grid_map(self.splashD[16:],[33,4],[-1,0],False)
		super().add_strip_to_grid_map(self.splashE[:15],[42,20],[0,-1],False)
		super().add_strip_to_grid_map(self.splashE[16:],[41,4],[-1,0],False)
		super().add_strip_to_grid_map(self.desk[:14],[11,15],[0,0],False)
		super().add_strip_to_grid_map(self.desk[15:21],[11,15],[1,0],False)
		super().add_strip_to_grid_map(self.desk[22:],[17,15],[1,0],False)

	def __init__(self):
		self.splash = self.splashA + self.splashB + self.splashC + \
			self.splashD + self.splashE

		self.grnd = self.desk

		self.allstrips = self.splash + self.grnd

		super().__init__(self.init_grid_map)

curr_house = State()