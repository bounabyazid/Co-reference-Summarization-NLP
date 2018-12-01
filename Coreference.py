#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 15:54:22 2018

@author: Yazid Bounab
"""
#https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
#https://www.tutorialspoint.com/python/python_remove_stopwords.htm
#https://pythonspot.com/nltk-stop-words/

import re
import nltk
import nlpnet
import string
import json

from nltk.tree import Tree

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer

from stanfordcorenlp import StanfordCoreNLP

from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
#_______________________________________________________________

def Read_Text():
    with open('Alan Turing.txt') as f:
         text = f.read()
    sentences = sent_tokenize(text)
    print (len(sentences))
    #print (sentences)
    return sentences
#_______________________________________________________________

def Preprocessing(sentence):
    #sentence = sentence.lower()
    sentence = re.sub('[0-9]+', '', sentence)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(sentence)
    stop_words = set(stopwords.words('english')) 
    words = [w for w in tokens if not w in stop_words]
    return words

def Tokenize_Sentences(sentences):
    Tokenized_Sentences = []
    for sent in sentences:
        Tokenized_Sentences.append(Preprocessing(sent))
    print (Tokenized_Sentences)
    return Tokenized_Sentences
#_______________________________________________________________

def draw():
    #https://stackoverflow.com/questions/31936026/drawing-a-flatten-nltk-parse-tree-with-np-chunks?rq=1
    sentence = [("the", "DT"), ("little", "JJ"), ("yellow", "JJ"), ("dog", "NN"), ("barked","VBD"), ("at", "IN"), ("the", "DT"), ("cat", "NN")]
    #sentence = 'Barack Obama was born in Hawaii.  He is the president. Obama was elected in 2008.'
    #sentence = list(map(lambda sent: Tree(sent[1], children=[sent[0]]), sentence))
    pattern = """NP: {<DT>?<JJ>*<NN>}
                VBD: {<VBD>}
                IN: {<IN>}"""
                
    NPChunker = nltk.RegexpParser(pattern) 
    result = NPChunker.parse(sentence)
    result.draw()
#_______________________________________________________________

def Parse_Draw(text):
    try:
        words = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(words)
        
        chunkGram = r"""Chunk: {<.*>+}
                                    }<VB.?|IN|DT|TO>+{"""

        chunkParser = nltk.RegexpParser(chunkGram)
        chunked = chunkParser.parse(tagged)

        chunked.draw()

    except Exception as e:
        print(str(e))
#_______________________________________________________________

def NE_Tagger(text):
    st = StanfordNERTagger('/home/polo/Downloads/stanford-ner-2018-02-27/classifiers/english.all.3class.distsim.crf.ser.gz',
					       '/home/polo/Downloads/stanford-ner-2018-02-27/stanford-ner.jar', encoding='utf-8')

    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)

    print(classified_text)
    return classified_text
#_______________________________________________________________
    
def NE_Sentences(sentences):
    TagSent = open('TagSentences','w') 
    i = 0
    for sent in sentences:
        print(sent)
        TagSent.write('Sentence '+str(i)+':\n')
        TagSent.write('===========\n')
        TagSent.write(sent)
        TagSent.write('\n.......................................\n')
        TagSent.write(','.join(str(e) for e in NE_Tagger(sent)))
        TagSent.write('\n_______________________________________\n')

        print('__________________________')
        i += 1
    TagSent.close()
#_______________________________________________________________
    
def Coreference(text):
    nlp = StanfordCoreNLP('/home/polo/Downloads/stanford-corenlp-full-2018-10-05/', quiet=False)
    props = {'annotators': 'dcoref', 'pipelineLanguage': 'en'}

    result = json.loads(nlp.annotate(text, properties=props))
    #print(result['corefs'].items())
    
    for key, value in result['corefs'].items():
        print ('=================================')
        print ('_______________Key_______________')
        print (key)
        print ('______________Value______________')
        for val in value:
            print (val)
            print ('$$$$$$$$$$$$$$$$$$$$')
            print (val['text'])
            print ('.....................')


    
    #num, mentions = result['corefs'].items()[0]
    #for mention in mentions:
    #    print(mention)
    nlp.close()
#_______________________________________________________________
    
def SRL(text):
    tagger = nlpnet.SRLTagger()
    print(tagger.tag(text))
#_______________________________________________________________
    
#sentences = Read_Text()
#NE_Sentences(sentences)

#Tokenized_Sentences = Tokenize_Sentences(sentences)

#with open('Alan Turing.txt') as f:
#     text = f.read()
#Coreference(text)
    
#draw()
text = 'Barack Obama was born in Hawaii.  He is the president. Obama was elected in 2008.'
#text = 'Turing was born in Maida Vale, London, while his father, Julius Mathison Turing (1873–1947), was on leave from his position with the Indian Civil Service (ICS) at Chatrapur'
#Parse_Draw(text)
#Coreference(text)

SRL(text)