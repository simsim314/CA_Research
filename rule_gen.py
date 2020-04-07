import golly as g
import random

def rand_rule(prob):

	isotropicsetS = isotropicsetB = {"0",
					 "1c", "1e",
					 "2c", "2e", "2k", "2a", "2i", "2n",
					 "3c", "3e", "3k", "3a", "3i", "3n", "3y", "3q", "3j", "3r",
					 "4c", "4e", "4k", "4a", "4i", "4n", "4y", "4q", "4j", "4r", "4t", "4w", "4z",
					 "5c", "5e", "5k", "5a", "5i", "5n", "5y", "5q", "5j", "5r",
					 "6c", "6e", "6k", "6a", "6i", "6n",
					 "7c", "7e",
					 "8"}
	
	isotropicsetB.remove("2a")
	isotropicsetB.remove("0")
	
	rulestr = "B"

	for i in isotropicsetB:
		if random.random() > prob:
			rulestr += i

	rulestr = rulestr + "/S"

	for i in isotropicsetS:
		if random.random() > prob:
			rulestr += i

	g.setrule(rulestr)

def rule_boring():
	explode = 0 
	die = 0 
	num_trial = 8
	
	for i in range(num_trial):
		g.new("")
		g.select([0,0,32,32])
		g.randfill(50)
		
		g.run(16)
		
		if int(g.getpop()) == 0:
			die += 1
			continue 
			
		r = g.getrect()
		
		if r[2] > 60 and r[3] > 60:
			explode += 1
			continue
		
		return -1 
			
	if explode == num_trial: 
		return 0 
		
	if die == num_trial:
		return 1
		
	return -1

def calc_p_boring(p_rule):
	boring_explode = 0 
	boring_die = 0 
	
	for i in range(1000):

		g.show(str(i))

		rand_rule(p_rule)
		bor = rule_boring()
		
		if bor == 0:
			boring_explode += 1
		
		if bor == 1:
			boring_die += 1
			
		if bor == -1:
			g.exit()
			
	return (boring_explode, boring_die)
	

def getwhp():
	bbox = g.getrect()
		
	if len(bbox) == 0:
		return 0,0,0

	return bbox[2], bbox[3], int(g.getpop())
		
def fail_cd():
	num_trial = 5
	status = [0, 0, 0, 0] 
	
	for i in range(num_trial):
		g.new("")
		g.select([0,0,32,32])
		g.randfill(50)
		
		ws = [] 
		hs = [] 
		pop = [] 
		
		for i in range(20):
			g.run(120)
			w, h, p = getwhp()
			ws.append(w)
			hs.append(h)
			pop.append(p)
		
		dw = ws[19] - ws[18]
		dh = hs[19] - hs[18]
		
		if dw < 3 and dh < 3:
			status[2] += 1 
			continue 
		
		if len(g.getcells([-64, -64, 128, 128])) == 0:
			status[1] += 1 
			continue 
		
		fail = False 
		
		for i in range(14, 19):
			if abs(pop[19] - pop[i]) > 25:
				status[0] += 1 
				fail = True 
				break
		
		if fail:
			continue
		
		for i in range(10, 20):
			w = ws[i] - ws[i - 1]
			
			if abs(dw - w) > 4:
				fail = True
				status[3] += 1
				break
		
		if not fail:
			return -1 
			
		for i in range(10, 20):
			h = hs[i] - hs[i - 1]
			
			if abs(dh - h) > 4:
				fail = True
				break
		
		if not fail:
			return -1 
	
	maxi = -1 
	maxv = 0 
	
	for i in range(4):
		if status[i] > maxv:
			maxi = i 
			maxv = status[i]
	
	return maxi 
	
def explode_dense():
	
	num_trial = 2

	for i in range(num_trial):
		g.new("")
		g.select([0,0,32,32])
		g.randfill(50)
		
		g.run(128)
		
		total = 0 
		
		for i in range(32):
			total += len(g.getcells([0,0,32,32])) / 2
			g.run(32)
			
		total /= 32
		
		if total >= 300:
			return True 
		
	return False 
		
#g.show(str(calc_p_boring(0.83)))

found = 0 
fail_reasons = [0,0,0,0,0,0,0]

for i in range(10000000): 
	p_rule= 0.6

	rand_rule(p_rule)
	bor = rule_boring()
	
	if bor != -1:
		fail_reasons[bor] += 1
	else:
		if explode_dense():
			fail_reasons[2] += 1 
			continue
			
		status = fail_cd()
		if status == -1:
			found += 1 
			g.show(str([fail_reasons, found, i]))
			g.reset()
			g.save("../../rule_gen/CA{0}.rle".format(found), "rle", True)
		else:
			fail_reasons[3 + status] += 1