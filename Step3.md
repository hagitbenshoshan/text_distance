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

### 1. Create a table of all the possible pairs combinations (cross join)  , table name #cross_categories 
```
with Q1 as   (select user_id   user1  from  VECTORS group by 1  ) ,  
     Q2 as   (select user_id   user2  from  VECTORS group by 1  )
     select * from Q1 cross join Q2
``` 
|user1|user2|
|-----|-------|
|119161| 140921	 
|1596111| 45957298	 
|286445| 486368	 
|430992| 14612223	 
 
 ### 2. Create flagged (positive/negative) KLD signatures table , table_name KLDS
```
SELECT  user_id , sign , word    case
when sign =1  then KL_SYM +1  
else KL_SYM-1   end as KLR 
FROM `SIGNATURES`
```
|Row|	user_id|	sign|	word|	KLR 	 
|---|--------|-----|-----|----
1|925405	|1|	vote|	1.0262807390446969	 
2|	925405|	1|	movi|	1.011751048183591	 
3|	925405|	1|	definet|	1.0114686347968689	 
4|	925405|	1|	gag|	1.0034762996406752	 
5|	925405|	1|	watch|	1.003279590849277	 
6	|925405|	-1|	audienc|	-0.9968483975383385	 
 
 ### 3. calculate distance between pairs of users 
```
with Q1 as (select user_id , word , KLR KLR1 FROM KLDS), 
     Q2 as (select user1  , user2   from  cross_categories)  

select sum(csize) csize , sum(diff) / sum(csize) distance_between_users , user1,user2 from 
(select sum(csize) csize , sum(abs(u1-u2))  diff ,word , user1, user2 from 
(select   word,max(u1) u1 , max(u2) u2 , user1,user2, 1 as csize     from  
( select word, if  (user_id = user1,KLR1,0) u1, 
               if  (user_id = user2,KLR1,0) u2, user1,user2  from Q1    
               cross join Q2  
               where user_id = user1 or user_id=user2 ) Q11  
               group by word,user1, user2 ) 
               group by word , user1, user2) 
group by     user1, user2 
```

Row|	csize	|distance_between_users|	user1	|user2|
---|-------|----------------------|-------|-----|
1	|869|	0.899003311889057	|3487897	|19835265	 
2	|854|	0.8635888345541498	|1622306	|2512513	 
3	|864|	0.877976033795813	|1562896	|3036648	 
