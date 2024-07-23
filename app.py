import streamlit as st
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, select, column, inspect
from dotenv import load_dotenv
from urllib.parse import quote
import os

from llama_index.core import SQLDatabase
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import LLM
from llama_index.core.query_engine import NLSQLTableQueryEngine
from hdbcli import dbapi

from io import StringIO
import pandas as pd


load_dotenv()
username = str(os.getenv('DB_USER'))
passwd = os.getenv('DB_PASS')
hostname = os.getenv('DB_HOST')
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

#engine = create_engine('hana+hdbcli://sivkris:Dtte123$@usa014.us.dte.com/DS4')
engine = create_engine("hana+hdbcli://{}:{}@{}/DS4".format(username,passwd,hostname))
#insp = inspect(engine)  # will be a HANAInspector
#print(insp.get_table_names('SAPS4H'))

llm = OpenAI(temperature=0.1, model="gpt-4o") #gpt-3.5-turbo"

sql_database = SQLDatabase(engine,schema = 'SAPS4H',include_tables=['vbak','vbap','mara','makt','vbfa'])

def query(query_string):
    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database,
        tables=['vbak','vbap','mara','makt','vbfa'],
        llm=llm
    )
    query_template = '''{}. 
        Present the output in CSV format with headers. 
        Do not generate SQL statements for exporting to CSV. 
        Do not provide additional descriptions apart from the data. 
        Always display a header row containing the column descriptions.
        '''.format(query_string)
    response = query_engine.query(query_template)
    return response

input = input('Enter query: ')
response = query(input)
print(response.metadata['sql_query'])
print(response)
