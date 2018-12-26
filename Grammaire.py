#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 12:05:03 2018

@author: Yazid Bounab
"""
import nltk
from nltk import RegexpParser
from nltk.tree import Tree

from nltk import word_tokenize, pos_tag, ne_chunk

chunker = r"""
    VP:{<VB.*><DT><NN.*>} 
    AdvP: {<RB.*><VB.*|JJ.*|NN.*>}
    """

pattern = """NP: {<DT>?<JJ>*<NN>}
             VP: {<VB.*><DT><NN.*>}
             ADJP : {}
             ADVP : {<RB.*><VB.*|JJ.*|NN.*>}
             PP : {}
             """
             
text = "This has allowed the device to start, and I then see glitches which is not nice."
tagged_text = pos_tag(word_tokenize(text))    

#_______________________________________________________________

def get_continuous_chunks(text, chunk_func=ne_chunk):
    chunked = chunk_func(pos_tag(word_tokenize(text)))
    continuous_chunk = []
    current_chunk = []

    for subtree in chunked:
        print(subtree)
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

#_______________________________________________________________

#print(get_continuous_chunks(text, chunk_func=chunker))

#p = RegexpParser(g)
#p.parse(tagged_text)
#print (p)
    
## Defining the POS tagger 


## A Single sentence - input text value
textv="This has allowed the device to start, and I then see glitches which is not nice."
tagged_text = pos_tag(word_tokenize(text))

## Defining Grammar rules for  Phrases
actphgrammar = r"""
     Ph: {<VB*>+<DT>?<NN*>+}  # verbal phrase - one or more verbs followed by optional determiner, and one or more nouns at the end
     {<RB*><VB*|JJ*|NN*\$>} # Adverbial phrase - Adverb followed by adjective / Noun or Verb
     """

### Parsing the defined grammar for  phrases
actp = RegexpParser(pattern)#actphgrammar)

actphrases = actp.parse(tagged_text)

print (actphrases)