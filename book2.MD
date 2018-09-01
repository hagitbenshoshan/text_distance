### create the base table ###
select * ,'NN' pos,  counter_in_corpus/words_in_corpus as global_weight ,counter_in_book/words_in_book as in_book_weight  ,counter_in_chapter/words_in_chapter as local_weight    from 
( select *  from 
( SELECT word ,book_name , chapter_id , 
count(*) over (partition by word) as counter_in_corpus , 
count(*) over (partition by book_name,word ) as counter_in_book , 
count(*) over (partition by book_name,chapter_id,word ) as counter_in_chapter, 
count(*) over () as words_in_corpus , 
count(*) over (partition by book_name) as words_in_book , 
count(*) over (partition by book_name,chapter_id) as words_in_chapter 
FROM `cooladata-cs-solutions.books2.raw_data_NN`   where book_name  not in ('pg39681','thehappy','Leaves_of_Grass','Life','pg34476','pg16435')   ) 
where counter_in_corpus > 5  and words_in_chapter > 150   
group by 1,2,3,4,5,6,7,8,9 ) 
