import pytest
import getpass
import pyodbc
import pandas as pd
from dotenv import load_dotenv
import os
import math

print("Load env variables")
project_folder = os.getcwd()  # adjust as appropriate
load_dotenv(os.path.join(project_folder, 'env.dist'))
server = os.getenv("SERVER")
database = os.getenv("DB_NAME_TEST")
username = os.getenv("USER")
password = os.getenv("PASSWORD")

print ("Connecting via ODBC")
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
print ("Connected!\n")

query = ("SELECT DISTINCT TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS") 
tables_df = pd.read_sql(query,con=cnxn)

tables = ["RepoMain", "PRMain", "PRFiles", "RepoAnalytics"]

@pytest.mark.unittesttableexc
def test_tables_exc():

    for table in tables:
        assert table in tables_df.TABLE_NAME.values

query = ("SELECT TABLE_NAME, COLUMN_NAME, IS_NULLABLE, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH \
          FROM INFORMATION_SCHEMA.COLUMNS \
          WHERE TABLE_NAME NOT IN ('database_firewall_rules','sysdiagrams')") 
tables_df = pd.read_sql(query,con=cnxn)
tables_str = pd.read_csv(os.path.join(os.getcwd(), "scr\\tables_str\\tables_str.csv"))

@pytest.mark.unittesttablestr
def test_tables_exc():
    
    for table in tables:
        
        tmp_df1 = tables_df[tables_df.TABLE_NAME==table]
        tmp_str1 = tables_str[tables_str.TABLE_NAME==table]

        for column in tmp_str1.COLUMN_NAME:
            
            print(column in tmp_df1.COLUMN_NAME.values)
            
            tmp_df2 = tmp_df1[tmp_df1.COLUMN_NAME==column]
            tmp_str2 = tmp_str1[tmp_str1.COLUMN_NAME==column]
            print(tmp_str2.IS_NULLABLE.values == tmp_df2.IS_NULLABLE.values)
            print(tmp_str2.DATA_TYPE.values == tmp_df2.DATA_TYPE.values)
            if(math.isnan(tmp_str2.CHARACTER_MAXIMUM_LENGTH.values[0]) and 
            math.isnan(tmp_df2.CHARACTER_MAXIMUM_LENGTH.values[0])):
                print(True)
            else:
                print(tmp_str2.CHARACTER_MAXIMUM_LENGTH.values == tmp_df2.CHARACTER_MAXIMUM_LENGTH.values)

