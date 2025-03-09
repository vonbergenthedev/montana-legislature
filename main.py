import time

from mt_all_bills import MTAllBills
from mt_bill import MTBill


all_bills_dict = MTAllBills(50).all_bills_dict
time.sleep(1)

for idx, bill in enumerate(all_bills_dict['bills']):
    current_bill = MTBill(all_bills_dict['bills'][idx]['bill_id'])
    time.sleep(.5)

