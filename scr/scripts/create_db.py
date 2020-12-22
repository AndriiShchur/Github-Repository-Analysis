#!/usr/bin/python

import sys
import os
import getpass
import pyodbc
from dotenv import load_dotenv

# Load env variables
project_folder = os.getcwd()  # adjust as appropriate
load_dotenv(os.path.join(project_folder, 'env.dist'))
server = os.getenv("SERVER")
database = os.getenv("DB")
username = os.getenv("USER")
password = os.getenv("PASSWORD")
db_name_test = os.getenv("DB_NAME_TEST")
script_name = input("Script to create DB: ")

print ("Connecting via ODBC")

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

print ("Connected!\n")

print('Run SQL query to create new DB if NOT EXISTS')

inputdir = 'sql_queries'
script_name = script_name

print('Run '+ script_name)

with open(inputdir+'\\' + script_name,'r') as inserts:
    sqlScript = inserts.read()
    sqlScript = sqlScript.replace('\n', ' ')
    for statement in sqlScript.split(';'):
        cursor.execute(statement)

print('Finished ' + script_name)

cnxn.close()