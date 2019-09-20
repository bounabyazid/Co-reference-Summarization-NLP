#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 16:00:19 2018

@author: Yazid Bounab
"""
import os
from os import listdir
from os.path import isfile, join

import nltk
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from nltk.translate.bleu_score import sentence_bleu
from Summarization import Summarize_Story

#_______________________________________________________________

#https://rxnlp.com/how-rouge-works-for-evaluation-of-summarization-tasks/#.XCXw9MaxU5k
#https://machinelearningmastery.com/calculate-bleu-score-for-text-python/

def Rouge_N(N,MSummary, RefSummary):
    tokens1 = word_tokenize(MSummary)
    Ngrams1 = list(ngrams(tokens1,N))

    tokens2 = word_tokenize(RefSummary)
    Ngrams2 = list(ngrams(tokens2,N))
    
    Bleu = 0
    Recall = 0
    Precision = 0
    F = 0
      
    OverlapNgram = len([Ngram for Ngram in Ngrams1 if Ngram in Ngrams2])
       
    Recall = round(OverlapNgram/len(Ngrams2),2)
    Precision = round(OverlapNgram/len(Ngrams1),2)
    
    if OverlapNgram != 0:
       F = round((1+pow(N,2))*(Precision*Recall/(pow(N,2)*Precision)+ Recall),2)

    weights = [0] * 4
    weights[N-1] = 1
    weights = tuple(weights)
    #print (weights)
    Bleu = round(sentence_bleu([RefSummary.split()], MSummary.split(), weights),2)
    #Bleu = sentence_bleu([RefSummary.split()], MSummary.split())
    
    #print ('Bleu'+str(N)+' = ',Bleu)
    #print ('R'+str(N)+'_Recall = ',Recall)
    #print ('R'+str(N)+'_Precision = ',Precision)
    #print ('F'+str(N)+' = ',F)
    
    return Bleu,Recall,Precision,F

#_______________________________________________________________

def Rouge1(MSummary, RefSummary):
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
    
    return Bleu,Recall,Precision,F1


#_______________________________________________________________
    
def Rouge2(MSummary, RefSummary):  
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
    F2 = (1+pow(2,2))*(Precision*Recall/(pow(2,2)*Precision)+ Recall)

    print ('Bleu2 = ',Bleu)
    print ('R2_Recall = ',Recall)
    print ('R2_Precision = ',Precision)
    print ('F2 = ',F2)
    
    return Bleu,Recall,Precision,F2

#_______________________________________________________________

def Summary_Evaluation(MSummary,RefSummary,OriginalDoc):
    with open(MSummary, encoding="ISO-8859-1") as f:
         Text1 = f.read()
         f.close()
         
    with open(RefSummary, encoding="ISO-8859-1") as f:
         Text2 = f.read()
         f.close()
    
    with open(OriginalDoc, encoding="ISO-8859-1") as f:
         Text3 = f.read()
         f.close()
         
    Bleu1 = 0
    Recall1 = 0
    Precision1 = 0
    F1= 0
    
    Bleu2 = 0
    Recall2 = 0
    Precision2 = 0
    F2 = 0
    Compressed_Rate = 0
    
    if Text1: 
       #Bleu1,Recall1,Precision1,F1 = Rouge1(Text1, Text2)
       #print ('.............................')
       Bleu1,Recall1,Precision1,F1 = Rouge_N(1,Text1, Text2)
       #print ('_____________________________')
    
       #Bleu2,Recall2,Precision2,F2 = Rouge2(Text1, Text2)
       #print ('.............................')
       Bleu2,Recall2,Precision2,F2 = Rouge_N(2,Text1, Text2)
       #print ('_____________________________')
    
       Total_words_summary = len(Text1.split())
       Total_words_original = len(Text3.split())
       Compressed_Rate = round(Total_words_summary / Total_words_original,2)
    
        #print ('Compressed Rate = ',Compressed_Rate)
    
    return Bleu1,Recall1,Precision1,F1,Bleu2,Recall2,Precision2,F2,Compressed_Rate

#_______________________________________________________________
    
def Evaluate_BBC_News_Summary():
    News_Articles = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/News Articles'
    Summaries = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/Summaries'
    Machine_Summary = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/Machine Summary'
    Evaluation_Summary = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/Evaluation Summary'

    #Summary_Evaluation(Machine_Summary+'/001.txt', Summaries+'/001.txt',News_Articles+'/001.txt')
    SubDirectories = os.listdir(News_Articles)

    try:  
        os.mkdir(Evaluation_Summary)
    except OSError:  
                print ("Creation of the directory %s failed" % Evaluation_Summary)
                
    for subdir in SubDirectories:
        try:  
            os.mkdir(Evaluation_Summary+'/'+subdir)
        except OSError:  
                print ("Creation of the directory %s failed" % subdir)
    
       
    for subdir in SubDirectories:
        FBleu1 = open(Evaluation_Summary+'/'+subdir+'/'+"Bleu1.csv","w+")
        FRecall1 = open(Evaluation_Summary+'/'+subdir+'/'+"Recall1.csv","w+")
        FPrecision1 = open(Evaluation_Summary+'/'+subdir+'/'+"Precision1.csv","w+")
        FF1 = open(Evaluation_Summary+'/'+subdir+'/'+"F1.csv","w+")
    
        FBleu2 = open(Evaluation_Summary+'/'+subdir+'/'+"Bleu2.csv","w+")
        FRecall2 = open(Evaluation_Summary+'/'+subdir+'/'+"Recall2.csv","w+")
        FPrecision2= open(Evaluation_Summary+'/'+subdir+'/'+"Precision2.csv","w+")
        FF2 = open(Evaluation_Summary+'/'+subdir+'/'+"F2.csv","w+")
    
        FComp_Rate = open(Evaluation_Summary+'/'+subdir+'/'+"Compressed_Rate.csv","w+")

        files = [f for f in listdir(News_Articles+'/'+subdir) if isfile(join(News_Articles+'/'+subdir, f))]    
        
        Bleus1 = []
        Recalls1 = []
        Precisions1 = []
        Fs1 = []
        Bleus2 = []
        Recalls2 = []
        Precisions2 = []
        Fs2 = []
        Compr_Rates = []
        
        for f in files:
            print(News_Articles+'/'+subdir+'/'+f)

            Bleu1,Recall1,Precision1,F1,Bleu2,Recall2,Precision2,F2,Compressed_Rate = Summary_Evaluation(Machine_Summary+'/'+subdir+'/'+f, Summaries+'/'+subdir+'/'+f,News_Articles+'/'+subdir+'/'+f)
           
            Bleus1.append(Bleu1)
            Recalls1.append(Recall1)
            Precisions1.append(Precision1)
            Fs1.append(F1)
            Bleus2.append(Bleu2)
            Recalls2.append(Recall2)
            Precisions2.append(Precision2)
            Fs2.append(F2)
            Compr_Rates.append(Compressed_Rate)
            
            #__________________________________________________________________
            f = f.replace('.txt','')
            FBleu1.write(f+','+str(Bleu1)+'\n')
            FRecall1.write(f+','+str(Recall1)+'\n')
            FPrecision1.write(f+','+str(Precision1)+'\n')
            FF1.write(f+','+str(F1)+'\n')
            
            FBleu2.write(f+','+str(Bleu2)+'\n')
            FRecall2.write(f+','+str(Recall2)+'\n')
            FPrecision2.write(f+','+str(Precision2)+'\n')
            FF2.write(f+','+str(F2)+'\n')
            
            FComp_Rate.write(f+','+str(Compressed_Rate)+'\n')
            
        FBleu1.close()
        FRecall1.close()
        FPrecision1.close()
        FF1.close()
    
        FBleu2.close()
        FRecall2.close()
        FPrecision2.close()
        FF2.close()
    
        FComp_Rate.close()
        
        Statistics = open(Evaluation_Summary+'/'+subdir+'/'+'Statistics '+subdir+'.csv',"w+")

        Statistics.write('Metrics,Min,Max,Avg\n')
        Statistics.write('Bleu1,'+str(min(Bleus1))+','+str(max(Bleus1))+','+str(round(sum(Bleus1) / float(len(Bleus1)),2))+'\n')
        Statistics.write('Recall1,'+str(min(Recalls1))+','+str(max(Recalls1))+','+str(round(sum(Recalls1) / float(len(Recalls1)),2))+'\n')
        Statistics.write('Precision1,'+str(min(Precisions1))+','+str(max(Precisions1))+','+str(round(sum(Precisions1) / float(len(Precisions1)),2))+'\n')
        Statistics.write('F1,'+str(min(Fs1))+','+str(max(Fs1))+','+str(round(sum(Fs1) / float(len(Fs1)),2))+'\n')

        Statistics.write('Bleu2,'+str(min(Bleus2))+','+str(max(Bleus2))+','+str(round(sum(Bleus2) / float(len(Bleus2)),2))+'\n')
        Statistics.write('Recall2,'+str(min(Recalls2))+','+str(max(Recalls2))+','+str(round(sum(Recalls2) / float(len(Recalls2)),2))+'\n')
        Statistics.write('Precision2,'+str(min(Precisions2))+','+str(max(Precisions2))+','+str(round(sum(Precisions2) / float(len(Precisions2)),2))+'\n')
        Statistics.write('F2,'+str(min(Fs1))+','+str(max(Fs2))+','+str(round(sum(Fs2) / float(len(Fs2)),2))+'\n')

        Statistics.write('Compressed Rate,'+str(min(Compr_Rates))+','+str(max(Compr_Rates))+','+str(round(sum(Compr_Rates) / float(len(Compr_Rates)),2))+'\n')

        Statistics.close()
#_______________________________________________________________

def Evaluate_StoryTelling_Summary():
    Stories = '/home/polo/.config/spyder-py3/Co-referece/Fairy tales/Storynory'
    Machine_Summary = '/home/polo/.config/spyder-py3/Co-referece/Fairy tales/Machine Summary'
  
    Summaries = '/home/polo/.config/spyder-py3/Co-referece/Fairy tales/Summaries'
    Evaluation_Summary = '/home/polo/.config/spyder-py3/Co-referece/Fairy tales/Evaluation Summary'

    #Summary_Evaluation(Machine_Summary+'/001.txt', Summaries+'/001.txt',News_Articles+'/001.txt')
    SubDirectories = os.listdir(Stories)

    try:  
        os.mkdir(Evaluation_Summary)
    except OSError:  
                print ("Creation of the directory %s failed" % Evaluation_Summary)
                
    for subdir in SubDirectories:
        try:  
            os.mkdir(Evaluation_Summary+'/'+subdir)
        except OSError:  
                print ("Creation of the directory %s failed" % subdir)
    
       
    for subdir in SubDirectories:
        FBleu1 = open(Evaluation_Summary+'/'+subdir+'/'+"Bleu1.csv","w+")
        FRecall1 = open(Evaluation_Summary+'/'+subdir+'/'+"Recall1.csv","w+")
        FPrecision1 = open(Evaluation_Summary+'/'+subdir+'/'+"Precision1.csv","w+")
        FF1 = open(Evaluation_Summary+'/'+subdir+'/'+"F1.csv","w+")
    
        FBleu2 = open(Evaluation_Summary+'/'+subdir+'/'+"Bleu2.csv","w+")
        FRecall2 = open(Evaluation_Summary+'/'+subdir+'/'+"Recall2.csv","w+")
        FPrecision2= open(Evaluation_Summary+'/'+subdir+'/'+"Precision2.csv","w+")
        FF2 = open(Evaluation_Summary+'/'+subdir+'/'+"F2.csv","w+")
    
        FComp_Rate = open(Evaluation_Summary+'/'+subdir+'/'+"Compressed_Rate.csv","w+")

        files = [f for f in listdir(Stories+'/'+subdir) if isfile(join(Stories+'/'+subdir, f))]    
        
        Bleus1 = []
        Recalls1 = []
        Precisions1 = []
        Fs1 = []
        Bleus2 = []
        Recalls2 = []
        Precisions2 = []
        Fs2 = []
        Compr_Rates = []
        
        for f in files:
            print(Stories+'/'+subdir+'/'+f)

            Bleu1,Recall1,Precision1,F1,Bleu2,Recall2,Precision2,F2,Compressed_Rate = Summary_Evaluation(Machine_Summary+'/'+subdir+'/'+f, Summaries+'/'+subdir+'/'+f,Stories+'/'+subdir+'/'+f)
           
            Bleus1.append(Bleu1)
            Recalls1.append(Recall1)
            Precisions1.append(Precision1)
            Fs1.append(F1)
            Bleus2.append(Bleu2)
            Recalls2.append(Recall2)
            Precisions2.append(Precision2)
            Fs2.append(F2)
            Compr_Rates.append(Compressed_Rate)
            
            #__________________________________________________________________
            f = f.replace('.txt','')
            FBleu1.write(f+','+str(Bleu1)+'\n')
            FRecall1.write(f+','+str(Recall1)+'\n')
            FPrecision1.write(f+','+str(Precision1)+'\n')
            FF1.write(f+','+str(F1)+'\n')
            
            FBleu2.write(f+','+str(Bleu2)+'\n')
            FRecall2.write(f+','+str(Recall2)+'\n')
            FPrecision2.write(f+','+str(Precision2)+'\n')
            FF2.write(f+','+str(F2)+'\n')
            
            FComp_Rate.write(f+','+str(Compressed_Rate)+'\n')
            
        FBleu1.close()
        FRecall1.close()
        FPrecision1.close()
        FF1.close()
    
        FBleu2.close()
        FRecall2.close()
        FPrecision2.close()
        FF2.close()
    
        FComp_Rate.close()
        
        Statistics = open(Evaluation_Summary+'/'+subdir+'/'+'Statistics '+subdir+'.csv',"w+")

        Statistics.write('Metrics,Min,Max,Avg\n')
        Statistics.write('Bleu1,'+str(min(Bleus1))+','+str(max(Bleus1))+','+str(round(sum(Bleus1) / float(len(Bleus1)),2))+'\n')
        Statistics.write('Recall1,'+str(min(Recalls1))+','+str(max(Recalls1))+','+str(round(sum(Recalls1) / float(len(Recalls1)),2))+'\n')
        Statistics.write('Precision1,'+str(min(Precisions1))+','+str(max(Precisions1))+','+str(round(sum(Precisions1) / float(len(Precisions1)),2))+'\n')
        Statistics.write('F1,'+str(min(Fs1))+','+str(max(Fs1))+','+str(round(sum(Fs1) / float(len(Fs1)),2))+'\n')

        Statistics.write('Bleu2,'+str(min(Bleus2))+','+str(max(Bleus2))+','+str(round(sum(Bleus2) / float(len(Bleus2)),2))+'\n')
        Statistics.write('Recall2,'+str(min(Recalls2))+','+str(max(Recalls2))+','+str(round(sum(Recalls2) / float(len(Recalls2)),2))+'\n')
        Statistics.write('Precision2,'+str(min(Precisions2))+','+str(max(Precisions2))+','+str(round(sum(Precisions2) / float(len(Precisions2)),2))+'\n')
        Statistics.write('F2,'+str(min(Fs1))+','+str(max(Fs2))+','+str(round(sum(Fs2) / float(len(Fs2)),2))+'\n')

        Statistics.write('Compressed Rate,'+str(min(Compr_Rates))+','+str(max(Compr_Rates))+','+str(round(sum(Compr_Rates) / float(len(Compr_Rates)),2))+'\n')

        Statistics.close()

#_______________________________________________________________
        
#Evaluate_BBC_News_Summary()
Evaluate_StoryTelling_Summary()