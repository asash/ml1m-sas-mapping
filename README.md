# ml1m-sas-mapping
Mapping from SASRec's version of Ml1m to the original repository

MovieLens 1-m is a popular benchmark dataset for comparing recommender systems. 

A version of it was published in the SASRec repository (https://github.com/kang205/SASRec/blob/master/data/ml-1m.txt) and became the de-facto standard 
for comparing sequential recommender systems (it is used, for example, in SASRec itself and BERT4Rec, two of the most popular transformer-based recommender systems). 

Unfortunately, the version from SASRec remapped the original user and item ids into a new range, so it is hard to use SASRec's version if we need to use other information from the original ML-1m dataset, such as title and genres. 

This repository recovers the mapping. We do that via fingerprinting of counts, and luckily. The result is one-to-one mapping. 

Recovered user ids are in the "sas_to_original_users.txt" file, and recovered items are in the "sas_to_original_items.txt" file. "decoded.csv" contains all interactions encoded by the original and SASRecs's versions of ids. 
