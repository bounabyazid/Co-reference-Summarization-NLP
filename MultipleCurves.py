#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 17:05:41 2019

@author: Yazid Bounab
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def LoadMetrics(SubDir):
    B1 = pd.read_csv(SubDir+'/Bleu1.csv',names=['x','y'], delimiter=',')
    P1 = pd.read_csv(SubDir+'/Precision1.csv',names=['x','y'], delimiter=',')
    R1 = pd.read_csv(SubDir+'/Recall1.csv',names=['x','y'], delimiter=',')
    F1 = pd.read_csv(SubDir+'/F1.csv',names=['x','y'], delimiter=',')
    
    B2 = pd.read_csv(SubDir+'/Bleu2.csv',names=['x','y'], delimiter=',')
    P2 = pd.read_csv(SubDir+'/Precision2.csv',names=['x','y'], delimiter=',')
    R2 = pd.read_csv(SubDir+'/Recall2.csv',names=['x','y'], delimiter=',')
    F2 = pd.read_csv(SubDir+'/F2.csv',names=['x','y'], delimiter=',')
    
    CR = pd.read_csv(SubDir+'/Compressed_Rate.csv',names=['x','y'], delimiter=',')

    return B1,P1,R1,F1,B2,P2,R2,F2,CR

def PlotMesure(Evaluation_Summary,SubDir,Type,Metric,x,y,colors):
    if Type == 'Double':
       df = pd.DataFrame({'x': x,'y':y})
       df = df.sort_values(df.columns[0], ascending = True)
       plt.plot(list(range(len(x))), df['y'].tolist(), color=colors[0], label=Metric+'2')
       plt.plot(list(range(len(x))), df['x'].tolist(), color=colors[2], label=Metric+'1')
    if Type == 'Single':
        plt.plot(x, y, color=colors[1], label=Metric)
 
    plt.title(SubDir)
    plt.xlabel('files')
    plt.ylabel('Values')

    plt.legend()
    #plt.show()
    plt.savefig(Evaluation_Summary+SubDir+'/'+SubDir+' '+Metric+'.png')
    plt.cla()
    
def PlotSubDir():
    Evaluation_Summary = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/Evaluation Summary/'
    colors = ['red','green','blue','orange','pink','brown','black','Aqua','yellow','Bright green']

    SubDirectories = os.listdir(Evaluation_Summary)
    
    for SubDir in SubDirectories:
        B1,P1,R1,F1,B2,P2,R2,F2,CR = LoadMetrics(Evaluation_Summary+SubDir)
   
        List5 = CR.sort_values(CR.columns[1], ascending = True)['y']
    
        df = pd.DataFrame({'Precision1': P1['y'].values,'Recall1':R1['y'].values})
        df = df.sort_values(df.columns[0], ascending = True)
        #plt.plot(df['Precision1'].tolist(), df['Recall1'].tolist(), color=colors[1], label='Rouge1')
   
        df = pd.DataFrame({'F1': P1['y'].values,'F2':R1['y'].values})
        df = df.sort_values(df.columns[0], ascending = True)
        PlotMesure(Evaluation_Summary, SubDir, 'Double', 'F', df['F1'].tolist(), df['F2'].tolist(), colors)

        df = pd.DataFrame({'B1': B1['y'].values,'B2':B2['y'].values})
        df = df.sort_values(df.columns[0], ascending = True)
        PlotMesure(Evaluation_Summary, SubDir, 'Double', 'Bleu', df['B1'].tolist(), df['B2'].tolist(), colors)
          
        PlotMesure(Evaluation_Summary, SubDir, 'Single', 'Compressed Rate', list(range(len(List5))), List5, colors)
    
PlotSubDir()
