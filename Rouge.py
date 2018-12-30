#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 16:00:19 2018

@author: yazid Bounab
"""
from nltk.translate.bleu_score import sentence_bleu
from Summarization import Read_TextFile, Preprocessing_Text

# cumulative BLEU scores
def BLEUSCORES():
    reference = [['this', 'is', 'small', 'test']]
    candidate = ['this', 'is', 'a', 'test']
    print('Cumulative 1-gram: %f' % sentence_bleu(reference, candidate, weights=(1, 0, 0, 0)))
    print('Cumulative 2-gram: %f' % sentence_bleu(reference, candidate, weights=(0.5, 0.5, 0, 0)))
    print('Cumulative 3-gram: %f' % sentence_bleu(reference, candidate, weights=(0.33, 0.33, 0.33, 0)))
    print('Cumulative 4-gram: %f' % sentence_bleu(reference, candidate, weights=(0.25, 0.25, 0.25, 0.25)))

#https://rxnlp.com/how-rouge-works-for-evaluation-of-summarization-tasks/#.XCXw9MaxU5k
def Rouge2(MSummary, RefSummary):
    Text,punct = Read_TextFile(MSummary)
    Precessed_Text1 = Preprocessing_Text(Text,punct)
    
    Text,punct = Read_TextFile(RefSummary)
    Precessed_Text2 = Preprocessing_Text(Text,punct)
    
    print (Precessed_Text1)
    print (Precessed_Text2)

    OverlapBigrams = 1
    
Summaries = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/Summaries'
Machine_Summary = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/Machine Summary'

Rouge2(Machine_Summary+'/001.txt', Summaries+'/001.txt')
