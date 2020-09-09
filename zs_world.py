import random
import os
import math

max_iterations = 500
max_population = 5000
total_cash = 1024
income_tax_rate = 0.05
wealth_tax_rate = 0.05
government_assistance = True
show_dynamic_results = True

economy = 0
deconomy = 0
ddeconomy = 0
lreconomy = 2*random.random()-1

deaths = 0
total_lifespan = 0
tax_revenue = 0
net_inheritance = 0
mean_wealth = 0
stddev_wealth = 0
brackets = {}
for i in range(9):
	brackets[i+1] = 0
history = []
#history.append(['population','stddev_wealth','tax_revenue','net_inheritance','economy','deconomy','ddeconomy','lreconomy'])

denizens = {}
people = []
free_ids = []
min_id = 4

denizens[0] = [20,256,[],None]
denizens[1] = [20,256,[],None]
denizens[2] = [20,256,[],None]
denizens[3] = [20,256,[],None]
people.append(0)
people.append(1)
people.append(2)
people.append(3)

#[age, money, descendants, parent]

def sqr(x):
	return x*x

def sign(x):
	if(x > 0):
		return 1
	elif(x < 0):
		return -1
	else:
		return 0

def print_all():
	global mean_wealth, stddev_wealth
	
	mean_wealth = 0
	for q in people:
		mean_wealth += denizens[q][1]
	mean_wealth /= max(1,len(people))
	stddev_wealth = 0
	for q in people:
		stddev_wealth += sqr(mean_wealth-denizens[q][1])
	stddev_wealth /= max(1,len(people))
	stddev_wealth = math.sqrt(stddev_wealth)
	
	for k in brackets.keys():
		brackets[k] = 0
	for q in people:
		if(denizens[q][1] > 0):
			ind = int(math.log(denizens[q][1],4))
		else:
			ind = 1
		ind = min(max(ind,1),9)
		brackets[ind] += 1
	
	history.append([len(people),stddev_wealth,economy,brackets[1],brackets[2],brackets[5],brackets[6]])
	if(not show_dynamic_results):
		return
	
	os.system('cls')
	for k in brackets.keys():
		print('bracket '+str(k)+': '+str(brackets[k]))
	print()
	print('population: '+str(len(people)))
	print('lifespan: '+str(int(total_lifespan/max(deaths,1))))
	#print('mean_wealth: '+str(int(mean_wealth)))
	print('stddev_wealth: '+str(int(stddev_wealth)))
	print('tax_revenue: '+str(tax_revenue))
	print('net_inheritance: '+str(net_inheritance))
	print()
	print('economy: '+str(economy))
	print('deconomy: '+str(deconomy))
	print('ddeconomy: '+str(ddeconomy))
	print('lreconomy: '+str(lreconomy))

def get_id():
	global min_id
	if(len(free_ids) == 0):
		min_id += 1
		return min_id-1
	result = free_ids[0]
	del free_ids[0]
	return result

def breed(parent):
	child = get_id()
	
	amnt = int(0.25*denizens[parent][1])
	denizens[parent][1] -= amnt
	child_data = [0,amnt,[],parent]
	
	denizens[child] = child_data
	denizens[parent][2].append(child)
	people.append(child)

def try_breed(person):
	threshold = 1-(max_population*1.5-len(people))/(30*len(people))
	threshold = max(threshold,0.8)
	for i in range(len(denizens[person][2])):
		threshold = (1+2*threshold)/3
	if(random.random() > threshold):
		breed(person)
		return True
	return False

def kill(person):
	global tax_revenue, net_inheritance, deaths, total_lifespan
	deaths += 1
	total_lifespan += denizens[person][0]
	
	descendants = denizens[person][2]
	if(len(descendants) > 0):
		amnt = denizens[person][1]
		net_inheritance += amnt
		amnt /= len(descendants)
		amnt = int(amnt)
		for q in descendants:
			denizens[q][1] += amnt
			denizens[person][1] -= amnt
			denizens[q][3] = None
	tax_revenue += denizens[person][1]
	
	if(denizens[person][3] != None):
		denizens[denizens[person][3]][2].remove(person)
	
	denizens[person][2] = []
	people.remove(person)
	free_ids.append(person)

