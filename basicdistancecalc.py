from math import sqrt

#returns the distances betwen two points
def pointdist(A, B):
	x1 = A[0]
	x2 = B[0]
	y1 = A[1]
	y2 = B[1]
	distance = sqrt((x1-x2)**2 + (y1-y2)**2)
	return(distance)

#creates ordered pairs from an X list and Y list
def orderedpairs(X, Y):
	orderedpairslist = []
	if len(X) != len(Y):
		return("Arrays not the same length")
	else:
		for i in range(len(X)):
			orderedpairs = (X[i], Y[i])
			orderedpairslist.append(orderedpairs)
	return(orderedpairslist)