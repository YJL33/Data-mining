"""
USC INF553 Sp. 2016
Assignment 3
Problem 1: Finding Similar Items

Suppose there are 100 different movies, numbered from 0 to 99.
A user is represented as a set of movies.
Jaccard coefficient is used to measure the similarity of sets.

Apply minhash to obtain a signature of 20 values for each user.
Recall that this is done by permuting the rows of characteristic matrix of movie-user matrix
(i.e., row are movies and columns represent users).

Assume that the i-th hash function for the signature:
h(x,i) = (3x + i) % 100 (i = 1...20), where x is the original row number in the matrix.

Apply LSH to speed up the process of finding similar users,
where the signature is divided into 5 bands, with 4 values in each band.
Name your script for this problem firstname_lastname_Lsh.py.
"""

import sys
import json

def lsh(inputdata):
    """
    inputdata: User Record
    e.g.
    ["Rachel", [1, 2, 3, 4]]
    ["Monica", [2, 3, 4, 5]]

    Steps:
    1. Construct the characteristic matrix as a dictionary.
       For each user, convert the movie ID set as a boolean list.
       [key = user, values = 100 booleans]
    2. Construct the signature matrix as a dictionary.
       Apply hash to obtain re-ordered movie list.
       [key = user, values = 20 integers]
    3. Apply LSH to speed up finding similar users
    """

    # Step 1. Construct the characteristic matrix
    #         As Textbook p.81, Fig 3.2, 3.3.1 Matrix Representation of Sets
    char_mat = {}
    for line in inputdata:          # Read each line in inputdata
        record = []
        record.append(json.loads(line)[0].encode("utf-8"))   # User name
        record.append(json.loads(line)[1])                   # Movie ID

        movie_list = []             # convert the Movie ID into 100 boolean values
        for i in xrange(100):
            if i in record[1]:
                movie_list.append(True)
            else:
                movie_list.append(False)
        char_mat[record[0]] = movie_list

    # Step 2: Construct the signature matrix
    #         Update the signature matrix iteratively by i(20) hash functions
    #         As Textbook p.83-85, 3.3.5 Computing Minhash Signatures
    sig_mat = {}                                    # initialize the dictionary for signatures
    for key in char_mat.keys():
        sig_mat[key] = [256 for x in xrange(20)]

    num_of_users = len(char_mat.values())
    for r in xrange(100):                           # r = original row number (0-99)
        for i in xrange(1, 21):                     # i = i-th hash function ((3x + i) % 100)
            new_r = (3*r+i)%100                     # new_r = new row number after hashing
            for u in xrange(num_of_users):          # u = Number of users
                if char_mat.values()[u][r] is True and new_r < sig_mat.values()[u][i-1]:
                        sig_mat.values()[u][i-1] = new_r

    # Below this line, char_mat should be no longer needed.

    # Step 3. Apply LSH to find similar users:
    # divide each sigature into 5 bands, with 4 values in each band
    for i in xrange(0, len(sig_mat.keys())):
        for j in xrange(i+1, len(sig_mat.keys())):
            sim_band = [1]*5
            for b in xrange(5):
                for r in xrange(4):
                    if sig_mat.values()[i][4*b+r] != sig_mat.values()[j][4*b+r]:
                        sim_band[b] = 0
                        break
            similarity = sum(sim_band)/5
            print sig_mat.keys()[i], sig_mat.keys()[j], similarity

# Do not modify below this line
# =============================
if __name__ == '__main__':
    lsh(open(sys.argv[1]))