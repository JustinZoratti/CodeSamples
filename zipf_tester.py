file_name = 'EoniaResearchFull.txt'

unallowed_chars = ['.',',',';',':','?','!','\"','(',')','\t','\n','\r','/','…']
unallowed_strings = ['\'s','s\'','- ',' -']

allowed_chars = ['\'','-']

text = []
with open(file_name, 'r') as file:
	for q in file.readlines():
		q = q.replace('“','"').replace('”','"')
		q = q.replace('’','\'').replace('‘','\'')
		q = q.replace('–',' - ')
		if(len(q) > 0):
			text.append(q)

word_list = []
while(len(text) > 0):
	l = text[0]
	del text[0]
	
	l = l.lower()
	for k in unallowed_chars:
		l = l.replace(k,' ')
	for k in unallowed_strings:
		l = l.replace(k,' ')
	
	word_list.extend(l.split(' '))

words = {}
fail_list = []
while(len(word_list) > 0):
	word = word_list[0]
	del word_list[0]
	
	if(len(word) > 0):
		allowed = True
		i = len(word)-1
		while(i >= 0):
			if(not word[i].isalpha()) and (not word[i] in allowed_chars):
				allowed = False
			i -= 1
		
		if(allowed):
			if word in words.keys():
				words[word] += 1
			else:
				words[word] = 1
		else:
			fail_list.append(word)

#print(fail_list)

frequencies = {}
for q in words.keys():
	word_list.append(q)
	if words[q] in frequencies.keys():
		frequencies[words[q]].append(q)
	else:
		frequencies[words[q]] = [q]
word_list.sort()
frequency_list = list(frequencies.keys())
frequency_list.sort(reverse = True)
for f in frequency_list:
	frequencies[f].sort()
max_freq = frequency_list[0]

i = 0
wordshift = '               '
for f in frequency_list:
	for word in frequencies[f]:
		if(i < 200):
			i += 1
			word = word+wordshift[len(word):len(wordshift)]
			print(str(i)+'.\t'+word+str(f)+'\t'+str(int(max_freq/f))+'\t'+str(f/max_freq))
