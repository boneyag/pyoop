import re
import nltk
from nltk import WordNetLemmatizer
from textblob import TextBlob
import os
import json
import string

class FilterResolution:

    """ This class detect comments that are related to resolution status
        and filter out irrelavant link that are not related to commits or 
        push statements. Common keywords are push(ed), attachment, commit 
        and patch """

    def __init__(self):
        pass

    def find_comments(self, bug_report, filename_keywords):
        wordnet_lemmatizer = WordNetLemmatizer()

        curr_dir = os.getcwd()
        keywords_file_path = os.path.join(curr_dir, 'data', filename_keywords)

        try:
            with open(keywords_file_path) as json_file_keywords:
                keywords_data = json.load(json_file_keywords)

        except IOError:
            print('The data file is missing!')

        resolution_keywords = keywords_data['resolution']
        
        print(resolution_keywords, '\n')

        # comment filteration process
        # 1) ignore title and first comment (first comment is the bug description)
        # 2) ignore quoted sentences as those already captured
        # 3) ignore the bugzilla url (often refer to another bug reported) 
        for key in bug_report.keys():
            if (key != 'title') and (key != 1):
                for key2 in bug_report[key]['text'].keys():
                    if any(keyword in wordnet_lemmatizer.lemmatize(bug_report[key]['text'][key2].lower()) for keyword in resolution_keywords):
                        if (re.match(r'^(&gt;).', bug_report[key]['text'][key2].strip())) is None:
                            # bi_gram = nltk.ngrams(bug_report[key]['text'][key2].split(), 2)
                            # for gram in bi_gram:
                            #     print(gram)
                            # print('\n')
                            if (re.match(r'.*http[s]://bugzilla\..+', bug_report[key]['text'][key2])) is None:
                                print(bug_report[key]['text'][key2])
                        # print(bug_report[key]['text'][key2].lower())

        