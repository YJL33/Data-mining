"""
USC INF553 Sp. 2016
Assignment 4
Problem 2: Find k-star

<Input>
The first input is a .json file the same as described in part 1.
The second input is a float in (0, 1), representing theta mentioned in Step 1.

<Output>
The output is a single integer representing k*.

<Execute>
python firstname_lastname_findkstar.py input.json theta
Use sample input file to test your code, set theta to 0.2, and the expected output should be 4.
"""
import sys
import json
import math
import yunjun_lee_kmeans as km

def findkstar(data_points, theta):
    """
    Input:
    1. data_points: a list of points (as tuples),
                    e.g., [(2, 2), (3.5, 2.5), (3.5, 4), (0, 7)]
    2. theta: a threshold between (0, 1)

    Steps of elbow method:
    1. Perform m clusterings to decides the range k* falls into.
    2. Perform a binary search for k* among the range [v/2, v].

    Output:
    The output is a single integer representing k*, optimum number of clusters.
    """

    def mClustering(dps, t):
        """
        Perform m clustering.
        dps: data points, t: theta

        return the left boundary of desired range
        """
        num_of_data_points = len(dps)                           # Number of data points
        keep_clustering = True
        k = 0               # used to generate the list of power of 2, e.g. k=0, 2**k=1...etc
        while keep_clustering:
            k += 1
            if 2**(k) > num_of_data_points:
                print "Special case (2v > N), k* = n:", num_of_data_points
                quit()
            cluster_v, cohesion_v = km.kmeans(dps, 2**(k-1))
            cluster_2v, cohesion_2v = km.kmeans(dps, 2**k)
            rate_of_chg = abs(cohesion_v - cohesion_2v) / (cohesion_v*abs(2**k))
            #print rate_of_chg
            if rate_of_chg < t: keep_clustering = False
        #print "Pick interval:", 2**(k-1), 2**k
        return 2**(k-1)

    def binarySearch(left, dps, t):
        """
        Perform binary search among the range [x,y], where y>x, z is the midpoint
        left: left boundary of desired range, dps: data points, t: theta

        return k-star
        """
        right = 2*left
        kstar = 0
        keep_search = True
        while keep_search:
            midpoint = (right+left)/2                   # midpoint for binary search
            cluster_m, cohesion_m = km.kmeans(dps, midpoint)
            cluster_r, cohesion_r = km.kmeans(dps, right)
            rate_of_chg = abs(cohesion_r - cohesion_m) / (cohesion_r*abs(right-midpoint))
            #print rate_of_chg
            if rate_of_chg > t: left = midpoint         # [z,y] is qualified => stay at [z,y]
            if rate_of_chg < t: right = midpoint        # [z,y] is not qualified => switch to [x,z]
            if right-left == 1: keep_search = False     # Criteria is met, break loop...
        cluster_l, cohesion_l = km.kmeans(dps, left)    # ... now output x or y,
        cluster_r, cohesion_r = km.kmeans(dps, right)   # whichever gives better cohesion,
        if cohesion_l < cohesion_r: kstar = left        # in other word, smaller diameter.
        else: kstar = right
        return kstar                                    # print kstar

    ################################################################################################
    # Below this line are the main part.

    left_boundary = mClustering(data_points, theta)             # Step 1.
    kstar = binarySearch(left_boundary, data_points, theta)     # Step 2.
    print kstar

# Do not modify below this line
# =============================
if __name__ == '__main__':
    f = open(sys.argv[1])   # json file that containing data points
    theta = float(sys.argv[2])
    if theta > 1 or theta <= 0:
        print "theta out of range (0,1)"
        quit()
    dp = []                 # data points
    for l in f:             # Read them all as tuple
        dp.append(tuple(json.loads(l)))
    findkstar(dp, theta)
