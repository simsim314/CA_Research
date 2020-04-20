import random
import golly as g 
import pickle
import os 

factor = 0.82
rule_flag = [random.uniform(0, 1) > factor for i in range(1638)]

def ruleTotal(n27):
	sumT = sum(n27)
	
	if sumT < 3:
		return 0 
		
	idx = sumT + 28 * n27[13]
	
	if rule_flag[idx]:
		return 1 
	else:
		return 0 
	
def init_flags():
	global rule_flag 
	rule_flag = [random.uniform(0, 1) > factor for i in range(1638)]


def sumidx(n27, idxs):
	total = 0 
	
	for id in idxs:
		total += n27[id]
		
	return total 
	
def ruleFEV(n27):
	global rule_flag
	
	F = [4, 10, 12, 14, 16, 22]
	V = [0, 2, 6, 8, 18, 20, 24, 26]
	E = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
	
	Ft = sumidx(n27, F)
	Vt = sumidx(n27, V)
	Et = sumidx(n27, E)
	
	if Ft + Vt + Et < 3:
		return 0 
		
	idx = Ft + 7 * Vt + 63 * Et + n27[13] * 819
	
	if rule_flag[idx]:
		return 1 
	else:
		return 0 
		
		
class CA3d:
	def __init__(self, rule):
		self.cur_state = {}
		self.rule = rule 
		self.n27 = [0 for i in range(27)]
		self.v = None
		
	def rand_fill(self, r):
		for x in range(r):
			for y in range(r):
				for z in range(r):
					if random.uniform(0, 1) > 0.5:
						self.cur_state[(x, y, z)] = 1
	
		
	def set_val(self, x, y, z, v):
		self.cur_state[(x, y, z)] = v 
			
	def set_state(self, arr):
		for x, y, z, v in input:
			self.cur_state[(x, y, z)] = v 
		
	def clear(self):
		self.cur_state = {}
	
	def apply(self):
		return self.rule(self.n27)
	
	def run(self, n):
		for i in range(n):
			self.evolve()
			
	def evolve(self):

		checked = set()
		next_vals = {}
		
		for (k, v) in self.cur_state.items():
			x, y, z = k
			
			for i in range(-1, 2):
				for j in range(-1, 2):
					for k in range(-1, 2):
						cur_key = (x + k, y + j, z + i)
						
						if not (cur_key in checked):
							checked.add(cur_key)
							
							v = self._calc_next(cur_key)
							
							if v != 0:
								next_vals[cur_key] = v
								
		self.cur_state = next_vals
							
	def _calc_next(self, loc):
		x, y, z = loc
		idx = 0 
		for i in range(-1, 2):
			for j in range(-1, 2):
				for k in range(-1, 2):
					cur_key = (x + k, y + j, z + i)
					
					if cur_key in self.cur_state:
						self.n27[idx] = self.cur_state[cur_key]
					else:
						self.n27[idx] = 0
					
					idx += 1 
					
		return self.apply()
		
	'''def show_cloud(self):
		n = len(self.cur_state)
		
		vec = np.zeros((n, 3))
		
		for i, (k, v) in enumerate(self.cur_state.items()):
			x, y, z = k
			vec[i][0] = x
			vec[i][1] = y
			vec[i][2] = z
	'''
	def density(self, r):
		inr = 0
		
		for (k, v) in self.cur_state.items():
			x, y, z = k
			
			if x >= 0 and x < r and y >= 0 and y < r and z >= 0 and z < r:
				inr += 1
				
		return float(inr) / (r**3)
		
	def draw(self):
		
		xy = [] 
		xz = [] 
		yz = [] 
		proj = []
		
		for (k, v) in self.cur_state.items():
			x, y, z = k
			
			xy.append(x)
			xy.append(y)
			
			xz.append(x + 128)
			xz.append(z)
			
			yz.append(y)
			yz.append(z + 128)
		
			proj.append(x + y + z + 128)
			proj.append(- x + y + z + 128)
			
		if len(g.getrect()) > 0:
			g.select(g.getrect())
			g.clear(0)
			g.select([])
		
		g.putcells(xy)
		g.putcells(xz)
		g.putcells(yz)
		g.putcells(proj)
		g.setpos("64", "64")
		g.setmag(1)
		g.update()
		
	def get_box(self):
		xmin = 1000000
		ymin = 1000000
		zmin = 1000000
		xmax = -1000000
		ymax = -1000000
		zmax = -1000000
		
		for (k, v) in self.cur_state.items():
			x, y, z = k
			xmin = min(x, xmin)
			ymin = min(y, ymin)
			zmin = min(z, zmin)
			xmax = max(x, xmax)
			ymax = max(y, ymax)
			zmax = max(z, zmax)
			
		return (xmin, ymin, zmin, xmax, ymax, zmax)
	
	def get_mm(self):
		xmin, ymin, zmin, xmax, ymax, zmax = self.get_box()
		
		return min(xmin, ymin, zmin), max(xmax, ymax, zmax) 
		
	def get_pop(self):
		return len(self.cur_state)


def is_exploding(testCA):
	testCA.rand_fill(10)
	
	fail = True 
	
	for i in range(4):
	
		testCA.run(1)
		mi, ma = testCA.get_mm()
		if not (mi == -i - 1 and ma == 10 + i + 1):
			fail = False 
			break 
			
	if fail:
		return True 
	
	fail = True 
		
	for i in range(5):
		testCA.run(1)
		
		if testCA.density(10) < 0.1:
			fail = False 
	
	if fail or testCA.get_pop() == 0:
		return True 
	
	return False 
	
def is_stable(testCA):
	testCA.rand_fill(10)
	testCA.run(12)
		
	for j in range(60):

		testCA.run(1)
		
		if testCA.get_pop() > 150 or testCA.get_pop() == 0:
			return True 
	
	if testCA.get_pop() > 100 or testCA.get_pop() == 0:
		return True 
		
	mi0, ma0 = testCA.get_mm()	
	testCA.run(12)	
	mi1, ma1 = testCA.get_mm()
	
	if mi0 == mi1 and ma0 == ma1:
		return True 
	else: 
		return False 

stablecnt = 0 
explodecnt = 0 
rule_cnt = 0 

if not os.path.exists(os.path.join(g.getdir("files"), '3d')):
    os.makedirs(os.path.join(g.getdir("files"), '3d'))
	
for iter in range(1000000):
	init_flags()
	testCA = CA3d(ruleFEV)
	
	if is_exploding(testCA):
		explodecnt += 1 
		g.show(str((stablecnt, explodecnt)))
		g.update()
		continue
	
	fail = True 
	
	for i in range(3):
		if not is_stable(testCA):
			fail = False 
			break 
			
	if fail:
		stablecnt += 1
		g.show(str((stablecnt, explodecnt)))
		g.update()
		continue
	
	with open(os.path.join(g.getdir("files"), '3d/rule{0}.pkl'.format(rule_cnt)), 'w+') as pickle_out:
		pickle.dump(rule_flag, pickle_out)
		rule_cnt += 1
		
	testCA.clear()
	testCA.rand_fill(10)
	testCA.run(5)

	for i in range(250):
		testCA.run(1)

		mi, ma = testCA.get_mm()
		testCA.draw()
		
		if testCA.get_pop() > 400 or testCA.get_pop() == 0:
			break
		