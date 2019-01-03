#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 16:05:59 2018

@author: Bounab Yazid
"""
import re
import os
import json
from os import listdir
from os.path import isfile, join

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk import pos_tag, word_tokenize

from stanfordcorenlp import StanfordCoreNLP
from nltk.tag import StanfordNERTagger

import numpy as np

import collections
import pandas as pd

from collections import Counter

#https://summari.es/
#https://towardsdatascience.com/very-simple-python-script-for-extracting-most-common-words-from-a-story-1e3570d0b9d0
#https://medium.com/agatha-codes/using-textual-analysis-to-quantify-a-cast-of-characters-4f3baecdb5c

stopwords = stopwords.words('english')
wordcount = {}
PosList = []

#_______________________________________________________________

def TextFile_To_Sentences(TextFile):
    with open(TextFile, encoding="ISO-8859-1") as f:
         text = f.read()
    sentences = sent_tokenize(text)
    return sentences
#_______________________________________________________________

def Read_TextFile(TextFile):
    with open(TextFile, encoding="ISO-8859-1") as f:
         Text = f.read()
         f.close()
    #print (Text)
    punct = re.sub('[A-Za-z]|[0-9]|[\n\t]','',Text)
    SymbList = list(dict.fromkeys(punct).keys())
    #print (SymbList)
    return Text,SymbList
#_______________________________________________________________
    
def Preprocessing_Text(Text,punct):
    Text = re.sub('[0-9]+', ' ', Text)
    Text = Text.replace('é','e')
    for p in punct:
        Text = Text.replace(p,' ')
    
    Text = re.sub(' +',' ', Text)
    Text = Text.strip()
    #Text = Text.lower()
    #print (Text)
    return Text

#______________________________________________________________
#https://summari.es/download/
def Read_JsonFile():
    path = '/home/polo/.config/spyder-py3/Co-referece/thin/test-shell.json'
    #json_data = open(path)
    #data = json.load(json_data)
    data = []
    with open(path) as f:
        for line in f:
            data.append(json.loads(line))
            break
    print (data)

#_______________________________________________________________

def Read_BBC_News_Summary():
    News_Articles = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/News Articles'
    Summaries = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/Summaries'
    Machine_Summary = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/Machine Summary'
    
    SubDirectories = os.listdir(News_Articles)
    
    try:  
        os.mkdir(Machine_Summary)
    except OSError:  
                print ("Creation of the directory %s failed" % Machine_Summary)
    for subdir in os.listdir(News_Articles):
        try:  
            os.mkdir(Machine_Summary+'/'+subdir)
        except OSError:  
                print ("Creation of the directory %s failed" % subdir)

    print (SubDirectories)
    
    n_print = int(input("How many most common words to print: "))
    
    for subdir in SubDirectories:
        files = [f for f in listdir(News_Articles+'/'+subdir) if isfile(join(News_Articles+'/'+subdir, f))]    
        for f in files:
            print(News_Articles+'/'+subdir+'/'+f)
            MainSents = Summarize_Story(News_Articles+'/'+subdir+'/'+f,n_print)
            with open(Machine_Summary+'/'+subdir+'/'+f, "w") as output:
                 output.write("".join(MainSents))
            
        print('____________________________________________________')

#_______________________________________________________________
def Term_Frequecy(Text,punct):
    Text = Preprocessing_Text(Text,punct)
    for word in Text.lower().split():
        if word not in stopwords:
           if word not in wordcount:
              wordcount[word] = 1
           else:
                wordcount[word] += 1
    #print(wordcount)
#_______________________________________________________________

def Text_tokenize(Text):
    Tokens = word_tokenize(Text)
    return Tokens

def Tagging(Text):
    Tagged_Text = pos_tag(Text_tokenize(Text))
    return Tagged_Text
#_______________________________________________________________

def NE_Tagger(Text):
    st = StanfordNERTagger('/home/polo/Downloads/stanford-ner-2018-02-27/classifiers/english.all.3class.distsim.crf.ser.gz',
					       '/home/polo/Downloads/stanford-ner-2018-02-27/stanford-ner.jar', encoding='utf-8')

    tokenized_text = word_tokenize(Text)
    classified_text = st.tag(tokenized_text)

    #print(classified_text)
    return classified_text
#_______________________________________________________________
    
def find_proper_nouns(Tagged_Text):
    proper_nouns = []
    i = 0
    while i < len(Tagged_Text):
         if Tagged_Text[i][1] == 'NNP':
            if Tagged_Text[i+1][1] == 'NNP':
               proper_nouns.append(Tagged_Text[i][0].lower()+" " +Tagged_Text[i+1][0].lower())
               i+=1
            else:
                proper_nouns.append(Tagged_Text[i][0].lower())
         i+=1
    return proper_nouns

#_______________________________________________________________

def summarize_text(proper_nouns, top_num):
    counts = dict(Counter(proper_nouns).most_common(top_num))
    return counts

#_______________________________________________________________
    
def MainCharacter(Text,n_print):
    NER_Text = [(x.lower(), y) for x,y in NE_Tagger(Text)]
    NER_Text = dict(NER_Text)
    
    word_counter = collections.Counter(wordcount)
    MainChar = max(word_counter, key=word_counter.get)
    #print('Main Character :',MainChar)
    return MainChar

#_______________________________________________________________

def SentsMainChar(sentences,MainChar):
    #but do the SRL before get sentences that contains the main Char
    MainSents = []
    for sent in sentences:
        if MainChar in sent.lower():
           MainSents.append(sent)
    return MainSents

#_______________________________________________________________

def MostCommon(n_print,Text):
    #Tagged_Text = Tagging(Text)
    #Tagged_Text = [(x.lower(), y) for x,y in Tagged_Text]
    #PosList = set([X[1] for X in Tagged_Text])
    #print (PosList)
    #print (Tagged_Text)
    #Tagged_Text = dict(Tagged_Text)

    NER_Text = [(x.lower(), y) for x,y in NE_Tagger(Text)]
    NER_Text = dict(NER_Text)
    #print (NER_Text)
    
    print("\nOK. The {} most common words are as follows\n".format(n_print))
    word_counter = collections.Counter(wordcount)
    #print(word_counter)
    for word, count in word_counter.most_common(n_print):
        #print(word, ": ", count, ": ",Tagged_Text[word])
        print(word, ": ", count, ": ",NER_Text[word])
    
    print('Most Common Term ',max(word_counter, key=word_counter.get))
    
        
#_______________________________________________________________

def DrawMostCommon(n_print):
    word_counter = collections.Counter(wordcount)
    lst = word_counter.most_common(n_print)
    df = pd.DataFrame(lst, columns = ['Word', 'Count'])
    df.plot.bar(x='Word',y='Count')

#_______________________________________________________________

def Simplified_Sentence(Sentence):
    Simple_Sent = Sentence
    #_____________________parentheticals________________________
    Simple_Sent = re.sub('".*?"', '', Simple_Sent) # remove  "...."
    Simple_Sent = re.sub('\(.*?\)', '', Simple_Sent) # remove (...)
    
    #Relative_Clause(Sentence)
    #non-restrictive
    #restrictive appositive phrases 
    #participial phrases offset by commas 

    #adjective and adverb phrases delimited by punctuation 
    #particular prepositional phrases 
    #lead noun phrases 
    #intra-sentential attributions 
    #___________________________________________________________
    return Simple_Sent
#_______________________________________________________________

def Simplified_Sentences(Sentences):
    Simple_Sents = []
    for Sentence in Sentences:
        #print (Sentence)
        Simplifed_Sent = Simplified_Sentence(Sentence)
        Simple_Sents.append(Simplifed_Sent)
    return Simple_Sents

#_______________________________________________________________

def Summarize_Story0():
    Text,punct = Read_TextFile('Alan Turing.txt')
    Precessed_Text = Preprocessing_Text(Text,punct)

    Term_Frequecy(Precessed_Text,punct)
    n_print = int(input("How many most common words to print: "))
    DrawMostCommon(n_print)

    print('____________________________________________________')

    MostCommon(n_print,Text)
    MainChar = MainCharacter(Text,n_print)

    sentences = TextFile_To_Sentences('Alan Turing.txt')
    #print ("\n".join(sentences))
    print('____________________________________________________')
    MainSents = Simplified_Sentences(SentsMainChar(sentences,MainChar))
    print ("\n.............\n".join(MainSents))
    print('____________________________________________________')
    print('Number of Sentences Containing Main Character ',MainChar,' = ', len(MainSents))
    #proper_nouns = find_proper_nouns(Tagged_Text)
    #print (summarize_text(proper_nouns, 10))
    print('____________________________________________________')
    with open("MSummary Alan Turing.txt", "w") as output:
         output.write("".join(MainSents))

#_______________________________________________________________

def Summarize_Story(filename,n_print):
    Text,punct = Read_TextFile(filename)
    Precessed_Text = Preprocessing_Text(Text,punct)

    Term_Frequecy(Precessed_Text,punct)
    
    MainChar = MainCharacter(Text,n_print)

    sentences = TextFile_To_Sentences(filename)

    MainSents = SentsMainChar(sentences,MainChar)
    MainSents = Simplified_Sentences(MainSents)
    
    return MainSents
#_______________________________________________________________
#Summarize_Story(filename,15)
    
#Read_BBC_News_Summary()
