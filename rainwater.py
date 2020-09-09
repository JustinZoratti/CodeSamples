import random

def max_fill_rec(l):
	print(l)
	if(len(l) <= 2):
		#print(0)
		return 0
	maxind = None
	smaxind = None
	for i in range(len(l)):
		if((maxind == None) or (l[i] > l[maxind])):
			smaxind = maxind
			maxind = i
		elif((smaxind == None) or (l[i] > l[smaxind])):
			smaxind = i
	i = min(maxind, smaxind)
	stop = max(maxind, smaxind)
	sum = max_fill_rec(l[0:i+1])
	print(l[i:stop+1])
	sum += max_fill_rec(l[stop:len(l)])
	i += 1
	while i < stop:
		sum += l[smaxind]-l[i]
		i += 1
	#print(sum)
	return sum

def max_fill_linear(l):
	lmax = []
	rmax = []
	
	val = 0
	i = 0
	while i < len(l):
		if(l[i] > val):
			val = l[i]
		lmax.append(val)
		i += 1
	
	val = 0
	i = len(l)-1
	while i >= 0:
		if(l[i] > val):
			val = l[i]
		rmax.insert(0,val)
		i -= 1
	
	print(lmax)
	print(rmax)
	
	sum = 0
	i = 0
	while i < len(l):
		sum += min(lmax[i],rmax[i])-l[i]
		i += 1
	return sum

def test():
	bars = []
	i = random.randint(1,100)
	while(i > 0):
		bars.append(random.randint(0,20))
		i -= 1
	print(bars)
	print()
	print(max_fill_rec(bars))
	print()
	print(max_fill_linear(bars))

test()
