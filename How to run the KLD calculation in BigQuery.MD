# NN_base contains only Nouns words.
creating NN_base (sparse matrix) as following 
```
with Q1 as ( SELECT word, global_weight,rnk global_rank    FROM `DVR`  order by rnk /*limit 100*/ ) , 
     Q2 as ( SELECT user_id                                FROM `VECTORS`  group by 1  /*limit 34*/ ) , 
     Q3 as ( SELECT word  , local_weight, user_id, counter , lrnk local_rank   FROM `VECTORS`   )  
     select * from ( select * from Q1 cross join Q2  ) 
     left join 
     Q3   using (word,user_id) 
     order by  user_id , counter  desc  
```


```
Each document contains an entry for all the words in the corpus. When the word is missing we assign 0 to it's local weight. 
```
word     |global_rank  |global_weight  |user_id   |local_weight| counter |local_rank  
---------|-------------|---------------|----------|------------|---------|---------- 
heartili |11155        |5.705e-06      |103511    |0.000297    | 5 |473         
heartili |11155        |5.705e-06      |2251264   |null        | null|null
person	| 81|0.0013477678061898945|	3051084|0.00055897149245388487	|2	|335	 
script	|92|0.00125906992857646|	3051084|null	|null	|null	
 
# Update the base table NN_base to store global and local weights ###
Save the results in <dataset.NN_base> table 
```
select * ,'NN' pos,  counter_in_corpus/words_in_corpus as global_weight ,counter_in_book/words_in_book as in_book_weight  ,counter_in_chapter/words_in_chapter as local_weight    from 
( select *  from 
( SELECT word ,book_name , chapter_id , 
count(*) over (partition by word) as counter_in_corpus , 
count(*) over (partition by book_name,word ) as counter_in_book ,   -- If exist
count(*) over (partition by book_name,chapter_id,word ) as counter_in_chapter, 
count(*) over () as words_in_corpus , 
count(*) over (partition by book_name) as words_in_book , 
count(*) over (partition by book_name,chapter_id) as words_in_chapter 
FROM `dataset.NN_base` )  -- replace by your  <dataset_name>.<table_name>     
/* Add it only in short texts scenario:  where counter_in_corpus > 5  and words_in_chapter > 150   */ 
group by 1,2,3,4,5,6,7,8,9 )
```
# Run KL distance calculation
Save the results in <dataset.signatures>  table 
```
select * , row_number() over (partition by user_id order by KL desc ) rnk from 
( SELECT
   if (existing_word_flag=1,
       ((local_weight -global_weight) *LOG10(local_weight /global_weight )),
      (epsilon -global_weight) *LOG10(epsilon /global_weight ))  KL,
  
    if (existing_word_flag=1,
      gamma*((local_weight -global_weight) *LOG10(local_weight /global_weight )),
      (epsilon -global_weight) *LOG10(epsilon /global_weight )) gama_KL,
          if (existing_word_flag=1,
      beta*((local_weight -global_weight) *LOG10(local_weight /global_weight )),
      (epsilon -global_weight) *LOG10(epsilon /global_weight )) beta_KL,
    *
  FROM (  
  select *  , 1-(missing_words*epsilon ) beta from (
    SELECT
      1/100000 epsilon,   -- Should match the corpus size
      1-(missing_words/words) gamma,
      
      *
    FROM (
      SELECT  
        SUM( word_counter) OVER (PARTITION BY user_id) words_in_user,
        COUNT(distinct word) OVER (PARTITION BY user_id ) distinct_words, 
        COUNT(*) OVER (PARTITION BY user_id ) words,
        SUM(existing_word_flag) OVER (PARTITION BY user_id ) existing_words,
        SUM(missing_word_flag) OVER (PARTITION BY user_id ) missing_words,
        *
      FROM (
        SELECT
          user_id ,word,
          global_weight,
          ifnull(local_weight, 1/100000) local_weight ,
          ifnull(word_counter,0) word_counter ,global_counter ,
          if ( word_counter is not null ,
            0,
            1) AS missing_word_flag,
          if ( word_counter is null ,
            0,
            1) AS existing_word_flag
        FROM
          [dataset.table]  )
      )) 
         )) 
```
#  SELECT *  FROM `dataset.signatures`  where rnk <= 500  order by user_id , rnk   
```
This is how we define the size of the signature (replace the 500 by any value) 
