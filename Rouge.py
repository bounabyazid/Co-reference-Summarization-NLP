#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 16:00:19 2018

@author: Yazid Bounab
"""
import nltk
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from nltk.translate.bleu_score import sentence_bleu
from Summarization import Summarize_Story

#_______________________________________________________________

#https://rxnlp.com/how-rouge-works-for-evaluation-of-summarization-tasks/#.XCXw9MaxU5k
#https://machinelearningmastery.com/calculate-bleu-score-for-text-python/

#_______________________________________________________________

def Rouge1(MSummary, RefSummary):
        
    #Text1 = 'the cat was found under the bed'
    #Text2 = 'the cat was under the bed'
    
    OverlapWords = len([w for w in MSummary.split() if w in RefSummary.split()])
       
    Recall = OverlapWords/len(RefSummary.split())
    Precision = OverlapWords/len(MSummary.split())
    
    Bleu = sentence_bleu([RefSummary.split()], MSummary.split(), weights=(1, 0, 0, 0))

    #F1 = 2 * (Bleu * Rouge) / (Bleu + Rouge)
    F1 = 2*(Precision*Recall/Precision+ Recall)
    
    print ('Bleu1 = ',Bleu)
    print ('R1_Recall = ',Recall)
    print ('R1_Precision = ',Precision)
    print ('F1 = ',F1)

#_______________________________________________________________
    
def Rouge2(MSummary, RefSummary):  
    #Text1 = 'the cat was found under the bed'
    #Text2 = 'the cat was under the bed'
    
    tokens1 = word_tokenize(MSummary)
    bigrms1 = nltk.bigrams(tokens1)
    bigrms1 = list(ngrams(tokens1,2))

    tokens2 = word_tokenize(RefSummary)
    bigrms2 = list(nltk.bigrams(tokens2))

    #print(*map(' '.join, bigrms1), sep=', ')
    #print(*map(' '.join, bigrms2), sep=', ')
            
    OverlapBigrams = len([val for val in list(bigrms1) if val in list(bigrms2)])
    
    Recall = OverlapBigrams/len(bigrms2)
    Precision = OverlapBigrams/len(bigrms1)
    
    Bleu = sentence_bleu([RefSummary.split()], MSummary.split(), weights=(0, 1, 0, 0))
    F2 = (1+pow(1,2))*(Precision*Recall/(pow(1,2)*Precision)+ Recall)

    print ('Bleu2 = ',Bleu)
    print ('R2_Recall = ',Recall)
    print ('R2_Precision = ',Precision)
    print ('F2 = ',F2)

#_______________________________________________________________

def Summary_Evaluation(MSummary,RefSummary,OriginalDoc):
    with open(MSummary, encoding="utf8") as f:
         Text1 = f.read()
         f.close()
         
    with open(RefSummary, encoding="utf8") as f:
         Text2 = f.read()
         f.close()
    
    with open(OriginalDoc, encoding="utf8") as f:
         Text3 = f.read()
         f.close()
         
    Rouge1(Text1, Text2)
    print ('_____________________________')
    Rouge2(Text1, Text2)
    print ('_____________________________')
    
    Total_words_summary = len(Text1.split())
    Total_words_original = len(Text3.split())
    Compressed_Rate = Total_words_summary / Total_words_original
    
    print ('Compressed Rate = ',Compressed_Rate)

#_______________________________________________________________

News_Articles = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/News Articles/business'
Summaries = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/Summaries/business'
Machine_Summary = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/Machine Summary/business'
 
#_______________________________________________________________

Summary_Evaluation(Machine_Summary+'/001.txt', Summaries+'/001.txt',News_Articles+'/001.txt')
