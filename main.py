import time

from mt_all_bills import MTAllBills
from mt_bill import MTBill
from sheety_api import SheetyAPI

s_api = SheetyAPI()
all_bills_dict = MTAllBills(num_of_bills=100).all_bills_dict
time.sleep(.25)

for idx, bill in enumerate(all_bills_dict['bills']):
    current_bill = MTBill(input_bill_id=all_bills_dict['bills'][idx]['bill_id'],
                          input_bill_number=all_bills_dict['bills'][idx]['bill_number'],
                          input_bill_title=all_bills_dict['bills'][idx]['bill_title'],
                          input_draft_number=all_bills_dict['bills'][idx]['bill_draft_number']
                          )

    s_api.add_row(current_bill)
    time.sleep(.25)
