#https://www.kaggle.com/currie32/comparing-books-with-word2vec-and-doc2vec/notebook

# encoding=utf8

book_filename = open("11-0.txt"  , 'r')
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 23:39:43 2016

@author: hagit
"""
# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import json
import os
import nltk

ps = nltk.PorterStemmer()

file=open('11-0.txt','r')
out_filename='all_words_stem_nltk1.csv'
try:
    os.remove(out_filename)
except OSError:
    pass
out     = open(out_filename,'w' )
outjson = open('out1.json','w')
for line in file:

    myline=line.strip()
    my_clean_text=''
    words = nltk.word_tokenize(myline)
    for w in words:
            #print(ps.stem(w) + '  ' + w)
            myword=ps.stem(w.lower())
            my_clean_text = my_clean_text+' '+myword
            tagged_word=nltk.pos_tag(nltk.word_tokenize(myword))
            for (theme,tag) in tagged_word:
                try:
                    if tag.strip()<>'.':
                        out.write(w+'\t'+tag.encode('utf-8').strip()+'\t'+theme.encode('utf-8').strip()+'\n')
                except:
                    pass
    parsed_json['text']=my_clean_text
    outjson.write(json.dumps(parsed_json))
    outjson.write('\n')
outjson.close()
out.close()
file.close()

"""
for book_filename in book_filenames:
    print("Reading '{0}'...".format(book_filename))
    with codecs.open(book_filename, "r", "utf-8") as book_file:
        corpus_raw += book_file.read()
    print("Corpus is now {0} characters long".format(len(corpus_raw)))
    print()

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
raw_sentences = tokenizer.tokenize(corpus_raw)

def sentence_to_wordlist(raw):
    '''Remove all characters except letters'''
    clean = re.sub("[^a-zA-Z]"," ", raw)
    words = clean.split()
    return words
# Clean the raw_sentences and add them to sentences.
sentences = []
for raw_sentence in raw_sentences:
    if len(raw_sentence) > 0:
        sentences.append(sentence_to_wordlist(raw_sentence))

# Take a look at a sentence before and after it is cleaned.
print(raw_sentences[5])
print(sentence_to_wordlist(raw_sentences[5]))



token_count = sum([len(sentence) for sentence in sentences])
print("The book corpus contains {0:,} tokens".format(token_count))

# Set the parameteres for Word2Vec
num_features = 300
min_word_count = 20
num_workers = multiprocessing.cpu_count()
context_size = 10
downsampling = 1e-4
seed = 2


 
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
raw_sentences = tokenizer.tokenize(corpus_raw)

def sentence_to_wordlist(raw):
    '''Remove all characters except letters'''
    clean = re.sub("[^a-zA-Z]"," ", raw)
    words = clean.split()
    return words
# Clean the raw_sentences and add them to sentences.
sentences = []
for raw_sentence in raw_sentences:
    if len(raw_sentence) > 0:
        sentences.append(sentence_to_wordlist(raw_sentence))

# Take a look at a sentence before and after it is cleaned.
print(raw_sentences[5])
print(sentence_to_wordlist(raw_sentences[5]))

token_count = sum([len(sentence) for sentence in sentences])
print("The book corpus contains {0:,} tokens".format(token_count))
"""