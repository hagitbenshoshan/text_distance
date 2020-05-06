# How to calculate similarity/distance between 2 signatures
Given a pair of signatures, how can we decide whether they were written by the same author or not?
Our method is to examine the source of the distance. Signatures of two authors can differ both in which words they contain and in why they contain these words - whether because they are used unusually frequently or unusually infrequently.

We distinguish between three distance-generating categories when comparing a pair of signatures.

1)    No overlap: These are words which appear in one of the signatures but not the other.

2)    Overlap same direction (Same trend) : These are words which appear in both signatures for the same reason - Either both authors use them or both don’t.

3)    Opposite trends: These are words which appear in both signatures but for opposite reasons - one author uses them while the other doesn’t.

 

In order to create cardinal differentiation between the trends ,we added +1 to the KLD of words with positive origin (words that exist in the author’s text) , and add -1 to the KLD of words with negative origin (words that were not exist in the author’s text).

For null KL we assigned 0. 

The distance between the signatures is auclidian distance between the 2 KLD+/-1 of the same word.

Normalize: 

We calculated the sum of all distances we found , and divided it by the number of words in the common corpus . (Minimum=500 , Maximum=1000) . 
