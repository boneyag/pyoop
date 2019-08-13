import os
import xml.etree.ElementTree as ET

class ReadBugsXML:

    """This class reads bug reports XML files and insert the content to a python dictionary.
       Each dictionary stored in a list."""
       
    def __init__(self, filename):
        # object initialization
        curr_dir = os.getcwd()
        data_file_path = os.path.join(curr_dir, 'data', filename)
        # print(data_file_path)
        try:
            self.bug_file = open(data_file_path, encoding='utf8')

        except IOError:
            print('The data file is missing!')

    def read_bugs(self):

        reports = []           #contian bug report data like senteces
        structure = []         #contain bug report structure like how many turn and how many sentences in each turn

        if self.bug_file:
            tree = ET.parse(self.bug_file)
            root = tree.getroot()

            for report in root:
                b_dict = {}
                s_dict = {}
                for item in report.iter('BugReport'):
                    for title in item.iter('Title'):
                        b_dict['title'] = title.text
                    i = 1
                    for turn in item.iter('Turn'):
                        temp = {}
                        for date in turn.iter('Date'):
                            temp['date'] = date.text
                        for user in turn.iter('From'):
                            temp['user'] = user.text
                        for text in turn.iter('Text'):
                            temp2 = {}
                            j = 1
                            for sentence in text.iter('Sentence'):
                                if(sentence.text is None):
                                    temp2[sentence.get('ID')] = ''
                                else:
                                    temp2[sentence.get('ID')] = sentence.text
                                j += 1
                            temp['text'] = temp2
                        b_dict[i] = temp
                        s_dict[i] = j-1
                        i += 1
                    # s_dict['turns'] = i-1
                reports.append(b_dict)
                structure.append(s_dict)

        return reports, structure

