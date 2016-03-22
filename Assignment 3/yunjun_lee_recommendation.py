"""
USC INF553 Sp. 2016
Assignment 3
Problem 2: Making Recommendations

Detail: https://goo.gl/FVfN7k
Debug: remove # at line 81
"""
import sys
import json

def recommend(inputdata_record, inputdata_lsh):
    """
    inputdata_record: Distinct User Records, e.g. ["Rachel", [1, 2, 3, 4]] ["Monica", [2, 3, 4, 5]]
    inputdata_lsh: candidates from LSH, e.g. ["U4", "U8"] ["U35", "U8"]

    Steps:
    1. For each distinct user, find all similar users based on LSH output, by findalikeuser()
    2. If number of similar users >= 5, compare the Jaccard similarity in record, by findtopfive()
    3. Make recommendations for each user based on their similar counterparts, by endorsement()
    """

    def findalikeuser(input2):
        """
        output: a dictionary, where key = user, values = list of similar users
        """
        sim_usrs = {}           # Dictionary: key = each user, values = user similar to key.
        pairs = []
        for line in input2:      # Read each line in inputdata
            pairs.append([json.loads(line)[0].encode("utf-8"), json.loads(line)[1].encode("utf-8")])
            pairs.append([json.loads(line)[1].encode("utf-8"), json.loads(line)[0].encode("utf-8")])
        for pair in pairs:
            if pair[0] not in sim_usrs:
                sim_usrs[pair[0]] = [pair[1]]
            else:
                sim_usrs[pair[0]].append(pair[1])
        return sim_usrs

    def findtopfive(rec, sim_usrs):
        """
        input: rec = user experience (record), sim_usrs = output from findalikeuser()
        output: a dictionary, where key = user, values = list of top-5 (or more) similar users
        """
        for user, alike_users in sim_usrs.iteritems():
            if len(alike_users) > 5:
                similarities = []
                for cand in alike_users:   # Calculate Jaccard Similarities (common/all)
                    common_element = float(len(list(set(rec[user]) & set(rec[cand]))))
                    all_element = float(len(list(set(rec[user]) | set(rec[cand]))))
                    similarities.append([common_element/all_element, cand])
                similarities.sort(reverse=True)
                last = 4                   # Index of last element in top-five (or more)
                while similarities[last][0] == similarities[last+1][0]:
                    last += 1
                for i in xrange(last+1, len(alike_users)):  # Remove un-desired elements
                    alike_users.remove(similarities[i][1])
        return sim_usrs

    def endorsement(rec, sim_usrs):
        """
        input: rec = user experience (record), sim_usrs = output from findalikeuser()
        output: a list containing users and recommended movies.
        """
        recommendations = []            # Recommendation Movie List for all user
        for user in sim_usrs.keys():            # For each user, 
            rec_movies = {}       # build a new dictionary, Key = unseen movie, Values = view count
            for sim_usr in sim_usrs[user]:      # check each of his/her similar user
                for movie in rec[sim_usr]:      # check each movie that similar user has seen
                    if movie not in rec[user]:  # an unseen movie
                        if movie not in rec_movies:   # Count it
                            rec_movies[movie] = 1       # First appear
                        else:
                            rec_movies[movie] += 1      # Count++
            # Now determine which movie should be recommended
            rec_list = []               # Recommendation Movie List for single user
            for movie in rec_movies:
                if rec_movies[movie] >= 3:      # Criteria is given by assignment:
                    rec_list.append(movie)      # movie must be watched by at least 3 users
            if len(rec_list) > 0:
                recommendations.append([user, rec_list])
        #print sorted(recommendations)
        return sorted(recommendations)

# Below this line are the main part.
    user_exp = {}                           # All user experience
    for line in inputdata_record:           # Read each line in inputdata_record
        user_exp[(json.loads(line)[0].encode("utf-8"))] = json.loads(line)[1]

    similar_users = findalikeuser(inputdata_lsh)            # Step 1
    top_five_list = findtopfive(user_exp, similar_users)    # Step 2
    recommendations = endorsement(user_exp, top_five_list)  # Step 3

    return recommendations
# Do not modify below this line
# =============================
if __name__ == '__main__':
    recommend(open(sys.argv[1]), open(sys.argv[2]))
