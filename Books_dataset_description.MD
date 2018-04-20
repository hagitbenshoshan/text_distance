% creating book_by_chapter_sample %

SELECT *  FROM [books.books_by_chapter] 
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
and chapter_id in ('01.txt','02.txt','03.txt','04.txt','05.txt','06.txt','07.txt','08.txt','09.txt','10.txt')
and pos in ('NN','NNS') 
and word not in ('“','’','-','(',')','‘','\'','_','[',']')


-- creating help2_NN_books_sample (aggregation by word,book) , local_weight=weight inside a book

select  * ,local_counter/words_per_book local_weight ,  global_counter/tot as global_weight from 
(select * , sum(local_counter) over (partition by book_name) as words_per_book  from  
(select * from 
(SELECT book_name   , word , count(word)  over (partition by  book_name,word ) as local_counter,  count(word) over (partition by  word) as  global_counter , count(*) over () as tot
 FROM [books.books_by_chapter_sample]   order by 3 desc ) group by 1,2,3,4,5 ) ) 
 
 -- help3_NN_books_sample (aggregation by word,chapter,book) , local_weight=weight inside a chapter

 
select  *    ,chapter_counter/words_per_chapter in_chapter_weight ,book_counter/words_per_book in_book_weight ,  global_counter/tot as global_weight 
from 
(
select * from ( 
SELECT book_name  ,chapter_id , word   
                   ,count(word)  over (partition by  book_name,chapter_id,word ) as chapter_counter
                   ,count(word)  over (partition by  book_name,word ) as book_counter
                   ,count(word)  over (partition by  word) as  global_counter   
                   ,count(*)     over (partition by book_name,chapter_id) as words_per_chapter 
                   ,count(*)     over (partition by book_name) as words_per_book
                   ,count(*)     over () as tot
 FROM [books.books_by_chapter_sample]  )   group by 1,2,3,4,5,6,7,8,9   )    order by global_weight desc 
