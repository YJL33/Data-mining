"""
USC INF553 Sp. 2016
Assignment 2
Problem 2: SON algorithm (phase 1)

The goal of 1st phase is to output the candidates of global frequent itemsets.

1. Mapper examines each chunk, and provide local frequent itemset.
2. Reducer outputs the candidates of global frequent itemset according to:
    (1) If itemset 'A' is in-frequent in all chunk => A is definitely NOT a frequent itemset.
    (2) If itemset 'B' is frequent in all chunk => B is definitely a frequent itemset.
    (3) If itemset 'C' is partially frequent in all chunk => whether C is frequent is unknown.
3. Among above situations, only B and C will output from phase1.
4. Only output the result to std out. Here are two ways to generate 'phase1output.json':
    (1) Just use the sample file 'phase1output.json' we provided;
    (2) Redirect your output to your own 'phase1output.json' with the following command,
       and then use it for phase 2:
       python firstname_lastname_son-phase1.py chunks.json > phase1output.json

Details: https://goo.gl/SKHNn4
"""

import sys
import MapReduce
import yunjun_lee_apriori as Apriori

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(chunk):
    """
    Each chunk has multiple baskets.
    Output format:
    key: candidate
    value: candidate count
    """
    candidates_list = Apriori.apriori(chunk, False)
    for each_candidate in candidates_list:
        mr.emit_intermediate(tuple(each_candidate), 1)

def reducer(key, list_of_values):
    """
    Based on what has been reported from mapper, judge whether it's a valid candidate or not
    """
    if len(list_of_values) is not 0:
        mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
