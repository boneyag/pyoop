import requests
import json
import os

class RestConnection:

    def __init__(self):
        pass

    def get_bug_info(self, id, filename_bug_info, filename_bug_comments):

        # getting bug info and writting to a file in json format
        serviceurl_bug_info = "https://bugzilla.mozilla.org/rest/bug/"+id+"?include_fields=id,product,summary,description"
        API_KEY = "Qk4lHMwSwB8A2WLIrJHoEmdayNRqHZ3K3nMZyxsO"

        headers = {"Content-type": "application/json"}
        params = {
                    "apikey": API_KEY,
                }

        resp = requests.get(serviceurl_bug_info, headers = headers, params = params)

        if resp.status_code != 200:
            print('error: ' + str(resp.status_code))
        else:
            print('Success')
            # print(resp.json())

        data = resp.json()
        curr_dir = os.getcwd()
        output_file_path = os.path.join(curr_dir, 'out', filename_bug_info)

        with open(output_file_path, 'w') as outfile:
            json.dump(data, outfile)

        # getting comments and writting to a file in json format
        serviceurl_bug_comments = "https://bugzilla.mozilla.org/rest/bug/"+id+"/comment"

        resp = requests.get(serviceurl_bug_comments, headers = headers, params = params)

        if resp.status_code != 200:
            print('error: ' + str(resp.status_code))
        else:
            print('Success')

        data = resp.json()
        output_file_path = os.path.join(curr_dir, 'out', filename_bug_comments)

        with open(output_file_path, 'w') as outfile:
            json.dump(data, outfile)