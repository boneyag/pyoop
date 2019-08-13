import pytextrank
import json
from nltk.corpus import stopwords
import pprint

class FilterClarrificationKeywords:
    
    def __init__(self):
        pass
    
    def preprocess_text(self, reports):
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