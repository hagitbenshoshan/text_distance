### creating book_by_chapter_sample 
```
SELECT *  FROM [books.books_by_chapters] 
where book_name in 
(
'A_Study_In_Scarlet-chapters',
'A_Tale_of_Two_Cities_by_Charles_Dickens-chapters',
'Adventures_of_Huckleberry_Finn_by_Mark_Twain-chapters',
'Alices_Adventures_in_Wonderland_by_Lewis_Carroll-chapters',
'Anne_of_Green_Gables-chapters',
'Emma_by_Jane_Austen-chapters',
'Great_Expectations_by_Charles_Dickens-chapters',
'Gullivers_Travels-chapters',
'Jane_Eyre_An_Autobiography_by_Charlotte_Bronte-chapters',
'Little_Women_by_Loui-chapters',
'Oliver_Twist-chapters',
'Peter_Pan_by_J._M.__Barrie-chapters',
'Pride_and_Prejudice_by_Jane_Austen-chapters',
'Sense_and_Sensibility_by_Jane_Austen-chapters',
'The_Adventures_of_Tom_Sawyer_by_Mark_Twain-chapters',
'The_King_in_Yellow_by_Robert_W.__Chambers-chapters',
'The_Life_and_Adventures_of_Robinson_Crusoe-chapters',
'The_Picture_of_Dorian_Gray_by_Oscar_Wilde-chapters',
'The_Time_Machine-chapters',
'Treasure_Island_by_Robert_Louis_Stevenson-chapters',
'Wuthering_Heigh-chapters') 
and chapter_id<11 
and pos in ('NN','NNS','JJ','JJR','JJS')    
and word not in ('“','’','-','(',')','‘','\'','_','[',']')
```

