Working example - Create signatures for Shakespeare dataset

# Create the sparse matrix (results saved in table : NN_base) 
```
with Q1 as ( SELECT word, weight global_weight, word_counter global_counter  FROM `ds.DVR`     ) , 
     Q2 as ( SELECT user_id                                   FROM `ds.VECTORS`  group by 1    ) , 
     Q3 as ( SELECT word  , local_weight, user_id, word_counter             FROM `ds.VECTORS`  )  
     select * from ( select * from Q1 cross join Q2  ) 
     left join 
     Q3   using (word,user_id) 
```     
# Create signatures  (results saved in table :kl_results)    
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
      1/30000 epsilon,   ### -- Should match the corpus size
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
          [ds.NN_base]  )
      ))   ))
```
# Cut the signatures in 500 most contributing words (results saved in table : kl_signatures) 
```
select * from ( SELECT * , row_number() over (partition by user_id order by KL desc) kl_rnk  FROM [ds.kl_results] )
where kl_rnk <=500 
```
# Results (Example of Shakespere books) 
https://github.com/hagitbenshoshan/text_distance/blob/master/KLD%20signatures.png
