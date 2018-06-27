from math import sqrt
from csvtodict import csvtodict, writeshortestdistances
import chromomatching
from basicdistancecalc import pointdist, orderedpairs

#finds the minimum distance from B to A and returns an array of dict objects
def pointdistancepairs(A, B):
	totaldistance = 0
	smallestdistance = -1 
	Aymin = 0 
	Aymin = 0
	Bx = 0 
	By = 0  
	Bkey = []
	for i in range(len(B)):
		origin = i+1 
		Bx = B[i][0]
		By = B[i][1]
		for j in range(len(A)):
			distance = pointdist(B[i], A[j])
			if smallestdistance > distance or smallestdistance == -1:
				smallestdistance = distance
				smallestdistancekey = j+1
				Axmin = A[j][0]
				Aymin = A[j][1]
		totaldistance = smallestdistance + totaldistance
		Bkey.append({'origin':origin, 'originx':Bx, 'originy':By, 'link':smallestdistancekey, 'linkx':Axmin, 'linky':Aymin, 'distance':smallestdistance})
		smallestdistance = -1 
	return Bkey

#finds the shortest distance between a set of points, returns the average distance, and all shortest distance key pairs
def shortestdistance(A, B, Achromoinfo = None, Bchromoinfo = None):
	totaldistance = 0 
	swapped = 0
	lenb = len(B)
	lena = len(A)
	#checks if chromo file is present
	if Achromoinfo != None and Bchromoinfo!= None: 
		Achromodistance = Achromoinfo[0]
		Achromoaverage = Achromoinfo[1]
		Bchromodistance = Bchromoinfo[0]
		Bchromoaverage = Bchromoinfo[1]
	#ensures that the longest array of points is matched first
	if lena > lenb:
		Bkey = pointdistancepairs(A, B)
		Akey = pointdistancepairs(B, A)
	else:
		Akey = pointdistancepairs(A, B)
		Bkey = pointdistancepairs(B, A)
		if Achromoinfo != None and Bchromoinfo != None:
			temp = Bchromodistance
			Bchromodistance = Achromodistance
			Achromodistance = temp
			temp = Bchromoaverage
			Bchromoaverage = Achromoaverage
			Achromoaverage = temp
		swapped = 1
	#prepares an array object that writeshortestdistances() can read out to a .csv final
	tempkey = []
	index = 0 
	effectiveBLen = 0 
	for i in range(len(Akey)):
		totaldistance = totaldistance + Akey[i]['distance']
	for i in range(len(Bkey)): 
		if (i+1) == Akey[Bkey[i]['link']-1]['link']:
			Bkey[i]['link'] = "None"
		else:
			totaldistance = totaldistance + Bkey[i]['distance']
			effectiveBLen = effectiveBLen + 1
			tempkey.append({'origin':Bkey[i]['link'], 'originx':Bkey[i]['linkx'], 'originy':Bkey[i]['linky'], 'link':Bkey[i]['origin'], 'linkx':Bkey[i]['originx'], 'linky':Bkey[i]['originy'], 'distance':Bkey[i]['distance']})
	averagedistance = totaldistance/(effectiveBLen + len(A))
	Akey.append(0)
	for i in range(len(tempkey)):
		Akey.append(tempkey[i])
	if Achromoinfo != None and Bchromoinfo != None:
			for i in range(len(Akey)):
				if Akey[i] != 0:
					originchromodistance = Achromodistance[Akey[i]['origin']]
					linkchromodistance = Bchromodistance[Akey[i]['link']]
					Akey[i]["origin chromo distance"] = originchromodistance
					Akey[i]["link chromo distance"] = linkchromodistance
					Akey[i]["average chromo distance"] = (originchromodistance+linkchromodistance)/2
	return(Akey, averagedistance, swapped)

#Examines a file location for it's filename
def examinefilename(filename):
	filelabel = ""
	lastbackslash = 0
	for i in range(len(filename)):
		if filename[i] == "/":
			lastbackslash = i + 1
	while lastbackslash < len(filename)-4:
		filelabel = filelabel + filename[lastbackslash]
		lastbackslash = lastbackslash + 1
	return(filelabel)

#Takes 2 .csv files, and optionally a .tif chromo file, and creates a 3rd that gives all pairs of shortest distance points
def extractAnalyizeData(file1, file2, savedfile, chromofile = None):
	file1_X = csvtodict(file1, 'X')	
	file1_Y = csvtodict(file1, 'Y')
	file2_X = csvtodict(file2, 'X')
	file2_Y = csvtodict(file2, 'Y')	
	#checks to see if a chromo file is present
	if chromofile != None: 
		(Achromodistance, Achromoaverage) = chromomatching.shortestdistanceprotientochromo(file1, chromofile)
		(Bchromodistance, Bchromoaverage) = chromomatching.shortestdistanceprotientochromo(file2, chromofile)

	file1_pairs = orderedpairs(file1_X, file1_Y)
	file2_pairs = orderedpairs(file2_X, file2_Y)
	#checks to see if a chromo file is present
	if chromofile == None:
		(key1, averagedistance, swapped) = shortestdistance(file1_pairs, file2_pairs)
	else: 
		(key1, averagedistance, swapped) = shortestdistance(file1_pairs, file2_pairs, (Achromodistance, Achromoaverage), (Bchromodistance, Bchromoaverage))
	file1name = examinefilename(file1)
	file2name = examinefilename(file2)
	#checks to see if values were swapped during shortestdistance() and if a chromo file is present
	if swapped == 0:
		if chromofile == None:
			writeshortestdistances(key1, averagedistance, file1name, file2name, savedfile)
		else: 
			writeshortestdistances(key1, averagedistance, file1name, file2name, savedfile, 'exists')
	else:
		if chromofile == None:
			writeshortestdistances(key1, averagedistance, file2name, file1name, savedfile)
		else: 
			writeshortestdistances(key1, averagedistance, file2name, file1name, savedfile, 'exists')