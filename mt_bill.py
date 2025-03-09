import pandas as pd
import json
import requests
import openpyxl


def get_bill_votes(bill_data_dict):
    if bill_data_dict:
        bill_id = bill_data_dict[0]['bill']['id']
        legislator_votes = bill_data_dict[0]['legislatorVotes']
        bill_draft_number = bill_data_dict[0]['bill']['draft']['draftNumber']
        vote_info_dict = {'bill_name': bill_id,
                          f'bill_votes': {},
                          'link': f'https://bills.legmt.gov/#/laws/bill/2/{bill_draft_number}'
                          }

        for vote in legislator_votes:
            vote_info_dict[f'bill_votes'].update({vote['legislatorId']: vote['voteType']})

        return vote_info_dict

    return None


class MTBill:

    def __init__(self, input_bill, input_draft_number):
        response = requests.get(f'https://api.legmt.gov/bills/v1/votes/findByBillId?billId={input_bill}')
        bill_data_dict = response.json()
        self.vote_info_dict = get_bill_votes(bill_data_dict)

        with open(f'./individual_bills/results{input_bill}.json', 'w') as file:
            if self.vote_info_dict is not None:
                file.write(json.dumps(self.vote_info_dict))
                df = pd.DataFrame([self.vote_info_dict])
                df.to_excel(f'./individual_bills/results{input_bill}.xlsx', index=False)

            else:
                bill_link = 'https://bills.legmt.gov/#/laws/bill/2/'

                df = pd.DataFrame([{
                    'bill_name': input_bill,
                    f'bill_votes': {},
                    'link': f'{bill_link}{input_draft_number}'
                }])

                df.to_excel(f'./individual_bills/results{input_bill}.xlsx', index=False)
                file.write(json.dumps({
                    'bill_name': input_bill,
                    f'bill_votes': {},
                    'link': f'{bill_link}{input_draft_number}'
                }))
