"""
USC INF553 Sp. 2016
Assignment 4
Problem 1: K-means algorithm

Input:
The first input argument is a .json file. Each line represents an n-dimensional data point.
The second input argument is an integer, the desired number of clusters.

Output:
The output contains k+1 lines, as stdout.
The first output "clusters" is the result of k-means clustering.
The second output "cohesion" is a float number representing the cohesion of the clustering.
It is measured by the average diameter of clusters in the clustering.
"""
import sys
import json
import math
from itertools import combinations

def kmeans(data_points, k_clusters, find_k_stars=False):
    """
    Input:
    1. data_points: a list of points (as tuples),
                    e.g., [(2, 2), (3.5, 2.5), (3.5, 4), (0, 7)]
    2. k_clusters: an integer, desired number of clusters
    3. find_k_stars: if True => Don't print out anything, but still return the final result

    Steps:
    1. Initialize
        For the initial centroids, pick points that are as far as possible:
        First, select the first point in the dataset as the first centroid.
        Next, pick the point with maximum "minimum Euclidean distance" to existing centroids.
        Repeat until k points has been chosen.
    2. Cluster
        Given centroids, cluster each datapoint into a group.
        After cluster is done, output the cluster as stdout, and update the centroids.
        Repeat until the result remain the same. (the centroids remain unchanged)
    3. Output/return the final result

    Output/return:
    1. clusters: a list consisted of lists of points (as tuples),
                 e.g. [[(4.6, 3.1), (4.7, 0.2)], [(4.9, 2.5), (5.5, 2.3)], [(6.3, 3.3)]]
    2. cohesion: a float, average of "max distance between any two points in each cluster"
    """

    def getDist(one, another):
        """
        return the Euclidean distance between two data points (two coordination)
        """
        assert len(one) == len(another)
        dim = len(one)
        sum = 0
        for i in xrange(dim):
            sum += (one[i] - another[i])**2
        return math.sqrt(sum)

    def getMinDistance(one, datapoints):
        """
        Given one single data point and a group of datapoints (list of existing centroids),
        return one's minimum Euclidean distance to the group.

        (Only for step 1. initialization, choose the one with the maximum value as next centroid.)
        """
        assert len(one) == len(datapoints[0])
        chosen_point = 0
        min_dist = getDist(one, datapoints[0])
        for p in datapoints:
            if getDist(one, p) < min_dist:
                chosen_point = p
                min_dist = getDist(one, p)
        return min_dist

    def initCentroids(datapoints, k_clusters):
        """
        (Step 1.)
        Pick and return k initial centroids.
        The first initial centroid is the first one in all the datapoints,
        The next initial centroid is the one has the maximum "min-distance" to all other centroids.
        Repeat until k initial centroids are chosen.
        """
        Centroids = []
        Centroids.append(datapoints[0])         # Add the first centroid (the first one)
        num_of_centroids = 1                    # The number of existing centroids
        while num_of_centroids < k_clusters:    # Keep seeking new one until number of centroids = k
            max_min_distance = 0
            seed = 0                            # index in original datapoints
            for p in datapoints:                # For each remaining datapoint
                if getMinDistance(p, Centroids) > max_min_distance: # If far from current centroids
                    max_min_distance = getMinDistance(p, Centroids) # Update it
                    seed = datapoints.index(p)
            Centroids.append(datapoints[seed])  # Add the next centroid
            #print "latest centroid:", Centroids[-1]
            num_of_centroids += 1               # Update the number of existing centroids
        #print "Centroids: ", Centroids
        return sorted(Centroids)

    def calcCentroids(data_points_in_a_cluster):
        """
        Update the centroids after the clustering is done.
        Given data points in a cluster (a list), return the centroid of these data points.

        (Only used in step 2. cluster)
        """
        new_centroid_pos = [0]*len(data_points_in_a_cluster[0])     # Calculate as list
        for dp in data_points_in_a_cluster:
            for dim in xrange(len(dp)):
                assert len(dp) == len(new_centroid_pos)
                new_centroid_pos[dim] += dp[dim]                    # Simply sum each dimension...
        for dim in xrange(len(new_centroid_pos)):                   # ... then divide them into avg
            new_centroid_pos[dim] = float(new_centroid_pos[dim])/len(data_points_in_a_cluster)
        return tuple(new_centroid_pos)                              # Output as tuple

    def getCohesion(cluster_dict):
        """
        input: a dictionary, key = cluster (group) id, values = data points in the same cluster
        cohesion: average of cluster diameter - max distance between any two points in each cluster
        return cohesion

        (Only used in step 3.)
        """
        cohesion = []                       # Use a list to store diameter of each cluster
        for cluster_dps in sorted(cluster_dict.values()):
            max_d = 0                       # max distance
            if len(cluster_dps) > 1:        # Update max_d when the cluster has more than one point
                for pair in list(combinations(sorted(cluster_dps), 2)):
                    if getDist(pair[0], pair[1]) > max_d: max_d = getDist(pair[0], pair[1])
            cohesion.append(max_d)
        return float(sum(cohesion))/len(cohesion)       # Return the avg diameter

    def cluster(datapoints, centroids, final_result=False):
        """
        arguments
        final_result: if True => return the final result

        (Step 2.)
        Given datapoints and centroids, assign each datapoint into a cluster.
        Next, update the centroids and return nothing

        (Step 3.)
        If criteria is met (centroids remain unchanged), stdout/return:
        1. k clusters, each as one line.
        2. the cohesion.
        """

        cluster_dict = {k: [] for k in range(len(centroids))}  # key: cluster #, value: data points
        for p in datapoints:                  # Find out which cluster a single datapoint belong to
            min_dist = getDist(p, centroids[0])
            seed = 0
            for c in centroids:
                if getDist(p, c) < min_dist:
                    min_dist = getDist(p, c)
                    seed = centroids.index(c)
            cluster_dict[seed].append(p)            # Assign data point into different groups

        for i in xrange(len(cluster_dict)):
            centroids[i] = calcCentroids(cluster_dict[i])   # Update the centroids

        #for v in sorted(cluster_dict.values()): print v

        if final_result:              # If the criteria is met...
            clusters = []
            for v in sorted(cluster_dict.values()):
                clusters.append(sorted(v))
            cohesion = getCohesion(cluster_dict)
            return clusters, cohesion                       # ...return clusters and cohesion

        #print "Cents:", sorted(centroids)  # DEBUG
        centroids = sorted(centroids)
        return 0

    ############################################################################################
    # Below this line are the main part of kmeans().

    if k_clusters >= len(data_points): k_clusters = len(data_points)
    centroids = initCentroids(data_points, k_clusters)                      # Step 1.
    keep_clustering = True
    while keep_clustering:
        old_centroids = []                  # old centroids
        for i in centroids: old_centroids.append(i)
        #print "Cents:", sorted(old_centroids)  # DEBUG
        cluster(data_points, centroids)                                     # Step 2.
        #print "New Cents:", sorted(centroids)  # DEBUG
        if old_centroids == centroids:      # if centroids remain the same => Step 3.
            cluster, cohesion = cluster(data_points, centroids, True)
            keep_clustering = False
            return sorted(cluster), cohesion        # Return as assigned

# Do not modify below this line
# =============================
if __name__ == '__main__':
    f = open(sys.argv[1])   # json file that containing data points
    k = int(sys.argv[2])
    dp = []                 # data points
    for l in f:             # Read them all
        dp.append(tuple(json.loads(l)))
    clus, coh = kmeans(dp, k)
    
    for c in clus: print sorted(c)  # Print clusters out
    print coh               # Print cohesion out

