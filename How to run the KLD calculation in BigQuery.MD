
# create the base table NN_base to store global and local weights ###
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
FROM `books2.NN_base` )  -- replace by your  <dataset_name>.<table_name>     
/* Add it only in short texts scenario:  where counter_in_corpus > 5  and words_in_chapter > 150   */ 
group by 1,2,3,4,5,6,7,8,9 )
```
# Run KL distance calculation
```
SELECT
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
         ) 

