"""
USC INF553 Sp. 2016
Assignment 2
Problem 2: SON algorithm (phase 2)

The goal of 2nd phase is to output global frequent itemsets. (not just candidates)

0. No global variables: to simulate MapReduce Architecture

1. How to execute:
    python firstname_lastname_son-phase2.py chunks.json phase1output.json

2. Here are two ways to generate 'phase1output.json':
    (1) Just use the sample file 'phase1output.json' we provided;
    (2) Redirect your output to your own 'phase1output.json' with the following command,
       and then use it for phase 2:
       python firstname_lastname_son-phase1.py chunks.json > phase1output.json

3. Mapper: Count the occurance of these candidates.
    Output from mapper the basket count in every key-value pair,
    (candidate, (candidate count, basket count)) or any equivalent format.

4. Reducer: Judge whether its a frequent item or not.

Details: https://goo.gl/SKHNn4
"""

import sys
import json
import MapReduce

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
    phase_one_output = open(sys.argv[2]).read().splitlines()
    # the file is a list seperated with => phase_one_output is a list of str.

    for line in phase_one_output:
        record = json.loads(line)                     # Read these str as list

        cand_count = 0
        for eachbasket in chunk:
            if set(record).issubset(set(eachbasket)):
                cand_count = cand_count + 1
        
        mr.emit_intermediate(tuple(record), cand_count)

def reducer(key, list_of_values):
    """
    Based on what has been reported from mapper, judge whether it's a valid candidate or not
    """
    chunks_of_baskets = open(sys.argv[1]).read().splitlines()
    # the file is a list seperated with \n =>  chunks_of_baskets is a list of str.

    basket_count = 0
    for chk in chunks_of_baskets:
       lst = json.loads(chk)                          # Read these str as list
       basket_count += len(lst)

    count_sum = 0
    for value in list_of_values:
        count_sum = count_sum + value
    if count_sum >= 0.3 * basket_count:               # Support = 30%
        mr.emit([list(key), count_sum])

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