def try_kill(person):
	#threshold = pow(1.01,-denizens[person][0])
	#threshold += 0.2+0.3*(1-pow(1.5,-denizens[person][1]))
	#base^(-100) = 0.5; base = 100th root of 2 = 1.007
	
	#threshold = pow(1.007,-denizens[person][0])*0.02+0.98
	threshold = pow(1.007,-denizens[person][0])+0.3
	
	#print('threshold: '+str(threshold))
	"""
	wealth_offset = 1-pow(1.2,-denizens[person][1]/256)
	wealth_offset *= 0.3
	
	threshold = wealth_offset+(1-wealth_offset)*threshold
	#print('\t'+str(threshold))
	"""
	if(denizens[person][1] > 256): #access to healthcare
		threshold = (1+threshold)/2
	else:
		threshold += max(min(0,economy)*0.015,-0.015)
	
	if(denizens[person][0] > 120) or (random.random() > threshold):
		kill(person)
		return True
	return False

def age():
	global net_inheritance
	net_inheritance = 0
	i = len(people)-1
	while(i >= 0):
		pid = people[i]
		pid = denizens[pid]
		pid[0] += 1
		if(not try_kill(people[i])) and (pid[0] >= 20) and (pid[0] <= 50):
			try_breed(people[i])
		i -= 1

def income():
	global lreconomy, ddeconomy, deconomy, economy, tax_revenue
	if(random.random() < 0.04):
		lreconomy = 2*random.random()-0.5
	ddeconomy = (-economy+3*lreconomy)/4+0.35*(random.random()-0.5)
	deconomy += ddeconomy/4+0.15*(random.random()-0.5)
	economy += deconomy/4
	if(abs(economy) > 1):
		economy = 0.998*economy
	
	effective_economy = max(min(economy,0.5),-0.5)
	
	for q in people:
		delta = random.random()-0.1
		delta += effective_economy
		delta *= max(1,denizens[q][1]*0.2)
		
		if(delta > 0) and (income_tax_rate != 0):
			tax_revenue += income_tax_rate*delta
			delta -= income_tax_rate*delta
		
		denizens[q][1] = max(0,denizens[q][1]+delta)

def tax():
	global tax_revenue
	for q in people:
		amnt = wealth_tax_rate*denizens[q][1]
		tax_revenue += amnt
		denizens[q][1] -= amnt

def ubi():
	if(len(people) == 0):
		return
	amnt = tax_revenue/len(people)
	for q in people:
		denizens[q][1] += amnt

def zero_sum():
	global total_cash
	total = 0
	for q in people:
		total += denizens[q][1]
	total = max(total,1)
	total_cash = max(total_cash, 256*len(people))
	scal = total_cash/total
	for q in people:
		denizens[q][1] = int(scal*denizens[q][1])

def time_step():
	global tax_revenue
	tax_revenue = 0
	age()
	income()
	if(wealth_tax_rate != 0):
		tax()
	if(government_assistance):
		ubi()
	zero_sum()
	print_all()



year = 0
while(len(people) > 0) and (year < max_iterations):
	time_step()
	year += 1

for i in range(len(history[0])):
	minf = 0
	maxf = 0
	for q in history:
		minf = min(minf,q[i])
		maxf = max(maxf,q[i])
	scal = maxf-minf
	if(scal > 0):
		scal = 1000*(len(history[0])-i)/scal
	for q in history:
		q[i] = (q[i]-minf)*scal

with open('history.csv','w') as file:
	for k in history:
		for q in k:
			file.write(str(q))
			file.write(',')
		file.write('\n')
