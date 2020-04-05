# text_distance Datasets and algorithm for short text

## Technologies used :  Google BigQuery , Python
                     
### Thesis - Datasetes and algorithm to compute distances between ranked non-conjoint lists 
 
* Input : Short text files documents , each document belongs to one author. 
* The algorithm requires pre-processing text manipulation (tokenize,stemming,POS tagging,remove stop words) performed by https://github.com/hagitbenshoshan/text_distance/blob/master/tokenize_stem_pos.py
Example : The input file name is review_26536435.txt , blongs to user_id = 26536435 
generates the following output:  

review_26536435.txt,matrix,NN,matrix
review_26536435.txt,like,IN,like
review_26536435.txt,time,NN,time
review_26536435.txt,science,NN,scienc
review_26536435.txt,fiction,NN,fiction
review_26536435.txt,movies,NN,movi
review_26536435.txt,makes,VB,make
review_26536435.txt,classic,JJ,classic

* We only include results of "Noun" words
* Raw data is uploaded to Google BigQuery table in the fillowing structure 
* Creating a domain in Google BigQuery : 
 
