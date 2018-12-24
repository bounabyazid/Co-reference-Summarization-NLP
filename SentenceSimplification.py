# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 19:46:49 2018

@author: Yazid Bounab
"""
import re
import nltk
import nlpnet
import string
import json
from nltk import RegexpParser
from nltk.tree import Tree

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize, pos_tag, ne_chunk
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

# Defining a grammar & Parser
NP = "NP: {(<V\w+>|<NN\w?>)+.*<NN\w?>}"
RC = "RC: {(who|whom|which|whosethat)<VBD>}"
RC = "RC: {<WP><VBD>}"

VB = "VB:{<VB.*><DT><NN.*>}"
pattern = """NP: {<DT>?<JJ>*<NN>}
                VBD: {<VBD>}
                IN: {<IN>}
                RC : {<S><NP> <VP>}
                ADVC : {\w+ly}
                
                """
#https://towardsdatascience.com/a-practitioners-guide-to-natural-language-processing-part-i-processing-understanding-text-9f4abfd13e72                
pattern = """NP: {<DT>?<JJ>*<NN>}
             VP: {<VB.*><DT><NN.*>}
             ADJP : {}
             ADVP : {<RB.*><VB.*|JJ.*|NN.*>}
             PP : {}
             """
                
chunker = RegexpParser(NP)

def get_continuous_chunks(text, chunk_func=ne_chunk):
    chunked = chunk_func(pos_tag(word_tokenize(text)))
    continuous_chunk = []
    current_chunk = []

    for subtree in chunked:
        #print(subtree)
        if type(subtree) == Tree:
            current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue

    return continuous_chunk

def Relative_Clause(sentence):
    #words = nltk.word_tokenize(sentence)
    #tagged = nltk.pos_tag(words)
    print('\n'.join(str(e) for e in nltk.pos_tag(nltk.word_tokenize(sentence))))
    return False
    
def Restrictive_Clause():
    return False
    
def Nonrestrictive_Clause():
    return False

def Reduced_Relative_Clauses():
    return False

def Simplified_Sentence(Sentence):
    Simple_Sent = ''
    #_____________________parentheticals________________________
    if Sentence.find('(') != -1 and Sentence.find(')') != -1:
       t = Sentence[Sentence.find('('):Sentence.find(')')+1]  # maintenant t pointe vers la nouvelle chaîne &#39;ll&#39;
       Sentence = Sentence.replace(t,'')
       #print(Sentence.replace(t,''))
    Relative_Clause(Sentence)
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
        print (Sentence)
        #Simple_Sents.append(Simplified_Sentence(Sentence))
    return Simple_Sents
#_______________________________________________________________
    
#Sentences = Read_Text()
#Simplified_Sentences(Sentences)

#Sentence = 'He signed the reauthorization of the State Children’s Health Insurance Program (SCHIP).'
Sentence = 'The article that I read was important for my literature review.'
Sentence1 = 'The participants who were interviewed volunteered to be part of the study.'
#Simplified_Sentence(Sentence1)

print(get_continuous_chunks(Sentence1, chunk_func=ne_chunk))
