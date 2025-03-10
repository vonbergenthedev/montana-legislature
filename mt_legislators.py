import os
import requests

from dotenv import load_dotenv

load_dotenv()

MT_LEGISLATORS_ENDPOINT = os.environ.get('MT_LEGISLATORS_ENDPOINT')


class MTLegislators:

    def __init__(self):
        response = requests.get(f'{MT_LEGISLATORS_ENDPOINT}')
        self.legislator_data = response.json()

    def get_legislator_information(self):
        return [{'id': legislator['id'], 'firstName': legislator['firstName'], 'lastName': legislator['lastName']} for
                legislator in self.legislator_data]
