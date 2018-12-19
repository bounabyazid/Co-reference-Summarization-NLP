#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 11:40:03 2018

@author: Yazid Bounab
"""
#https://github.com/jawahar273/SRLTagger
#http://sag.art.uniroma2.it/Babel/babel.jsp
#http://sag.art.uniroma2.it/demo-software/babel/

from nltk.tokenize import word_tokenize

from srlnltk import SennaSRLTagger 
from nltk.tag import SennaTagger
from nltk.tag import StanfordNERTagger

sent = 'Shakespeare theatre was in London .'
text = 'Turing was born in Maida Vale, London, while Turing\'s father, Julius Mathison Turing -LRB-1873--1947-RRB-, was on leave from his father\'s position with the Indian Civil Service -LRB-ICS-RRB- at Chatrapur'

sents = """He killed the man with a knife and murdered him with a dagger.""".split()
sents1 = 'The police officer detained the suspect at the scene of the crime.'.split()
path = '/home/polo/Downloads/senna-v3.0/senna'

from nltk.tag import SennaChunkTagger
from nltk.tag import SennaNERTagger

def NE_Tagger(text):
    st = StanfordNERTagger('/home/polo/Downloads/stanford-ner-2018-02-27/classifiers/english.all.3class.distsim.crf.ser.gz',
					       '/home/polo/Downloads/stanford-ner-2018-02-27/stanford-ner.jar', encoding='utf-8')
    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)
    print(classified_text)
    return classified_text

def SRL_Event_Structure(labels):
    EventStructures = {'Who':'','What':'','Whom':'','When':'','Where':''}
    Args = []
    text = ''
    for label in labels:
        if 'B-' in label[1][2]:
             Args.append(text)
             text = label[1][0]
        elif label[1][2] != 'O':
            text += ' '+label[1][0]
        #for item in label[1]:
        #    print (type(item))
    return Args
      
srltagger = SennaSRLTagger(path)
nertagger = SennaNERTagger(path)
chktagger = SennaChunkTagger(path)
tagger = SennaTagger(path)

#w = s.tag("Are you studying here?".split())
#w = s.tag("""A general interface to the SENNA pipeline that supports any of the operations specified in SUPPORTED OPERATIONS..""".split()) 

#print(tagger.tag(sents))
#print('\n___________________\n')
#print(chktagger.tag(sents))
#print('\n___________________\n')
#print(nertagger.tag(sents))
#print('\n___________________\n')
print(srltagger.tag(sents))
print('\n___________________\n')

NE_Tagger(text)
#print('\n'.join(str(e) for e in NE_Tagger(sents)))

print('\n___________________\n')

labels = srltagger.tag(text.split())
print ('\n'.join(map(str, labels)))
print('\n___________________\n')

print ('\n'.join(map(str, SRL_Event_Structure(labels))))

#tokens = word_tokenize(sents)
#SennaSRLTagger.tag2file(tokens,file_name='testing_file.txt', file_mode='w')

#s.tag2file("""A general interface to the SENNA pipeline that supports any of the operations specified in SUPPORTED OPERATIONS..""".split())
