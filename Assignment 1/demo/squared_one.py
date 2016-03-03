import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

# consider C: NxN = A: NxN * B: NxN
# in this problem, we assume N = 5

# use one-phase only
# one reducer per element of C, doing multiplcation and addition
# mapper sends required elements to each reducer for the computation

def mapper(record):
    # get matrix element
    ind1 = record[0]
    ind2 = record[1]
    value = record[2]
    ##print 'mapper input:', ind1, ind2, value

    # send to reducer(ind1, k) where k iterates over columns of C
    for k in range(0,5):
	mr.emit_intermediate((ind1, k), ('a', ind1, ind2, value))
	##print '\tsend to reducer:', (ind1, k)
    
    # send to reducer(i, ind2) where i iterates over rows of C
    for i in range(0,5):
	mr.emit_intermediate((i, ind2), ('b', ind1, ind2, value))
	##print '\tsend to reducer:', (i, ind2)

def reducer(key, list_of_values):
    ##print 'reducer:', key

    # separate A and B elements in the list of values
    elemsA = []
    elemsB = []

    for value in list_of_values:
    	##print '\t', value
	if value[0] == 'a':
		elemsA.append((value[1], value[2], value[3]))
	else:
		elemsB.append((value[1], value[2], value[3]))
		
    ##print '\tfrom matrix A: ', elemsA
    ##print '\tfrom matrix B: ', elemsB

    # accumulating sum of individual products

    sum = 0
    for valueA in elemsA:
    	for valueB in elemsB:
		if (valueA[1] == valueB[0]):
			#print valueA, valueB
			sum += valueA[2] * valueB[2]

    mr.emit((key[0], key[1], sum))
			

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
