import os
import requests

from dotenv import load_dotenv

load_dotenv()

MT_ALL_BILLS_ENDPOINT = os.environ.get('MT_ALL_BILLS_ENDPOINT')


def get_bills(bill_data_dict):
    all_bills_dict = {'bills': {}}

    for idx, bill in enumerate(bill_data_dict['content']):
        bill_id = bill['draft']['id']
        bill_number = bill['billNumber']
        bill_code = bill['billType']['code']
        bill_draft_number = bill['draft']['draftNumber']
        short_title = bill['draft']['shortTitle']

        all_bills_dict['bills'].update({
            idx: {
                'bill_id': bill_id,
                'bill_number': f'{bill_code}{bill_number}',
                'bill_draft_number': bill_draft_number,
                'short_title': short_title
            }
        })

    return all_bills_dict


class MTAllBills:

    def __init__(self, num_of_bills):
        response = requests.post(f'{MT_ALL_BILLS_ENDPOINT}{num_of_bills}', json={"sessionIds": [2]})
        data = response.json()
        self.all_bills_dict = get_bills(data)
