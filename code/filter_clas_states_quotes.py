import nltk
from nltk import PorterStemmer
from nltk import SnowballStemmer
# from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import sre_constants
import os
import json
import codecs
import html
import pprint

class FilterClarificationQuotes:

    """ This class detect comments that have quoted sentence
        and links between sentence based on word similarity 
        symbols indicate that a sentence is quoted from previous
        sentence/comment """

    def __init__(self):
        pass

    def find_a_match(self, key, bug_repot_dict):
        list_of_keys = list(bug_repot_dict.keys())
        
        start_index = list_of_keys.index(key)
        query = re.sub(r'^> ', '', bug_repot_dict[key])
        
        
        for i in range(start_index-1, 0, -1):
            # print(bug_repot_dict[list_of_keys[i]])
            
            try:
                res = re.search(query, bug_repot_dict[list_of_keys[i]])
            
            except sre_constants.error:
                continue
            
            if res:
                print(query)
                print(list_of_keys[i],':',bug_repot_dict[list_of_keys[i]])
        
    def find_matches(self, reports):
        pp = pprint.PrettyPrinter(indent=4)

        stopwords_en = set(stopwords.words('english'))

        # dictionary to hold comment ID and tokenized words after removing stop words
        # and decoding escape chars and HTML symbols

        bug_repot_dict = {}
        i = 27
        for k1 in reports[i].keys():
            if (k1 != 'title'):
                for k2 in reports[i][k1]['text'].keys():
                    tokens = reports[i][k1]['text'][k2].split()
                    # print([html.unescape(codecs.getdecoder("unicode_escape")(token.lower())[0]) \
                    #    for token in tokens if token.lower() not in stopwords_en])
                    temp_str = ' '.join([html.unescape(codecs.getdecoder("unicode_escape")(token.lower())[0]) \
                        for token in tokens if token.lower() not in stopwords_en])
                    bug_repot_dict[k2] = temp_str.strip()
        # pp.pprint(bug_repot_dict)

        for k1 in bug_repot_dict.keys():
            if (re.match(r'^>.*', bug_repot_dict[k1])):
                self.find_a_match(k1, bug_repot_dict)
                
                