### creating help2_NN_books_sample/help2_JJ_books_sample (aggregation by word,book) , local_weight=weight inside a book
```
select  * ,local_counter/words_per_book local_weight ,  global_counter/tot as global_weight from 
(select * , sum(local_counter) over (partition by book_name) as words_per_book  from  
(select * from 
(SELECT book_name   , word , count(word)  over (partition by  book_name,word ) as local_counter,  count(word) over (partition by  word) as  global_counter , count(*) over () as tot
 FROM [books.books_by_chapter_sample]  where  pos in ('NN','NNS')  --   ('JJ','JJR','JJS') 
 order by 3 desc ) group by 1,2,3,4,5 ) )
```
# creating improved aggregation - Cleaning the current book from the aggregation (help2_JJ_sample_clean table) 
```
SELECT
  *,
  local_counter/words_per_book local_weight,
  global_counter/tot AS global_weight,
  (global_counter-local_counter)/tot AS global_weight_clean,
  (global_counter-local_counter) as     global_counter_clean
FROM (
  SELECT
    *,
    SUM(local_counter) OVER (PARTITION BY book_name) AS words_per_book
  FROM (
    SELECT
      *
    FROM (
      SELECT
        book_name,
        word,
        pos,
        COUNT(word) OVER (PARTITION BY book_name, word ) AS local_counter,
        COUNT(word) OVER (PARTITION BY word)             AS global_counter,
        COUNT(*) OVER () AS tot
      FROM
        [books.book_by_chapter_sample] where  pos in ('JJ','JJR','JJS')    
      ORDER BY         3 DESC )
    GROUP BY
      1,      2,      3,      4,      5,      6) )
``` 
### creating help3_NN_books_sample (aggregation by word,chapter,book) , local_weight=weight inside a chapter
``` 
select  *    ,chapter_counter/words_per_chapter in_chapter_weight ,book_counter/words_per_book in_book_weight ,  global_counter/tot as global_weight ,  
          (book_counter-chapter_counter)/words_per_book AS in_book_weight_clean,
          (book_counter-chapter_counter) as     in_book_counter_clean , 
          (global_counter-chapter_counter) as   global_counter_clean, 
          (global_counter-chapter_counter)/(tot-chapter_counter)  as   global_weight_clean  
from 
(
select * from ( 
SELECT book_name  ,chapter_id , word   
                   ,count(word)  over (partition by  book_name,chapter_id,word ) as chapter_counter
                   ,count(word)  over (partition by  book_name,word )     as book_counter
                   ,count(word)  over (partition by  word)                as  global_counter   
                   ,count(*)     over (partition by book_name,chapter_id) as words_per_chapter 
                   ,count(*)     over (partition by book_name)            as words_per_book
                   ,count(*)     over () as tot
 FROM [books.book_by_chapter_sample] where  pos in ('NN','NNS')    )   group by 1,2,3,4,5,6,7,8,9   )    order by global_weight desc 
```
### calculating distance of chapter from its own book (distance_of_chapter_from_its_book_NN)  
```
SELECT
  book_name,
  chapter_id,
  SUM(words_per_chapter) words_per_chapter,
  SUM(words_per_book) words_per_book,
  SUM(words) common_words_per_chapter,
  (SUM(distance_per_user)) /2 distance_per_user
FROM (
  SELECT
    book_name,    chapter_id,    words_per_book,    words_per_chapter,    SUM(distance) AS distance_per_user,    COUNT(*) AS words
  FROM (
    SELECT
      word,
      gln,
      tot,
      lln,
      book_name book_name,
      chapter_id,
      words_per_book words_per_book,
      words_per_chapter words_per_chapter,
      -- Calculating distance between local to global weight for each word
      if ( lln IS NULL,        gln,        ABS( gln - lln )) AS distance    FROM 
      (      SELECT
        *,
        in_book_weight AS gln,
        in_chapter_weight lln
      FROM
        [books.help3_NN_books_sample] )   ) exist_in_local
  GROUP BY     1,    2,    3,    4 ),
    -- Calculating distance for missing words 
  (
  SELECT
    book_name,
    chapter_id,
    1- SUM(in_book_weight ) distance_per_user,
    SUM(in_book_weight ) in_book_weight
  FROM
    [books.help3_NN_books_sample]
  GROUP BY     book_name,    chapter_id   ) exist_in_global
GROUP BY
  1,  2 ORDER BY  1,  2
```
### calculating distance of chapter in virtual book from DVR (distance_of_chapter_from_virtual_DVR_JJ)  
```
SELECT
  book_name,
  chapter_id,
  SUM(words_per_chapter) words_per_chapter,
  SUM(words_per_book) words_per_book,
  SUM(words) common_words_per_chapter,
  (SUM(distance_per_user)) /2 distance_per_user
FROM (
  SELECT
    book_name,    chapter_id,    words_per_book,    words_per_chapter,    SUM(distance) AS distance_per_user,    COUNT(*) AS words
  FROM (
    SELECT
      word,
      gln,
      tot,
      lln,
      book_name book_name,
      chapter_id,
      words_per_book words_per_book,
      words_per_chapter words_per_chapter,
      -- Calculating distance between local to global weight for each word
      if ( lln IS NULL,        gln,        ABS( gln - lln )) AS distance    FROM 
      (      SELECT
        *,
        global_weight  AS gln,
        in_chapter_weight lln
      FROM
        [books.help3_JJ_books_sample_virt] )   ) exist_in_local
  GROUP BY     1,    2,    3,    4 ),
    -- Calculating distance for missing words 
  (
  SELECT
    book_name,
    chapter_id,
    1- SUM(global_weight  ) distance_per_user,
    SUM(global_weight  ) global_weight
  FROM
    [books.help3_JJ_books_sample_virt]
  GROUP BY     book_name,    chapter_id   ) exist_in_global
GROUP BY
  1,  2 ORDER BY  1,  2
```
### creating 21 virtual books (books_by_chapter_sample_virt_NN / books_by_chapter_sample_virt_JJ) 
```
  select   concat('virt_', string(ABS(HASH(integer( 1000* (rand()))) )% 21 ))   book_name ,book_name old_book_name,	
  chapter_id   from  
 ( select  chapter_id , book_name   from  [books.books_by_chapter_sample] where pos contains 'NN'  group by 1,2  )  order by 1
  
``` 
### OLD calculating distance of chapter from its own book (distance_of_chapter_from_its_book_NN)   
```  
 -- Distance between book and its chapters  *** distances_of_chapter_fixed  ***
  
  -- The distance is the summary of missing_in_local+distance from global

select      book_name ,chapter_id,sum(words_per_chapter) words_per_chapter  ,sum(words_per_book) words_per_book , sum(words) common_words_per_chapter,  (sum(distance_per_user)) /2  distance_per_user ,  from 
--### Summerize the distance per each user , for his existing words 
(select   book_name  book_name,  chapter_id , words_per_book,words_per_chapter, sum(distance) as distance_per_user ,count(*) as words from 
(select   global.word,global.gln, local.tot , local.lln , local.book_name book_name , chapter_id, global.words_per_book words_per_book,local.words_per_chapter words_per_chapter,

-- Calculating distance between local to global weight for each word 
if (local.lln is null  ,global.gln ,  abs(global.gln - local.lln ))    as distance    from 


 (select   book_name , a.word  as word , a.gln as gln  ,words_per_book  from 
--Each word in the general corpus 
 (select   book_name, word   as  word,    local_weight     as gln  , words_per_book   from [books.help2_NN_books_sample]   ) a 
  )  global  
--Inner join 
  Join 
-- Each word in the local list of the chapter   
(SELECT * ,in_chapter_weight            lln FROM [books.help3_NN_books_sample]   
 )  local 

 on   global.word=local.word  
 and  global.book_name=local.book_name 
  
  ) exist_in_local
  group by 1,2,3 ,4
) , 


( 
-- Substract the weight of existing words from 1 , to get the global weight of the missing words per chapter    
   select book_name ,chapter_id, 1-sum(weight) distance_per_user   from  

   ( select d.book_name  book_name, c.weight weight,chapter_id     from 
-- Global weight of all words per book    
   (select book_name,word,local_weight weight   from [books.help2_NN_books_sample]     ) c
     join
--  join Local words only for each chapter    
   (select     book_name,chapter_id, word       FROM [books.help3_NN_books_sample]     )  d 
    on         c.word=d.word
    where      c.book_name=d.book_name 
    ) 
	 group by book_name,chapter_id)  missing_in_local 
	
   group by 1,2  order by 1,2 
```   
   ### Calculating matrix of all chapters distance (example of 3 books) 
