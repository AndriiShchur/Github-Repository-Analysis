import pytest
import getpass
import pyodbc
import pandas as pd
from dotenv import load_dotenv
import os

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

query_result = ("SELECT MAX(RepoID) FROM [dbo].[RepoAnalytics]") 
result = pd.read_sql(query_result,con=cnxn).values
query_repos = ("SELECT MAX(RepoID) FROM [dbo].[RepoMain]") 
repos = pd.read_sql(query_repos,con=cnxn).values

@pytest.mark.unittestresults
def test_tables_exc():
    assert result == repos