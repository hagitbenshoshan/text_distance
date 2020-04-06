select * from ( SELECT * , row_number() over (partition by user_id order by KL desc) kl_rnk  FROM [cooladata-cs-solutions:imdb.s_kl_results] )
where kl_rnk <=500