```
select book_name ,book_name2nd , chapter_id  , chapter_id2nd ,  sum(diff/2) as dist from 
    (  select a.*, b.book_name book_name2nd, b.chapter_id chapter_id2nd , b.in_chapter_weight  in_chapter_weight2nd  , abs( a.in_chapter_weight-b.in_chapter_weight) diff from 
    (select book_name,word,chapter_id,ifnull(in_chapter_weight,0)  in_chapter_weight  from 
    ( SELECT  * FROM `books.help5_NN_books_sample` CROSS JOIN `books.help4_NN_books_sample`   CROSS JOIN `books.help7_NN_books_sample` 
       where book_name in ('Emma_by_Jane_Austen-chapters','Pride_and_Prejudice_by_Jane_Austen-chapters' , 'Alices_Adventures_in_Wonderland_by_Lewis_Carroll-chapters'	)  
      )
      left   join 
     `books.help3_NN_books_sample`   using(book_name,word,chapter_id)
       )    a
      left    join 
      (select book_name,word,chapter_id  ,ifnull(in_chapter_weight,0)  in_chapter_weight   from 
      (SELECT  * FROM `books.help5_NN_books_sample` CROSS JOIN `books.help4_NN_books_sample`   CROSS JOIN `books.help7_NN_books_sample` 
       where book_name in ('Emma_by_Jane_Austen-chapters','Pride_and_Prejudice_by_Jane_Austen-chapters' , 
       'Alices_Adventures_in_Wonderland_by_Lewis_Carroll-chapters')  
     )
      left   join 
     `books.help3_NN_books_sample`   using(book_name,word,chapter_id)
       )   b
       using(word ) 
       where  
       a.in_chapter_weight<>b.in_chapter_weight ) 
       group by 1,2 ,3 ,4  order by 1,2,3,4
```
