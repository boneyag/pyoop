import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
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
        
        # print(key, '\t', bug_repot_dict[key])
        query = re.sub(r'^>\s?', '', bug_repot_dict[key])
        query = re.sub(r'\s\s+', ' ', query)
        # print(len(query),":", query)
        
        
               
        # print('\nMatches for quotes\n')
        if (len(query) != 0):
            for i in range(start_index-1, 0, -1):
                
                try:
                    # search_space = self.clean_sentence(bug_repot_dict[list_of_keys[i]])
                    res = re.search(query, bug_repot_dict[list_of_keys[i]])
                
                except sre_constants.error:
                    continue
                
                if res:
                    print(key, '\t-> ' , list_of_keys[i])
                    print(list_of_keys[i],':',bug_repot_dict[list_of_keys[i]])
                    return key
    
    def find_links(self, turn, key, report):
        
        # positive_responses contain sentence IDs that has full/partial match to query
        positive_responses = []
                
        # responses contain any sentence IDs that don't start with '>'
        responses = []
                
        lemmatizer = WordNetLemmatizer()
        
        for k2 in report[turn]['text'].keys():
            if (report[turn]['text'][k2][:5] != ' &gt;' and k2 > key):
                responses.append(k2)
        quote_token = self.remove_stop_words(report[turn]['text'][key])
        quote_token.remove('&gt;')
        quote_token = [lemmatizer.lemmatize(token, 'v') for token in quote_token]
        
        for res in responses:
            temp_token = self.remove_stop_words(report[turn]['text'][res])
            temp_token = [lemmatizer.lemmatize(token, 'v') for token in temp_token]
            if bool(set(quote_token).intersection(set(temp_token))):
                positive_responses.append(res)
            
            temp_string = ' '.join(temp_token)
            temp_string.strip()
            
            quote_string = ' '.join(quote_token)
            quote_string.strip()
            # print(fuzz.ratio(quote_string, temp_string))
            print(process.extract(quote_string, temp_string))
            # print(fuzz.ratio(quote_token, temp_token))
                        
            # for token in quote_token:
            #     temp_extracts = process.extract(token, temp_token)
            #     print(token,":",[item for item in temp_extracts if item[1] > 50]) 
                # if (process.extract(token, temp_token)[1] > 50):
                #     if res not in positive_responses:
                #         positive_responses.append(res)
                # print(token,':',process.extract(token, temp_token))
        print(positive_responses)  
        
    def remove_stop_words(self, text):
 
        stopwords_en = set(stopwords.words('english'))   
        
        tokens = text.split()
        
        return [w for w in tokens if w not in stopwords_en]    
                        
    def clean_sentence(self, text):
        temp_text = text
        temp_text2 = html.unescape(text)
        
        while (temp_text != temp_text2):
            temp_text = temp_text2
            temp_text2 = html.unescape(temp_text2)
            
        text = temp_text
        
        new_text = re.sub(r'\-+|\=\=+|\*+', '', text)
        new_text = re.sub(r'\[details\]', '', new_text)
        
        new_text = re.sub(r'\s\s+', ' ', new_text)
        new_text = re.sub(r'(^\s)|(\s$)', '', new_text)
        
        return new_text
    
    def find_matches(self, reports):
        # dictionary to hold comment ID and tokenized words after removing stop words
        # and decoding escape chars and HTML symbols

        bug_repot_dict = {}
        i = 0
        for k1 in reports[i].keys():
            if (k1 != 'title'):
                for k2 in reports[i][k1]['text'].keys():
                    bug_repot_dict[k2] = self.clean_sentence(reports[i][k1]['text'][k2])
        # pp.pprint(bug_repot_dict)

        for k1 in bug_repot_dict.keys():
            if (re.match(r'^>.*', bug_repot_dict[k1])):
                key = self.find_a_match(k1, bug_repot_dict)
                
                if key != None:
                    turn = key.split('.')[0]
                    self.find_links(int(turn), key, reports[i])
                
                
                
                
