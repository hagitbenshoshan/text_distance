# text_distance Datasets and algorithm for short text

## Technologies used :  Google BigQuery , Python
                     
### Thesis - Datasetes and algorithm to compute distances between ranked non-conjoint lists 
* Input : Short text files documents , each document belongs to one author. 
* The algorithm requires pre-processing text manipulation (tokenize,stemming,POS tagging,remove stop words) performed by https://github.com/hagitbenshoshan/text_distance/blob/master/tokenize_stem_pos.py
```
Example : The input file name is review_26536435.txt , blongs to user_id = 26536435 
generates the following output: 
```
document_id | original word | POS | stemmed word 
------------|---------------|-----|---------------    
review_26536435.txt|matrix|NN|matrix
review_26536435.txt|like|IN|like
review_26536435.txt|time|NN|time
review_26536435.txt|science|NN|scienc
review_26536435.txt|fiction|NN|fiction
review_26536435.txt|movies|NN|movi
review_26536435.txt|makes|VB|make
review_26536435.txt|classic|JJ|classic
review_26536435.txt|matrix|NN|matrix
```

- We only include results of "Noun" (NN/NNS)  words
- Raw data is uploaded to Google BigQuery table in the fillowing structure 

```
user_id | word | Frequency
--------|------|----------
26536435|matrix|2
26536435|time|1
26536435|scienc|1
26536435|fiction|1
26531122|time|12
```

- Creating a domain in Google BigQuery (result table name #DVR) : 

select   word,word_counter,word_counter/tot as global_weight,rnk from 
(SELECT 
 * , row_number() over (order by word_counter desc ) as rnk , sum(word_counter) over () as tot from 
( select word , sum(counter) 	word_counter	 from
( select word , sum(Frequency) counter
  FROM ( -- Replace the following lines with your raw data table name 
         select 'a' word,   3 Frequency  union all 
         select 'b' word,   9 Frequency  union all 
         select 'c' word,   6 Frequency             
         ) 
  where pos like 'NN%' 
  group by 1  )  group by 1 )) 
  
  ``` 
  word|word_counter|global_weight|rnk
  ----|------------|-------------|----
b|9|0.5|1	 
c|6|0.3333333333333333|2	 
a|3|0.16666666666666666|3

```
- Creating user's vector in Google BigQuery (result table name #VECTORS) : 

select *, word_counter/total_weight 	local_weight , rank() over (partition by user_id order by word_counter desc) rnk 	from 
(select *,    sum(word_counter) over (partition by user_id )  as total_weight  from 
( select    word ,    user_id ,   sum(Frequency)  word_counter  
from  ( -- Replace the following lines with your raw data table name 
select 'a' word , 1 user_id , 3 Frequency union all 
select 'a' word , 1 user_id , 3 Frequency union all 
select 'a' word , 2 user_id , 4 Frequency union all 
select 'b' word , 1 user_id , 5 Frequency union all 
select 'c' word , 1 user_id , 1 Frequency union all 
select 'b' word , 2 user_id , 7 Frequency  
      ) 
 group by 1 ,2
   )  ) order by   2
 ```
word|	user_id|	word_counter|	total_weight|	local_weight|	rnk	
----|--------|--------------|-------------|-------------|-----
a|	1|	6|	12|	0.5|	1	 
b|	1|	5|	12|	0.4166666666666667|	2	 
c|	1|	1|	12|	0.08333333333333333|	3	 
b|	2|	7|	11|	0.6363636363636364|	1	 
a|	2|	4|	11|	0.36363636363636365|	2
  ``` 
 
  

 
