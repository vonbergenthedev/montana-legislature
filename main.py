import requests

bill_id = 2251

bill_data = requests.get(f'https://api.legmt.gov/bills/v1/votes/findByBillId?billId={bill_id}')
bill_data = bill_data.json()

legislator_votes = bill_data[0]['legislatorVotes']

bill_draft_number = bill_data[0]['bill']['draft']['draftNumber']
print(f'Draft number: {bill_draft_number}')

vote_info_dict = {f'bill_{bill_id}': {

}, 'website': f'https://bills.legmt.gov/#/laws/bill/2/{bill_draft_number}'}

for vote in legislator_votes:
    legislator_id = vote['legislatorId']
    legislator_vote = vote['voteType']



    print(f'On bill {bill_id}, legislator {legislator_id} voted {legislator_vote}')
    vote_info_dict[f'bill_{bill_id}'].update({legislator_id:legislator_vote})


print(vote_info_dict)

