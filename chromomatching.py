import numpy
from PIL import Image
from math import floor, sqrt
import csvtodict
from basicdistancecalc import pointdist, orderedpairs



#This section is a test for finding the closest points to a chromosome
#gridtopoint, given an x,y grid locaiton, returns the center of the grid as a point
def gridtopoint(XY):
	X = XY[0]
	Y = XY[1]
	X = X + .5
	Y = Y + .5
	return(X,Y)

#pointtogrid, given a point, return which grid it belows to
def pointtogrid(XY):
	X = XY[0]
	Y = XY[1]
	X = floor(X)
	Y = floor(Y)
	return(X,Y)

#given an location on an XYgrid, how many layers the shell is, and an X and Y max, will return points in a shell that is layer away from the XYgrid
def gridshell(XYgrid, layer, Xmax, Ymax):
	shell = []
	X = XYgrid[0] 
	Y = XYgrid[1] 
	for i in [-layer, layer]:
		for j in range(-layer, layer+1):
			if X+j >= 0 and Y+i >=0 and X + j < Xmax and Y + i < Ymax: 
				shell.append((X+j, Y+i))
	for i in range(-layer+1, layer):
		for j in [-layer, layer]:
			if X+j >= 0 and Y+i >=0 and X + j < Xmax and Y + i < Ymax: 
				shell.append((X+j, Y+i))
	return(shell)

#given a protien and chromo file, will return the distance for each point, as well as the average distance, between the chromo and protien
def shortestdistanceprotientochromo(protienfile, chromofile):
	im = Image.open(chromofile)

	imarray = numpy.array(im)

	Xprotien = csvtodict.csvtodict(protienfile, 'X')
	Yprotien = csvtodict.csvtodict(protienfile, 'Y')

	protienpoints = orderedpairs(Xprotien, Yprotien)
	protiengrid = []
	tempprotiengrid = 0


	for i in range(len(protienpoints)):
		tempprotiengrid = pointtogrid(protienpoints[i])
		protiengrid.append(tempprotiengrid)

	#set variables
	tempshortestdistance = 0 
	shortestdistance = -2
	totaldistance = 0 
	maxdistanceforloopstop = 0
	distanceforeachpoint = ["None"]

	for i in range(len(protiengrid)):
		Ygrid = protiengrid[i][1] 
		Xgrid = protiengrid[i][0]
		Ypoint = protienpoints[i][1]
		Xpoint = protienpoints[i][0]
		#if the point is on a grid that also contains a chromo
		if imarray[Xgrid, Ygrid] == 0: 
			shortestdistance = pointdist((Xpoint, Ypoint), (Xgrid + .5, Ygrid +.5))
		#else, expand outwards and search increasingly large shells for a chromo
		else: 
			z = 1
			while maxdistanceforloopstop > (z-.5) or maxdistanceforloopstop == 0: 
				shell = gridshell(protiengrid[i], z, len(imarray), len(imarray[0]))
				for j in range(len(shell)): 
					shellX = shell[j][0]
					shellY = shell[j][1]
					#if the point contains a chromo
					if imarray[shellX, shellY] == 0:
						shellpoint = gridtopoint(shell[j])
						tempshortestdistance = pointdist(shellpoint, protienpoints[i])
						#sets the shortest distance to chromo
						if tempshortestdistance < shortestdistance or shortestdistance == -2:
							shortestdistance = tempshortestdistance
							#sets the stop condition to ensure the closest chromo match to protien is found
							if maxdistanceforloopstop == 0:
								maxdistanceforloopstop = shortestdistance
				#increase layers of shell
				z = z + 1
		#append results
		distanceforeachpoint.append(shortestdistance)
		totaldistance = shortestdistance + totaldistance
		#reset variables
		shortestdistance = -2
		maxdistanceforloopstop = 0
	averagedistance = totaldistance/len(protienpoints)
	return(distanceforeachpoint, averagedistance)

