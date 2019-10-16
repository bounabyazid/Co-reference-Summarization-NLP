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

sent = 'Shakespeare theatre was in London to make theature.'
text = 'Turing was born in Maida Vale, London, while Turing\'s father, Julius Mathison Turing -LRB-1873--1947-RRB-, was on leave from his father\'s position with the Indian Civil Service -LRB-ICS-RRB- at Chatrapur'

sents = """He killed the man with a knife and murdered him with a dagger.""".split()
sents1 = 'The police officer detained the suspect at the scene of the crime.'.split()
path = '/home/polo/Downloads/senna-v3.0/senna'

text = 'John and Carol mopped the floor with the dress Mary bought while studying and traveling in Thailand'
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
    #AM : Argument Modifier
    EventStructures = {'Who':'','What':'','Whom':'','When':'','Where':'','How':''}
    Args = []
    text = ''
    arg = ''
    for i in range(0,len(labels)-1):
        if labels[i][1][2].startswith('B-'):
           if 'B-V' == labels[i][1][2]:
                EventStructures['What'] = labels[i][1][1]
           else:
                arg =  labels[i][1][2][2:]
                if 'A1' == arg:
                  EventStructures['Who'] = text
                elif 'A2' == arg:
                    EventStructures['Whom'] = text
                text = labels[i][1][0]
                Args.append(text)
        else:
            text += ' '+labels[i][1][0]
       
    print (EventStructures)
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
#print(srltagger.tag(sents))
#print('\n___________________\n')
#text = sent
NE_Tagger(text)
#print('\n'.join(str(e) for e in NE_Tagger(sents)))

print('\n___________________\n')

labels = srltagger.tag(text.split())
print ('\n'.join(map(str, labels)))
print('\n___________________\n')

print ('\n'.join(map(str, SRL_Event_Structure(labels))))
#srltagger.tag2file(text.split(),file_name='testing_file.txt', file_mode='w')

#tokens = word_tokenize(sents)
#SennaSRLTagger.tag2file(tokens,file_name='testing_file.txt', file_mode='w')

#s.tag2file("""A general interface to the SENNA pipeline that supports any of the operations specified in SUPPORTED OPERATIONS..""".split())