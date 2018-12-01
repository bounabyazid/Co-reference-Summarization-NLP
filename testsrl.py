#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 11:40:03 2018

@author: polo
"""
#https://github.com/jawahar273/SRLTagger

from srlnltk import SennaSRLTagger 
from nltk.tag import SennaTagger

sents = """He killed the man with a knife and murdered him with a dagger.""".split()
sents = 'The police officer detained the suspect at the scene of the crime.'.split()
path = '/home/polo/Downloads/senna-v3.0/senna'

from nltk.tag import SennaChunkTagger
from nltk.tag import SennaNERTagger

srltagger = SennaSRLTagger(path)
nertagger = SennaNERTagger(path)
chktagger = SennaChunkTagger(path)
tagger = SennaTagger(path)

#w = s.tag("Are you studying here?".split())
#w = s.tag("""A general interface to the SENNA pipeline that supports any of the operations specified in SUPPORTED OPERATIONS..""".split()) 

print(tagger.tag(sents))
print('\n___________________\n')
print(chktagger.tag(sents))
print('\n___________________\n')
print(nertagger.tag(sents))
print('\n___________________\n')
print(srltagger.tag(sents))

#s.tag2file("""A general interface to the SENNA pipeline that supports any of the operations specified in SUPPORTED OPERATIONS..""".split())