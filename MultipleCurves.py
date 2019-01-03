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

def DrawSubDir():
    Evaluation_Summary = '/home/polo/.config/spyder-py3/Co-referece/BBC News Summary/Evaluation Summary/business/'
    SubDirectories = os.listdir(Evaluation_Summary)
    colors = ['red','green','blue','orange','pink','brown','black','Aqua','yellow','Bright green']
    i = 0
    print (SubDirectories)
    df = pd.read_csv(Evaluation_Summary+'Bleu2.csv',names=['x','y'], delimiter=',')
    plt.plot(df['x'].tolist(), df['y'].tolist(), color=colors[i], label='Bleu2.csv')

    #for SubDir in SubDirectories:
    #    df = pd.read_csv(Evaluation_Summary+SubDir,names=['x','y'], delimiter=',')
    #    plt.plot(df['x'].tolist(), df['y'].tolist(), color=colors[i], label=SubDir)
    #    i += 1
    #    break
        
    plt.title('business')
    plt.ylabel('Metrics')
    plt.xlabel('Files')
    plt.legend()
    plt.show()
    
DrawSubDir()
