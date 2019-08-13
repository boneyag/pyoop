import os
import xml.etree.ElementTree as ET


class ReadAnnotationXML:

    """This class reads bug annotation XML files and insert the content to a python dictionary.
       Each dictionary stored in a list."""

    def __init__(self, filename):
        # object initialization
        curr_dir = os.getcwd()
        data_file_path = os.path.join(curr_dir, 'data', filename)
        # print(data_file_path)
        try:
            self.annotated_file = open(data_file_path, encoding='utf8')

        except IOError:
            print('The data file is missing!')

    def read_annoations(self, structure):
        summary_reports = []

        if self.annotated_file:
            for report in structure:
                sum_dict = {}
                for key, val in report.items():
                    for j in range(val):
                        index = str(key)+"."+str(j+1)
                        # index = str(i)+"."+str(key)+"."+str(j+1)
                        # print(index)
                        sum_dict[index] = 0
                summary_reports.append(sum_dict)
                

            # pp.pprint(summary_reports[35])

            tree = ET.parse(self.annotated_file)
            root = tree.getroot()

            i = 1
            for report in root:
                for item in report.iter('BugReport'):
                    for annotation in item.iter('Annotation'):
                        for summary in annotation.iter('ExtractiveSummary'):
                            for sentence in summary.iter('Sentence'):
                                index = str(sentence.get('ID')).strip()
                                summary_reports[i-1][index] += 1
                i += 1

            # pp.pprint(summary_reports[35])

            for sr in summary_reports:
                for key, val in sr.items():
                    if (val >= 2):
                        sr[key] = 1
                    else:
                        sr[key] = 0
        
        # pp.pprint(summary_reports[35])

        return summary_reports

