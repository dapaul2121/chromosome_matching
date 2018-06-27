import csv 

#converts csv files to python arrays
def csvtodict(filepath, variable):
	counter = 0 
	counterstop = 0
	header = 1
	values = []
	with open(filepath, newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			for item in row: 
				counter = counter + 1
				if header == 0 and counter == counterstop:
					values.append(float(item))
					counter = 0 
					break
				if header == 1 and item == variable:
					header = 0
					counterstop = counter
					counter = 0
					break
	return values

#writes .csv files after calculations have been done
def writeshortestdistances(finalkey, averagedistance, file1name, file2name, savedfile, chromofile = None):
	with open(savedfile, 'w', newline = '') as myfile:
		wr = csv.writer(myfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		wr.writerow(["These pairs are the shortest distance between " + file1name + " and " + file2name])
		if chromofile == None: 
			wr.writerow([file1name + ' ID', file1name + ' X', file1name + ' Y', file2name + ' ID', file2name + ' X', file2name + ' Y', 'distance between'])
			for i in range(len(finalkey)):
				if finalkey[i] == 0:
					wr.writerow("")
					wr.writerow(["These pairs are the shortest distance between " + file2name + " and " + file1name + "that are not repeats of the sets above"])
					wr.writerow([file1name + ' ID', file1name + ' X', file1name + ' Y', file2name + ' ID', file2name + ' X', file2name + ' Y', 'distance between'])
				else:
					wr.writerow([finalkey[i]['origin'], finalkey[i]['originx'], finalkey[i]['originy'], finalkey[i]['link'], finalkey[i]['linkx'], finalkey[i]['linky'], finalkey[i]['distance']])
		else:
			wr.writerow([file1name + ' ID', file1name + ' X', file1name + ' Y', file2name + ' ID', file2name + ' X', file2name + ' Y', 'distance between', '', file1name + ' distance to chromo', file2name + ' distance to chromo', 'average distance to chromo'])
			for i in range(len(finalkey)):
				if finalkey[i] == 0:
					wr.writerow("")
					wr.writerow(["These pairs are the shortest distance between " + file2name + " and " + file1name + "that are not repeats of the sets above"])
					wr.writerow([file1name + ' ID', file1name + ' X', file1name + ' Y', file2name + ' ID', file2name + ' X', file2name + ' Y', 'distance between', '', file1name + ' distance to chromo', file2name + ' distance to chromo', 'average distance to chromo'])
				else:
					wr.writerow([finalkey[i]['origin'], finalkey[i]['originx'], finalkey[i]['originy'], finalkey[i]['link'], finalkey[i]['linkx'], finalkey[i]['linky'], finalkey[i]['distance'], '', finalkey[i]['origin chromo distance'], finalkey[i]['link chromo distance'], finalkey[i]['average chromo distance']])
