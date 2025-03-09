import json
import requests


def get_bill_votes(bill_data_dict):

    if bill_data_dict:
        bill_id = bill_data_dict[0]['bill']['id']
        legislator_votes = bill_data_dict[0]['legislatorVotes']
        bill_draft_number = bill_data_dict[0]['bill']['draft']['draftNumber']
        vote_info_dict = {f'bill_{bill_id}': {},
                          'link': f'https://bills.legmt.gov/#/laws/bill/2/{bill_draft_number}'
                          }

        for vote in legislator_votes:
            vote_info_dict[f'bill_{bill_id}'].update({vote['legislatorId']: vote['voteType']})

        return vote_info_dict

    return -1


class MTBill:

    def __init__(self, input_bill):
        response = requests.get(f'https://api.legmt.gov/bills/v1/votes/findByBillId?billId={input_bill}')
        bill_data_dict = response.json()
        self.vote_info_dict = get_bill_votes(bill_data_dict)

        if self.vote_info_dict != -1:
            with open(f'./individual_bills/results{input_bill}.json', 'w') as file:
                file.write(json.dumps(self.vote_info_dict))
