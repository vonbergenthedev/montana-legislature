import os
import requests

from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN = os.environ.get('SHEETY_BEARER_TOKEN')
SHEETY_ENDPOINT = os.environ.get('SHEETY_ENDPOINT')


class SheetyAPI:

    def __init__(self):
        self.header = {
            'Authorization': BEARER_TOKEN
        }

    def get_sheet_data(self):
        response = requests.get(SHEETY_ENDPOINT, headers=self.header)

        return response.json()

    def add_row(self, mt_bill):
        body = {
            'allBill': {
                'billName': mt_bill.vote_info_dict['bill_name'],
                'billTitle': mt_bill.vote_info_dict['bill_title'],
                'billVotes': str(mt_bill.vote_info_dict['bill_votes']),
                'link': mt_bill.vote_info_dict['link'],
            }
        }

        response = requests.post(SHEETY_ENDPOINT, headers=self.header, json=body)
        # print(response.text)
