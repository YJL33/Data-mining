Problem		TestCase	Output					Note
APriori		baskets_1.json	output_1_1.txt				has C4 but no L4
APriori		baskets_2.json	output_1_2.txt				has C2 but no L2
APriori		baskets_3.json	output_1_3.txt				no frequent
APriori		baskets_4.json	output_1_4.txt				no C3, also OK if output C3 (and L3) as []
APriori		baskets_5.json	output_1_5.txt				bigger file, has C3 no L3
SON		chunks_1.json	output_2_1_1.json, output_2_1_2.json
SON		chunks_2.json	output_2_2_1.json, output_2_2_2.json	
SON		chunks_3.json	output_2_3_1.json, output_2_3_2.json	1-3 same data as baskets_5, distributed into different chunks, final result should be the same
SON		chunks_4.json	output_2_4_1.json, output_2_4_2.json	has local frequent but no global frequent
SON		chunks_5.json	output_2_5_1.json, output_2_5_2.json	same data as 4 but only 1 chunk, no local nor global frequent