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

# cumulative BLEU scores
def BLEUSCORES():
    reference = [['this', 'is', 'small', 'test']]
    candidate = ['this', 'is', 'a', 'test']
    print('Cumulative 1-gram: %f' % sentence_bleu(reference, candidate, weights=(1, 0, 0, 0)))
    print('Cumulative 2-gram: %f' % sentence_bleu(reference, candidate, weights=(0.5, 0.5, 0, 0)))
    print('Cumulative 3-gram: %f' % sentence_bleu(reference, candidate, weights=(0.33, 0.33, 0.33, 0)))
    print('Cumulative 4-gram: %f' % sentence_bleu(reference, candidate, weights=(0.25, 0.25, 0.25, 0.25)))
#_______________________________________________________________

#https://rxnlp.com/how-rouge-works-for-evaluation-of-summarization-tasks/#.XCXw9MaxU5k
def Rouge(MSummary, RefSummary):
        
    with open(MSummary, encoding="utf8") as f:
         Text1 = f.read()
         f.close()
         
    with open(RefSummary, encoding="utf8") as f:
         Text2 = f.read()
         f.close()
    #Text1 = 'the cat was found under the bed'
    #Text2 = 'the cat was under the bed'
    OverlapWords = 0
    for w in Text1.split():
        if w in Text2.split():
           OverlapWords += 1
           
    Recall = OverlapWords/len(Text2.split())
    Precision = OverlapWords/len(Text1.split())
    
    #Bleu = sentence_bleu(Text2.split(), Text1.split(), weights=(1, 0, 0, 0))
    #F1 = 2 * (Bleu * Rouge) / (Bleu + Rouge)

    #print ('Bleu = ',Bleu)
    print ('R1_Recall = ',Recall)
    print ('R1_Precision = ',Precision)
    #print ('F1 = ',F1)

    
def Rouge2(MSummary, RefSummary):
    with open(MSummary, encoding="utf8") as f:
         Text1 = f.read()
         f.close()
         
    with open(RefSummary, encoding="utf8") as f:
         Text2 = f.read()
         f.close()
         
    #Text1 = 'the cat was found under the bed'
    #Text2 = 'the cat was under the bed'
    
    tokens1 = word_tokenize(Text1)
    bigrms1 = nltk.bigrams(tokens1)
    bigrms1 = list(ngrams(tokens1,2))

    tokens2 = word_tokenize(Text2)
    bigrms2 = list(nltk.bigrams(tokens2))

    #print(*map(' '.join, bigrms1), sep=', ')
    #print(*map(' '.join, bigrms2), sep=', ')
            
    OverlapBigrams = len([val for val in list(bigrms1) if val in list(bigrms2)])
    
    Recall = OverlapBigrams/len(bigrms2)
    Precision = OverlapBigrams/len(bigrms1)
     
    print ('R2_Recall = ',Recall)
    print ('R2_Precision = ',Precision)
#_______________________________________________________________
#https://rxnlp.com/how-rouge-works-for-evaluation-of-summarization-tasks/#.XCXw9MaxU5k
def Summary_Evaluation():
    Time_read_original = 1
    Time_read_summary = 1
    Time_saved = Time_read_original/Time_read_summary
    
    MainSentences = 1
    TotalSentencesSummarized = 1
    TotalSentences = 1
    
    Precision = MainSentences/TotalSentencesSummarized
    Recall = MainSentences/TotalSentences
    
    Bleu = 1
    Rouge = 1
    F1 = 2 * (Bleu * Rouge) / (Bleu + Rouge)
    
    Total_words_summary = 1
    Total_words_original = 1
    Compressed_Rate = Total_words_summary / Total_words_original

def Summary_Evaluation(MSummary,RSummary):
    overlapping_ngrams    
    MainSentences = 1
    TotalSentencesSummarized = 1
    TotalSentences = 1
    
    Precision = MainSentences/TotalSentencesSummarized
    Recall = MainSentences/TotalSentences
    
    Bleu = 1
    Rouge = 1
    F1 = 2 * (Bleu * Rouge) / (Bleu + Rouge)
    
    Total_words_summary = 1
    Total_words_original = 1
    Compressed_Rate = Total_words_summary / Total_words_original    
#_______________________________________________________________

News_Articles = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/News Articles'
Summaries = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/Summaries/business'
Machine_Summary = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/Machine Summary/business'

#MainSents = Summarize_Story(News_Articles+'/business/001.txt',10)
#with open(Machine_Summary+'/001.txt', "w") as output:
#     output.write("".join(MainSents))
     
#_______________________________________________________________

Rouge(Machine_Summary+'/001.txt', Summaries+'/001.txt')
Rouge2(Machine_Summary+'/001.txt', Summaries+'/001.txt')
