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

bed = list(range(64*4,64*4+35))
desk = list(range(64*5,64*5+40))
grnd = desk + bed

allstrips = sky + splash + grnd

grid_map = [[-1 for x in range(32)] for y in range(128)]

def add_strip_to_grid_map(strip,start_pos,direction_uvec,rev):
	if rev:
		strip = reversed(strip)
	count = 0
	for indx in strip:
		new_pos = [start_pos[0]+count*direction_uvec[0], \
			   start_pos[1]+count*direction_uvec[1]]
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