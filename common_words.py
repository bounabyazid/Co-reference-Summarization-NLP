#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 15:05:16 2018

@author: polo
"""
#https://towardsdatascience.com/very-simple-python-script-for-extracting-most-common-words-from-a-story-1e3570d0b9d0
import re

import collections
import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

# Stopwords
stopwords = stopwords.words('english')

# Instantiate a dictionary, and for every word in the file, 
# Add to the dictionary if it doesn't exist. If it does, increase the count.
wordcount = {}
#_______________________________________________________________

# Read input file, note the encoding is specified here 

def Read_Text(TextFile):
    with open(TextFile, encoding="utf8") as f:
         Text = f.read()
         f.close()
    punct = re.sub('[A-Za-z]|[0-9]|[\n\t]','',Text)
    SymbList = list(dict.fromkeys(punct).keys())
    print (SymbList)
    return Text,SymbList
#_______________________________________________________________

def Preprocessing_Text(Text,punct):
    Text = re.sub('[0-9]+', ' ', Text)
    Text = Text.replace('é','e')
    for p in punct:
        Text = Text.replace(p,' ')
    
    Text = re.sub(' +',' ', Text)
    Text = Text.strip()
    Text = Text.lower()
    
    #print (Text)
    for word in Text.lower().split():
        if word not in stopwords:
           if word not in wordcount:
              wordcount[word] = 1
           else:
                wordcount[word] += 1
    #print(wordcount)

#_______________________________________________________________

def MostCommon(n_print):
    # Print most common word
    print("\nOK. The {} most common words are as follows\n".format(n_print))
    word_counter = collections.Counter(wordcount)
    for word, count in word_counter.most_common(n_print):
        print(word, ": ", count)
#_______________________________________________________________

def DrawMostCommon(n_print):
    # Create a data frame of the most common words 
    # Draw a bar chart
    word_counter = collections.Counter(wordcount)
    lst = word_counter.most_common(n_print)
    df = pd.DataFrame(lst, columns = ['Word', 'Count'])
    df.plot.bar(x='Word',y='Count')

#_______________________________________________________________
    
Text,punct = Read_Text('Alan Turing.txt')

Preprocessing_Text(Text,punct)

n_print = int(input("How many most common words to print: "))

DrawMostCommon(n_print)
MostCommon(n_print)
