### Extract one book and create a  table per book (KL) ###
SELECT *  FROM [cooladata-cs-solutions:books.help4_NN_books]  where book_name = 'Treasure_Island_by_Robert_Louis_Stevenson-chapters' order by chapter_id , weight_in_chapter desc 	


### Create 1 book table (KL_tresure) ###
1) SELECT word,chapter_id, counter, weight_in_chapter local_weight , book_length, chapter_length, counter_in_book, weight_in_book  global_weight  
FROM [cooladata-cs-solutions:books.KL]  where counter_in_book> 5  order by global_weight desc 

2) select word	,chapter_id	,counter	, 	 	 	counter_in_book global_counter ,	 	tot_book_length	, tot_chapter_length , counter/tot_chapter_length	 local_weight ,counter_in_book/tot_book_length global_weight   from 
(
SELECT * , sum(counter)  over () as tot_book_length , sum(counter)  over (partition by chapter_id ) as tot_chapter_length  
          FROM [cooladata-cs-solutions:books.KL_tresure]  )  --ovveride the same table

### Create the DVR (KL_DVR) 
SELECT word,tot_book_length , global_counter , global_weight , count(distinct chapter_id ) in_chapters_counter  FROM [cooladata-cs-solutions:books.KL_tresure]  group by 1,2,3,4


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
        [cooladata-cs-solutions:books.KL_DVR]) b
        left join        
        (SELECT chapter_id  , word, counter , local_weight             
      FROM
        [cooladata-cs-solutions:books.KL_tresure]   ) a -- where user_id in ( 11596,223692, 1002035)  ) a
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
  [cooladata-cs-solutions:books.help4_NN_books]
WHERE
  book_name = 'A_Study_In_Scarlet-chapters'
  AND chapter_id ='01.txt'
ORDER BY
  chapter_id,
  weight_in_chapter DESC

 
