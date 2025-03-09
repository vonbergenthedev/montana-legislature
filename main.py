import time

from mt_all_bills import MTAllBills
from mt_bill import MTBill


all_bills_dict = MTAllBills(10).all_bills_dict
time.sleep(.5)


for idx, bill in enumerate(all_bills_dict['bills']):
    current_bill = MTBill(all_bills_dict['bills'][idx]['bill_id'], all_bills_dict['bills'][idx]['draft_number'])
    time.sleep(.5)

