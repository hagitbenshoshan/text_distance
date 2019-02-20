
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 23:39:43 2016

@author: hagit
"""
# encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import os
import codecs
import nltk

# modify here your NLTK directory name
nltk.data.path.append("/my_nltk_directory/nltk")

import glob

from nltk.stem     import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus   import stopwords
from nltk.tokenize import RegexpTokenizer

import fnmatch
import os

matches = []
# modify here your chapters directory name
for root, dirnames, filenames in os.walk('/books_by_chapters'):
    for filename in fnmatch.filter(filenames, '*.txt'):
        matches.append(os.path.join(root, filename))
        print filename



stopset = set(stopwords.words('english'))

ps = nltk.PorterStemmer()
snowball_stemmer = SnowballStemmer("english")

for book_filename in matches:
    print("Reading '{0}'...".format(book_filename))
    str2=book_filename.split('/')
    n=len(str2)
    book_chapter=str2[n-1]
    book_dir   = str2[n - 2]
    print book_chapter
    print book_dir
    file=open(book_filename,'r')            
    out_filename = book_filename + '.csv'   
    try:
        os.remove(out_filename)
    except OSError:
        pass


    out     = open(out_filename,'w' )

    for line in file:
        line=unicode(line, errors='ignore')
        my_clean_text=''
        toker = RegexpTokenizer(r'((?<=[^\w\s])\w(?=[^\w\s])|(\W))+', gaps=True)
        words = toker.tokenize(line)

        words= [w for w in words if not w in stopset]
        for w in words:
            myword=snowball_stemmer.stem(w.lower())
            my_clean_text = my_clean_text+' '+myword
            tagged_word=nltk.pos_tag(nltk.word_tokenize(myword))
            for (theme,tag) in tagged_word:
                try:
                    if tag.encode('utf-8').strip()!='.':
                        out.write(book_dir+','+book_chapter+','+w+','+tag.encode('utf-8').strip()+','+theme.encode('utf-8').strip()+'\n')
                except:
                    pass
    out.close()
    file.close()



