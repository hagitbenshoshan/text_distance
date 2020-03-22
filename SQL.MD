### Extract one book and create a  table per book (KL_tresure) ###
SELECT *  FROM [books.NN_books]  where book_name = 'Treasure_Island_by_Robert_Louis_Stevenson-chapters' order by chapter_id , weight_in_chapter desc 	

### Create the DVR (KL_DVR) 
SELECT word,tot_book_length , global_counter , global_weight , count(distinct chapter_id ) in_chapters_counter  FROM [books.KL_tresure]  group by 1,2,3,4


### KL Distances of chapter from its book  ### 
select chapter_id , sum(KL_SYM) KL_distance from   
( SELECT
    *,  
    if(chapter_id is null ,  (1/1000) ,   (( global_weight- local_weight) * log10 (global_weight / local_weight ))   )  AS KL_SYM 
   FROM (
    SELECT
      chapter_id ,
      a.word word,
      counter,
      local_weight,     
      b.global_weight global_weight ,
        (1/10000)  epsilon  FROM 
(SELECT word,global_weight   from 
        [books.KL_DVR]) b
        left join        
        (SELECT chapter_id  , word, counter , local_weight             
      FROM
        [books.KL_tresure]   ) a 
     ON
      a.word=b.word )   )   
   GROUP BY
  1   

### Create another chapter table , from diffrent origin  (KL1) ### 
SELECT
  book_name,
  word,
  '99.txt' chapter_id,
  counter,
  weight_in_chapter,
  book_length,
  chapter_length,
  counter_in_book,
  weight_in_book,
  global_weight,
  tot_counter,
  tot
FROM
  [books.help4_NN_books]
WHERE
  book_name = 'A_Study_In_Scarlet-chapters'
  AND chapter_id ='01.txt'
ORDER BY
  chapter_id,
  weight_in_chapter DESC
  
### Cosaine similarity ### 
  /*
Cosine Similarity (d1, d2) =  Dot product(d1, d2) / ||d1|| * ||d2||

Dot product (d1,d2) = d1[0] * d2[0] + d1[1] * d2[1] * … * d1[n] * d2[n]
||d1|| = square root(d1[0]2 + d1[1]2 + ... + d1[n]2)
||d2|| = square root(d2[0]2 + d2[1]2 + ... + d2[n]2)*/ 

  select user_id , 10000 * (Dot_product/ d1*d2 ) as  cos_similarity from 
( select user_id , sum(Dot_product) Dot_product , sqrt( sum(d1)) d1   ,sqrt( sum(d2) ) d2
from 
( SELECT 

user_id, 
global_weight_X_idf * local_weight_X_idf  Dot_product ,
global_weight_X_idf * global_weight_X_idf   d1,  
local_weight_X_idf  * local_weight_X_idf    d2  

FROM [imdb3.help3_tfidf_weighted]  ) 
group by 1 ) 

### Create TF/IDF for DVR   ### 
select * , word_counter TF ,   word_counter * IDF as TFIDF , 1+log10(word_counter ) WTF  , IDF *  ( 1+log10(word_counter ) ) WTFIDF  from 
( select  rnk, a.word word, word_counter , 
global_weight , cum_sum,prev_cum_sum, added, users_per_word  , log10(3969 /users_per_word ) IDF    from 
(select  * ,  abs(100- (  cum_sum / prev_cum_sum)  * 100)  as added  from 
(select *, lead (cum_sum) over (order by cum_sum desc  ) as prev_cum_sum   from 
( SELECT 
rnk, word , word_counter , 
global_weight , 
-- lead (global_weight) over (order by global_weight  ) as prev_weight , 
sum (global_weight) over (order by global_weight desc ) as cum_sum   FROM [imdb3.help2]
order by global_weight  desc  )  order by global_weight  desc )  where word_counter > 5  ) a
join (SELECT count(distinct  user_id , 99999) as users_per_word , word  FROM [imdb3.help33]  group by word ) b on a.word=b.word  )  order by rnk   

### Results_kl_dist_chapter_DVR_10 ### 
--   KL Distances of chapter from general DVR 
 
SELECT
  cid,
  SUM(KL_SYM) KL_distance
FROM (
  SELECT
    *,
    IF(cid IS NULL, (1/1000), (( global_weight- local_weight) * log10 (global_weight / local_weight )) ) AS KL_SYM
  FROM (
    SELECT
       cid,
       word word,
       chapter_counter counter,
       in_chapter_weight local_weight,
       global_weight global_weight,
      (1/10000) epsilon
   
      FROM
       [validation.books_10chapters_VECTORS]       
      )) 
GROUP BY
  1
