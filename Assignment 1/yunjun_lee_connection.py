"""
USC INF553 Sp. 2016
Assignment 1
Problem 1: Social Network
Details: https://goo.gl/ix2NwN
"""

import sys
import MapReduce

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    """
    Each record has two persons, output this relationship twice
    key: first person
    value: second person
    """
    key = record[0]
    value = record[1]
    mr.emit_intermediate(key, value)
    mr.emit_intermediate(value, key)

def reducer(key, list_of_values):
    """
    Sort the neighbors alphabetically, then output the combination of neighbors.
    key: person of interest
    value: list of his/her neighbors
    """
    list_of_values.sort()
    if len(list_of_values) >= 2:
        for poi in range(0, len(list_of_values)):
            for neighbor in range((poi+1), len(list_of_values)):
                # Should no use print here
                # str() is not necessary for output format
                mr.emit([list_of_values[poi], list_of_values[neighbor], key])
# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
