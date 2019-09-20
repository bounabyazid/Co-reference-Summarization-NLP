#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 16:05:59 2018

@author: Bounab Yazid
"""
import re
import os
import heapq  

from os import listdir
from os.path import isfile, join

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk import pos_tag, word_tokenize

from nltk.tag import StanfordNERTagger

import collections
import pandas as pd

from gensim.summarization.summarizer import summarize

#https://summari.es/
#https://towardsdatascience.com/very-simple-python-script-for-extracting-most-common-words-from-a-story-1e3570d0b9d0
#https://medium.com/agatha-codes/using-textual-analysis-to-quantify-a-cast-of-characters-4f3baecdb5c

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

#_______________________________________________________________

def Term_Frequecy(Text,punct):
    word_frequencies = {}
    Text = Preprocessing_Text(Text,punct)
    for word in Text.lower().split():
        if word not in stopwords.words('english'):
           if word not in word_frequencies:
              word_frequencies[word] = 1
           else:
                word_frequencies[word] += 1
    return word_frequencies
    
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
    
def MainCharacter(Text,n_print,word_frequencies):
    NER_Text = [(x.lower(), y) for x,y in NE_Tagger(Text)]
    NER_Text = dict(NER_Text)
    
    word_counter = collections.Counter(word_frequencies)
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

def MostCommon(n_print,Text,word_frequencies):

    NER_Text = [(x.lower(), y) for x,y in NE_Tagger(Text)]
    NER_Text = dict(NER_Text)
    #print (NER_Text)
    
    print("\nOK. The {} most common words are as follows\n".format(n_print))
    word_counter = collections.Counter(word_frequencies)
    #print(word_counter)
    for word, count in word_counter.most_common(n_print):
        #print(word, ": ", count, ": ",Tagged_Text[word])
        print(word, ": ", count, ": ",NER_Text[word])
    
    print('Most Common Term ',max(word_counter, key=word_counter.get))
    
        
#_______________________________________________________________

def DrawMostCommon(n_print,word_frequencies):
    word_counter = collections.Counter(word_frequencies)
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
    
def Summarize_Ranked_Sentences(filename):
    word_frequencies = {}
    Weighted_frequencies = {}
    sentence_scores = {}

    Text,punct = Read_TextFile(filename)
    Precessed_Text = Preprocessing_Text(Text,punct)

    word_frequencies = Term_Frequecy(Precessed_Text,punct)
    
    sentences = TextFile_To_Sentences(filename)

    Weighted_frequencies = word_frequencies
    maximum_frequncy = max(word_frequencies.values())
    
    for word in Weighted_frequencies.keys():  
        Weighted_frequencies[word] = (Weighted_frequencies[word]/maximum_frequncy)
        
    for sent in sentences:  
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
               if len(sent.split(' ')) < 30: 
                  if sent not in sentence_scores.keys():
                     sentence_scores[sent] = word_frequencies[word]
                  else:
                      sentence_scores[sent] += word_frequencies[word]
    
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
    summary_sentences = Simplified_Sentences(summary_sentences)
    #summary = ' '.join(summary_sentences)  
    #print(summary)
    return summary_sentences
    
#_______________________________________________________________

def Read_BBC_News_Summary():
    News_Articles = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/News Articles'
    #Summaries = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/Summaries'
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
    
    #n_print = int(input("How many most common words to print: "))
    
    for subdir in SubDirectories:
        files = [f for f in listdir(News_Articles+'/'+subdir) if isfile(join(News_Articles+'/'+subdir, f))]    
        for f in files:
            print(News_Articles+'/'+subdir+'/'+f)
            MainSents = Summarize_Ranked_Sentences(News_Articles+'/'+subdir+'/'+f)
            #MainSents = Summarize_Story(News_Articles+'/'+subdir+'/'+f,n_print)
            with open(Machine_Summary+'/'+subdir+'/'+f, "w") as output:
                 output.write("".join(MainSents))
            
        print('____________________________________________________')

#_______________________________________________________________
        
def Read_StoryTelling_Summary():
    Stories = '/home/polo/.config/spyder-py3/Co-referece/Fairy tales/Storynory'
    #Summaries = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/Summaries'
    Machine_Summary = '/home/polo/.config/spyder-py3/Co-referece/Fairy tales/Machine Summary'
    
    SubDirectories = os.listdir(Stories)
    
    try:  
        os.mkdir(Machine_Summary)
    except OSError:  
                print ("Creation of the directory %s failed" % Machine_Summary)
    for subdir in os.listdir(Stories):
        try:  
            os.mkdir(Machine_Summary+'/'+subdir)
        except OSError:  
                print ("Creation of the directory %s failed" % subdir)

    print (SubDirectories)
    
    #n_print = int(input("How many most common words to print: "))
    
    for subdir in SubDirectories:
        files = [f for f in listdir(Stories+'/'+subdir) if isfile(join(Stories+'/'+subdir, f))]    
        for f in files:
            print(Stories+'/'+subdir+'/'+f)
            MainSents = Summarize_Ranked_Sentences(Stories+'/'+subdir+'/'+f)
            #MainSents = Summarize_Story(News_Articles+'/'+subdir+'/'+f,n_print)
            Text,punct = Read_TextFile(Stories+'/'+subdir+'/'+f)
            with open(Machine_Summary+'/'+subdir+'/'+f, "w") as output:
                 output.write("".join(MainSents))
            
            with open(Machine_Summary+'/'+subdir+'/TextRank.txt', "w") as output:
                 output.write("".join(summarize(Text)))
        print('____________________________________________________')
        
#_______________________________________________________________

#Summarize_Story(filename,15)
    
#Read_BBC_News_Summary()
Read_StoryTelling_Summary()

#print(Summarize_Ranked_Sentences('Alan Turing.txt'))

#print(Summarize_Ranked_Sentences('/home/polo/.config/spyder-py3/Co-referece/Fairy tales/Storynory/Hansel and Gretel/Hansel and Gretel.txt'))