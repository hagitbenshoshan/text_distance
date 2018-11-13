### create the base table NN_base ###
```
select * ,'NN' pos,  counter_in_corpus/words_in_corpus as global_weight ,counter_in_book/words_in_book as in_book_weight  ,counter_in_chapter/words_in_chapter as local_weight    from 
( select *  from 
( SELECT word ,book_name , chapter_id , 
count(*) over (partition by word) as counter_in_corpus , 
count(*) over (partition by book_name,word ) as counter_in_book , 
count(*) over (partition by book_name,chapter_id,word ) as counter_in_chapter, 
count(*) over () as words_in_corpus , 
count(*) over (partition by book_name) as words_in_book , 
count(*) over (partition by book_name,chapter_id) as words_in_chapter 
FROM `books2.raw_data_NN`   where book_name  not in ('pg39681','thehappy','Leaves_of_Grass','Life','pg34476','pg16435')   ) 
where counter_in_corpus > 5  and words_in_chapter > 150   
group by 1,2,3,4,5,6,7,8,9 ) 
```
### KL Distances of chapter from its book ###
```
select chapter_id ,book_name, avg(words_in_chapter) words_in_chapter, sum(KL_SYM) KL_distance , sum(missing) missing , sum(total) total , sum(present) present   , sum(missing) /sum(total)  as missing_pct , 1/sum(total) epsilon , 
sum(missing_in_top_10)  missing_in_top_10 , 
sum(missing_in_top_20)  missing_in_top_20    from
( SELECT *,
if(chapter_id is null ,  1/sum(total) over ()  , (( global_weight- local_weight) * log10 (global_weight / local_weight )) ) AS KL_SYM FROM 
(select *, if ( second_part.counter_in_chapter> 0 ,0 , 1 ) as missing   , if ( second_part.counter_in_chapter> 0 ,1 , 0 ) as present    , 1 as total  ,
if (inbook_rank < 21 and  second_part.counter_in_chapter is null,1,0 )  as missing_in_top_20  , 
if (inbook_rank < 11 and  second_part.counter_in_chapter is null,1,0 )  as missing_in_top_10 from 
(select * from 
( select * from 
  (SELECT book_name,chapter_id  from  `books2.NN_base`   group by 1,2  ) c
  left join 
  (SELECT word ,book_name,in_book_weight global_weight,rank() over (partition by book_name order by in_book_weight desc ) as inbook_rank   from  `books2.NN_base`   group by 1,2,3  ) b
  using (book_name) 
)) first_part 
left   join
(SELECT chapter_id , word, counter_in_chapter , words_in_chapter, local_weight, book_name ,word  as joiner  FROM `books2.NN_base`   ) second_part 
using(book_name, chapter_id , word)    ))
GROUP BY 1,2  order by 4 desc 
```
### KL and L1Norm distances ### 
```
select chapter_id ,book_name, avg(words_in_chapter) words_in_chapter, sum(KL_SYM) KL_distance, sum(L1_SYM) L1_distance , sum(missing) missing , sum(total) total , sum(present) present   , sum(missing) /sum(total)  as missing_pct , 1/sum(total) epsilon , 
sum(missing_in_top_10)  missing_in_top_10 , 
sum(missing_in_top_20)  missing_in_top_20    from
( SELECT *,
if(joiner is null ,  1/sum(total) over ()  , (( global_weight- local_weight) * log10 (global_weight / local_weight )) ) AS KL_SYM  , abs(global_weight-ifnull(local_weight,0) ) as L1_SYM FROM 
(select *, if ( second_part.counter_in_chapter> 0 ,0 , 1 ) as missing   , if ( second_part.counter_in_chapter> 0 ,1 , 0 ) as present    , 1 as total  ,
if (inbook_rank < 21 and  second_part.counter_in_chapter is null,1,0 )  as missing_in_top_20  , 
if (inbook_rank < 11 and  second_part.counter_in_chapter is null,1,0 )  as missing_in_top_10 from 
(select * from 
( select * from 
  (SELECT book_name,chapter_id  from  `cooladata-cs-solutions.books2.NN_base`   group by 1,2  ) c
  left join 
  (SELECT word ,book_name,in_book_weight global_weight,rank() over (partition by book_name order by in_book_weight desc ) as inbook_rank   from  `cooladata-cs-solutions.books2.NN_base`   group by 1,2,3  ) b
  using (book_name) 
)) first_part 
left   join
(SELECT chapter_id , word, counter_in_chapter , words_in_chapter, local_weight, book_name ,word  as joiner  FROM `cooladata-cs-solutions.books2.NN_base`   ) second_part 
using(book_name, chapter_id , word)    ))
GROUP BY 1,2  order by 4 desc
```
### KL / L1 distance for 10 chapters  : Distance of chapter from its book (newest version) ###
```
select chapter_id ,book_name, avg(words_in_chapter) words_in_chapter, sum(KL_SYM) KL_distance, sum(L1_SYM)/2  L1_distance , sum(missing) missing , sum(total) total , sum(present) present   , sum(missing) /sum(total)  as missing_pct , 1/sum(total) epsilon , 
sum(missing_in_top_10)  missing_in_top_10 , 
sum(missing_in_top_20)  missing_in_top_20    
from
( SELECT *, 
if(joiner is null ,  1/sum(total) over ()  , (( global_weight- local_weight) * log10 (global_weight / local_weight )) ) AS KL_SYM  , abs(global_weight-ifnull(local_weight,0) ) as L1_SYM FROM 
(select *, if ( second_part.counter_in_chapter> 0 ,0 , 1 ) as missing   , if ( second_part.counter_in_chapter> 0 ,1 , 0 ) as present    , 1 as total  ,
if (inbook_rank < 21 and  second_part.counter_in_chapter is null,1,0 )  as missing_in_top_20  , 
if (inbook_rank < 11 and  second_part.counter_in_chapter is null,1,0 )  as missing_in_top_10 from 

(select * from   /* N Chapters (for example 10 ) lines X  each word  , with the global weight (in book) of the word  [Grey,02.txt,youth,0.00016999575010624734,945] N (10)  identical rows 	*/ 
( select * from 
/* list of all the chapters in all the books */ 
  (SELECT book_name,chapter_id  from  `cooladata-cs-solutions.books2.NN_base_10`     group by 1,2  ) c
  left join 
  /* the global weight (in book weight) and the global rank (in book rank) of a word */ 
  (SELECT word ,book_name,in_book_weight global_weight,rank() over (partition by book_name order by in_book_weight desc ) as inbook_rank   from  `cooladata-cs-solutions.books2.NN_base_10`   group by 1,2,3  ) b 
  using (book_name) 
)) first_part 
left   join  /* Second_part is  all the words in all the chapters in all the books , we are using it to take the local weight in chapter , and to show the statistics for the missing words percentage */ 
(SELECT chapter_id , word, counter_in_chapter , words_in_chapter, local_weight, book_name ,word  as joiner  FROM `cooladata-cs-solutions.books2.NN_base_10`   ) second_part 
using(book_name, chapter_id , word)  )  ) 
GROUP BY 1,2  order by 4 desc
```
### KL / L1 distance of book from DVR 
```
-- Distance of single book from DVR 
SELECT
  book_name,
  sum(counter_in_book) counter_in_book,
  SUM(KL_SYM) KL_distance,
  SUM(L1_SYM)/2 L1_distance 
  
FROM (  
  SELECT
    *,
    IF(local_weight IS NULL,
    1/162801  ,   -- number of records in NN_base_10 table 
      (( global_weight- local_weight) * log10 (global_weight / local_weight )) ) AS KL_SYM,
    ABS(global_weight-ifnull(local_weight,
        0) ) AS L1_SYM
  FROM (  
(select * from 
             (select  word , global_weight   FROM `cooladata-cs-solutions.books2.NN_base_10`   group by 1,2)    -- All words (global weight) x
cross  join  (select  book_name  FROM `cooladata-cs-solutions.books2.NN_base_10`  group by 1 ) ) p1             -- All books 
left join 
(   SELECT  word   , book_name ,counter_in_book ,counter_in_corpus   ,in_book_weight local_weight , words_in_book , words_in_corpus   FROM `cooladata-cs-solutions.books2.NN_base_10`  --In book weights
group by 1,2,3,4,5,6,7 )  
using (word,book_name ) )       ) group by 1
 ```
