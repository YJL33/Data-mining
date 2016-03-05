"""
USC INF553 Sp. 2016
Assignment 2
Problem 1: Apriori algorithm

Details: https://goo.gl/SKHNn4
"""
import sys
import json

def apriori(baskets, prrst):
    """
    baskets: a list of integer list, containing all the baskets read from file,
             e.g.: [[1, 2], [1, 2, 3], [1, 3, 4], [2, 3, 4], [3, 4]]
    prrst: boolean value, True = print out result of each pass
    output: a nested list containing all the frequent itemsets found by the algorithm,
            as [[sorted list of frequent 1-itemsets],..., [sorted list of frequent k- itemsets]],
            e.g.: [[[1], [2], [3], [4], [6]], [[1, 2], [1, 3], [2, 3]]]

    Steps:  (1) Get "local candidate of freq. 1 items" and "local frequent 1 items" (C1 & L1)
            (2) Get "local candidate of freq. k items" and "local frequent k itemsets" (Ck & Lk)
            (3) Output all local frequent item/itemsets.
    """
    # Step 0: Setup variables
    sup_threshold = 0.3 * len(baskets)                          # Set to 30% as assigned
    all_items = []                                              # All items
    distinct_items = []                                         # candidates of freq 1 itemset
    frequent_items = []                                         # freq itemset
    frequent_number = 1                                         # k for checking frequent-k itemset
    output = []                                                 # Output all candidates as list

    # Step 1: Get C1 and L1
    for eachbasket in baskets:
        for item in eachbasket:
            all_items.append(item)                                  # Get all items w/ repetitive
    distinct_items = list(set(all_items))                           # Get C1
    frequent_items = [x for x in distinct_items if all_items.count(x) >= sup_threshold]   # Get L1
    for x in frequent_items:
        output.append([x])
    check_pass_result(prrst, frequent_number,
                      [[x] for x in distinct_items], [[x] for x in frequent_items])

    # Step 2: Iteratively get Ck and Lk
    while len(frequent_items) >= 1:
        frequent_number += 1
        distinct_items = get_candidate(frequent_items, frequent_number)           # Get Ck
        frequent_items = check_frequency(distinct_items, baskets, sup_threshold)  # Get Lk
        for x in frequent_items:
            output.append(x)
        check_pass_result(prrst, frequent_number, distinct_items, frequent_items)

    # Step 3: Output all local frequent itemsets
    return output

def get_candidate(frequent_items, k):
    """
    Return candidates (each as list) of frequent k itemset from frequent (k-1) itemset
    Steps for k > 2:
       1. Get all supersets from k-1 itemsets
       2. Remove supersets that have incorrect length
       3. Remove duplicates
       4. Check whether it's a valid candidate (apriori property)
       5. Check whether these candidates is a valid frequent item.
    """
    if k is not 2:
        freq_k_cand = [list(set(frequent_items[i]) | set(frequent_items[j]))
                       for i in range(0, len(frequent_items))
                       for j in range(i+1, len(frequent_items))]               # Step 1
        freq_k_cand = [x for x in freq_k_cand if len(x) == k]                  # Step 2
        freq_k_cand = [list(i) for i in set(map(tuple, freq_k_cand))]          # Step 3
        counter = len(freq_k_cand) * [0]                                       # Step 4
        # Count the number of subset: Each valid freq-k itemset should have k immdeiate subsets
        for freq in frequent_items:
            for cand in freq_k_cand:
                if set(freq).issubset(cand):
                    counter[freq_k_cand.index(cand)] += 1
        return [x for x in freq_k_cand if counter[freq_k_cand.index(x)] >= k]  # Step 5
    else:   # set() doesn't work for k = 2
        freq_2_cand = [[frequent_items[i], frequent_items[j]]
                       for i in range(0, len(frequent_items))
                       for j in range(i+1, len(frequent_items))]
        return freq_2_cand

def check_frequency(candidates, baskets, sup_threshold):
    """ Return valid candidate by checking whether it is frequent itemset (back to basket) """
    freq = []            # freq itemset
    for cand in candidates:
        count = 0
        for eachbasket in baskets:
            if set(cand).issubset(eachbasket):
                count = count + 1
        if count >= sup_threshold:
            freq.append(cand)
    return freq

def check_pass_result(prrst_checker, k, cand_pass, freq_pass):
    """ If prrst is True, print out the local freq. k candidates and local frequent k itemsets """
    if prrst_checker is True:
        print "C" + str(k) + ": " + str(cand_pass)
        if len(cand_pass) is not 0:
            print "L" + str(k) + ": " + str(freq_pass)

# Do not modify below this line
# =============================
if __name__ == '__main__':
    apriori(json.load(open(sys.argv[1])), bool(sys.argv[2]))
