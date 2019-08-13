import sys
from code import ReadBugsXML
from code import ReadAnnotationXML
from code import WordCount
from code import RestConnection
from code import JsonToXml
from code import FilterResolution
from code import FilterClarificationQuotes
from code import FilterClarificationKeywords
import pprint

def main():
    pass
    # conn = RestConnection()
    # conn.get_bug_info('707428', 'bug_info_707428.json', 'bug_comment_707428.json')

    # json_to_xml = JsonToXml()
    # json_to_xml.write_to_xml('bug_info_707428.json', 'bug_comment_707428.json')

    bug_reports = ReadBugsXML('bugreports.xml')
    reports, structure = bug_reports.read_bugs()

    pp = pprint.PrettyPrinter(indent=4)

    # pp.pprint(reports[0])
    # pp.pprint(structure[0])

    # annotations = ReadAnnotationXML('annotation.xml')
    # summaries = annotations.read_annoations(structure)

    # pp.pprint(summaries[0])

    # wc = WordCount()
    # word_count, sentence_word_count = wc.count(reports)

    # pp.pprint(word_count[34])
    # pp.pprint(sentence_word_count[35])

    # res_state = FilterResolution()
    # res_state.find_comments(reports[1], 'se_keywords.json')

    clas_state = FilterClarificationQuotes()
    clas_state.find_matches(reports)


# invoking main

if __name__ == "__main__":
    main()