import os
import requests

from dotenv import load_dotenv

load_dotenv()

MT_BILLS_LAW_ENDPOINT = os.environ.get('MT_BILLS_LAW_ENDPOINT')
MT_BILLS_VOTES_ENDPOINT = os.environ.get('MT_BILLS_VOTES_ENDPOINT')


def get_bill_votes(input_bill_vote_data_dict, input_bill_number):
    if input_bill_vote_data_dict:
        legislator_votes = input_bill_vote_data_dict[0]['legislatorVotes']
        bill_draft_number = input_bill_vote_data_dict[0]['bill']['draft']['draftNumber']
        vote_info_dict = {'bill_name': input_bill_number,
                          f'bill_votes': {},
                          'link': f'{MT_BILLS_LAW_ENDPOINT}{bill_draft_number}'
                          }

        for vote in legislator_votes:
            vote_info_dict[f'bill_votes'].update({str(vote['legislatorId']): vote['voteType']})

        return vote_info_dict

    return None


class MTBill:

    def __init__(self, input_bill_id, input_bill_number, input_draft_number):
        response = requests.get(f'{MT_BILLS_VOTES_ENDPOINT}{input_bill_id}')
        bill_vote_data_dict = response.json()

        if not bill_vote_data_dict:
            self.vote_info_dict = {
                'bill_name': input_bill_number,
                'bill_votes': {},
                'link': f'{MT_BILLS_LAW_ENDPOINT}{input_draft_number}'
            }
        else:
            self.vote_info_dict = get_bill_votes(bill_vote_data_dict, input_bill_number)
