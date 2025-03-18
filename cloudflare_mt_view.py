from bs4 import BeautifulSoup
import os
import requests
import sqlite3

from dotenv import load_dotenv
from cloudflare import Cloudflare
from sqlalchemy import create_engine, insert, text
from sqlalchemy.exc import OperationalError

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

sqliteConnection = sqlite3.connect('sql/montana-legislature-test.db')
cursor = sqliteConnection.cursor()


with open('sql/montana-legislature-test.sql', 'r') as file:
    for file_line in file:
        if 'PRAGMA' not in file_line:
            try:
                cursor.execute(file_line[:-2])
                sqliteConnection.commit()
            except sqlite3.IntegrityError:
                print('Table Exists!')
                break
            except sqlite3.OperationalError:
                print('Table Exists!')
                break
    sqliteConnection.close()

engine = create_engine("sqlite+pysqlite:///sql/montana-legislature-test.db", echo=True)
with engine.connect() as conn:
    result = conn.execute(text("select 'all_bills'"))
    print(result.all())
