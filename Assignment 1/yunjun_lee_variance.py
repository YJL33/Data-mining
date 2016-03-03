"""
USC INF553 Sp. 2016
Assignment 1
Problem 2: Variance Calculation
Details: https://goo.gl/ix2NwN
"""

import sys
import MapReduce

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    """
    Each record has multiple integers, assign them as the same key
    key: 1 => E(X),  2 => E(X^2)
    value: (sum of integer, count) or (sum of integer^2, count)
    """
    sum_of_int = 0
    sum_of_sq = 0
    count = 0
    for integer in record:
        sum_of_int = sum_of_int + integer
        sum_of_sq = sum_of_sq + integer**2
        count = count + 1
    mr.emit_intermediate(1, (sum_of_int, sum_of_sq, count))

def reducer(key, list_of_values):
    """
    VAR(X) = E(X^2) - E(X)^2
    E(X^2) = average of all v[1]
    E(X) = average of all v[0]
    """
    sum_f = 0
    sum_s = 0
    count = 0
    for (integer, square, partial_count) in list_of_values:
        sum_f = sum_f + integer
        sum_s = sum_s + square
        count = count + partial_count
    avg_f = sum_f/float(count)
    avg_s = sum_s/float(count)
    # Should not use print here
    # Should not round the result (even it's round to 12 digit)
    mr.emit(avg_s - avg_f**2)

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
