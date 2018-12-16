#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 23:18:51 2018

@author: polo
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 15:54:22 2018

@author: Yazid Bounab
"""
#https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
#https://www.tutorialspoint.com/python/python_remove_stopwords.htm
#https://pythonspot.com/nltk-stop-words/

import nltk
import json

from nltk.tree import Tree
from stanfordcorenlp import StanfordCoreNLP

from nltk import word_tokenize, pos_tag, ne_chunk
from nltk import RegexpParser
import pandas as pd

#Anaphora
#________
Ana1 = 'The music was so loud that it couldn\'t be enjoyed.'
#The anaphor it follows the expression to which it refers (its antecedent)
Ana2 = 'Our neighbors dislike the music. If they are angry, the cops will show up soon.'
#The anaphor they follows the expression to which it refers (its antecedent).

#Cataphora
#_________
Cata1 = 'If they are angry about the music, the neighbors will call the cops.'
# The cataphor they precedes the expression to which it refers (its postcedent).
Cata2 = 'Despite her difficulty, Wilma came to understand the point.'
# The cataphor her precedes the expression to which it refers (its postcedent)

#Split antecedents
#_________________
SAnt1 = 'Carol told Bob to attend the party. They arrived together.'
# The anaphor they has a split antecedent, referring to both Carol and Bob.
SAnt2 = 'When Carol helps Bob and Bob helps Carol, they can accomplish any task.'
# The anaphor they has a split antecedent, referring to both Carol and Bob.

#Coreferring noun phrases
#________________________
CorNP1 = 'The project leader is refusing to help. The jerk thinks only of himself.'
# Coreferring noun phrases, whereby the second noun phrase is a predication over the first.
CorNP2 = 'Some of our colleagues are going to be supportive. These kinds of people will earn our gratitude'
# Coreferring noun phrases, whereby the second noun phrase is a predication over the first.


# Defining a grammar & Parser
NP = "NP: {(<V\w+>|<NN\w?>)+.*<NN\w?>}"
chunker = RegexpParser(NP)

def get_continuous_chunks(text, chunk_func=ne_chunk):
    chunked = chunk_func(pos_tag(word_tokenize(text)))
    continuous_chunk = []
    current_chunk = []

    for subtree in chunked:
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


def Parse_Draw(text):
    words = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(words)
    return tagged

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

def Find_Split_Antecedents(mentions, Tmention):
    SAmention = []
    text = ''
    for j in range(1, len(mentions)):
        Rmention = mentions[j]
        if Rmention['type'] != 'PRONOMINAL' and Rmention['number'] != 'PLURAL':# and Rmention['gender']=='':
           SAmention.append(Rmention)
           if text == '':
               text = Rmention['text']
           else:
               text += ' and '+Rmention['text']

    print ('\n'.join(map(str, SAmention)))
    print ('polo', text)

    return text,SAmention

def resolve(corenlp_output):
    for coref in corenlp_output['corefs']:
        mentions = corenlp_output['corefs'][coref]
        #print ('\n............\n'.join(map(str, mentions)))
        #a.remove('b')
        #____________________Anaphora____________________
        for j in range(1, len(mentions)):
            mention = mentions[j]
            if mention['type'] == 'PRONOMINAL':
               #print (mention)
               target_sentence = mention['sentNum']
               target_token = mention['startIndex'] - 1 

               if mention['number'] == 'SINGULAR':
                  antecedent = mentions[0] 
                  corenlp_output['sentences'][target_sentence - 1]['tokens'][target_token]['word'] = antecedent['text']
               if mention['number'] == 'PLURAL':
                  text,SAmention = Find_Split_Antecedents(mentions, mention)
                  #print ('polo', text)
                  corenlp_output['sentences'][target_sentence - 1]['tokens'][target_token]['word'] = text
        #___________________Cataphora____________________
        #_______________Split_antecedents________________
        #__________________noun phrases__________________
        
        
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

def test(text): 
    nlp = StanfordCoreNLP('/home/polo/Downloads/stanford-corenlp-full-2018-10-05/', quiet=False)
    props = {'annotators': 'dcoref', 'pipelineLanguage': 'en'}

    output = json.loads(nlp.annotate(text, properties=props))
       
    #output = nlp.annotate(text, properties= {'annotators':'dcoref','outputFormat':'json','ner.useSUTime':'false'})

    resolve(output)

    print('Original:', text)
    print('_________________________________________')
    #print('Resolved: ', end='')
    #print_resolved(output)
    #draw()
    nlp.close() 

#text = 'Barack Obama was born in Hawaii.  He is the president. Obama was elected in 2008.'
#test(text)

#test(Ana1)
#test(Ana2)

#test(Cata1)
#test(Cata2)

test(SAnt1)
#test(SAnt2)

#test(CorNP1)
#test(CorNP2)

#print(Parse_Draw(Cata1))
#print('_________________________________________')
#print(Parse_Draw(Ana2))
#df = pd.DataFrame({'text':['This is a foo, bar sentence with New York city.','Another bar foo Washington DC thingy with Bruce Wayne.']})
#df['text'].apply(lambda sent: get_continuous_chunks(sent, chunker.parse))