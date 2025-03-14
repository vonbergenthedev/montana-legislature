from bs4 import BeautifulSoup
import os
import requests
import sqlite3

from dotenv import load_dotenv
from cloudflare import Cloudflare

load_dotenv()

client = Cloudflare()

class CLOUDFLAREMT:

    def __init__(self):
        self.at_bookmark_initial_response = client.d1.database.export(
            database_id=os.environ.get('CLOUDFLARE_DATABASE_ID'),
            account_id=os.environ.get('CLOUDFLARE_ACCOUNT_ID'),
            output_format="polling",
        )

        self.signed_url_response = client.d1.database.export(
            database_id=os.environ.get('CLOUDFLARE_DATABASE_ID'),
            account_id=os.environ.get('CLOUDFLARE_ACCOUNT_ID'),
            output_format="polling",
            current_bookmark=self.at_bookmark_initial_response.at_bookmark
        )

        self.sql_file = self.create_database_sql_file()

    def get_database_sql_export_url(self):
        return self.signed_url_response.result.signed_url

    def create_database_sql_file(self):
        database_sql_url = self.get_database_sql_export_url()
        sql_text_response = requests.get(database_sql_url)
        soup = BeautifulSoup(sql_text_response.content, 'html.parser')
        sql_text = soup.get_text()

        with open('sql/montana-legislature-test.sql', 'w') as file:
            file.write(sql_text)

        return 'sql/montana-legislature-test.sql'

cmt = CLOUDFLAREMT()
sql_file_location = cmt.sql_file
print(sql_file_location)

sqliteConnection = sqlite3.connect('sql/montana-legislature-test.db')
cursor = sqliteConnection.cursor()

with open(sql_file_location, 'r') as file:
    lines = file.readlines()
    for line in lines:
        print(f'{line}\n\n')