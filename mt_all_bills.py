import json
import requests


def get_bills(bill_data_dict):
    all_bills_dict = {'bills': {}}

    for idx, bill in enumerate(bill_data_dict['content']):
        bill_id = bill['draft']['id']
        draft_number = bill['draft']['draftNumber']
        short_title = bill['draft']['shortTitle']

        all_bills_dict['bills'].update({
            idx: {
                'bill_id': bill_id,
                'draft_number': draft_number,
                'short_title': short_title
            }
        })

    return all_bills_dict


class MTAllBills:

    def __init__(self, num_of_bills):
        all_bills_parameters = {"sessionIds": [2]}
        response = requests.post(
            f'https://api.legmt.gov/bills/v1/bills/search?includeCounts=false&sort=billType.sortOrder,desc&sort=billNumber,asc&sort=draft.draftNumber,asc&limit={num_of_bills}&offset=0',
            json=all_bills_parameters)
        data = response.json()
        self.all_bills_dict = get_bills(data)

        # with open('./all_bills/all_bills.json', 'w') as file:
        #     file.write(json.dumps(self.all_bills_dict))
