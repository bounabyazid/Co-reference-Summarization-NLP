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
import json

from nltk.tree import Tree


from stanfordcorenlp import StanfordCoreNLP

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
    
def resolve(corenlp_output):
    """ Transfer the word form of the antecedent to its associated pronominal anaphor(s) """
    for coref in corenlp_output['corefs']:
        mentions = corenlp_output['corefs'][coref]
        antecedent = mentions[0]  # the antecedent is the first mention in the coreference chain
        for j in range(1, len(mentions)):
            mention = mentions[j]
            if mention['type'] == 'PRONOMINAL':
                # get the attributes of the target mention in the corresponding sentence
                target_sentence = mention['sentNum']
                target_token = mention['startIndex'] - 1
                # transfer the antecedent's word form to the appropriate token in the sentence
                corenlp_output['sentences'][target_sentence - 1]['tokens'][target_token]['word'] = antecedent['text']


def print_resolved(corenlp_output):
    """ Print the "resolved" output """
    possessives = ['hers', 'his', 'their', 'theirs']
    for sentence in corenlp_output['sentences']:
        for token in sentence['tokens']:
            output_word = token['word']
            # check lemmas as well as tags for possessive pronouns in case of tagging errors
            if token['lemma'] in possessives or token['pos'] == 'PRP$':
                output_word += "'s"  # add the possessive morpheme
            output_word += token['after']
            print(output_word, end='')


text = "Tom and Jane are good friends. They are cool. He knows a lot of things and so does she. His car is red, but " \
       "hers is blue. It is older than hers. The big cat ate its dinner."
       
text0 = 'Barack Obama was born in Hawaii.  He is the president. Obama was elected in 2008.'

text2 = "The music was so loud that it couldn\'t be enjoyed." \
       "Our neighbors dislike the music. If they are angry, the cops will show up soon." \
       "If they are angry about the music, the neighbors will call the cops." \
       "Despite heri difficulty, Wilmai came to understand the point."
       
nlp = StanfordCoreNLP('/home/polo/Downloads/stanford-corenlp-full-2018-10-05/', quiet=False)
props = {'annotators': 'dcoref', 'pipelineLanguage': 'en'}

output = json.loads(nlp.annotate(text, properties=props))       
#output = nlp.annotate(text, properties= {'annotators':'dcoref','outputFormat':'json','ner.useSUTime':'false'})

resolve(output)

print('Original:', text)
print('_________________________________________')
print('Resolved: ', end='')
print_resolved(output)
nlp.close() 
#draw()
