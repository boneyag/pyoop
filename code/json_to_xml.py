import json
import xml.etree.ElementTree as ET
# from textblob import TextBlob
from nltk import tokenize
import os

class JsonToXml:

    def __init__(self):
        pass

    def write_to_xml(self, filename_bug_info, filename_bug_comments):

        curr_dir = os.getcwd()
        bug_file_path = os.path.join(curr_dir, 'out', filename_bug_info)
        comment_file_path = os.path.join(curr_dir, 'out', filename_bug_comments)

        with open(bug_file_path) as json_file_bug:
            bug_data = json.load(json_file_bug)

        with open(comment_file_path) as json_file_comments:
            comment_data = json.load(json_file_comments)

        xml_root = ET.Element('BugReport')

        for key in bug_data['bugs']:
            title = ET.SubElement(xml_root, 'Title')
            title.text = "(" + str(key['id']) + ") " + key['product'] + " - " + key['summary']

        for comment in comment_data['bugs']['707428']['comments']:  
            turn = ET.SubElement(xml_root, 'Turn')
            date = ET.SubElement(turn, 'Date')
            date.text = comment['time']
            author = ET.SubElement(turn, 'From')
            author.text = comment['author']
            text = ET.SubElement(turn, 'Text')

            # text_blob = TextBlob(comment['text'])
            sentences = tokenize.sent_tokenize(comment['text'])

            count = int(comment['count'])
            i = 1
            for sentence in sentences:
                line = ET.SubElement(text, str(count+1)+'.'+str(i))
                line.text = str(sentence)
                i += 1

            xml_data = ET.tostring(xml_root)

            output_path = os.path.join(curr_dir, 'out', 'text_xml_707428.xml')
            xml_out_file = open(output_path, "wb")
            xml_out_file.write(xml_data)
