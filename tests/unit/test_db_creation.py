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
database = os.getenv("DB")
username = os.getenv("USER")
password = os.getenv("PASSWORD")
db_name_test = os.getenv("DB_NAME_TEST")


print ("Connecting via ODBC")
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
print ("Connected!\n")

query = ("SELECT d.name, d.catalog_collation_type_desc, slo.* \
          FROM sys.databases d \
          JOIN sys.database_service_objectives slo \
          ON d.database_id = slo.database_id \
          WHERE d.name = " + "'" + db_name_test + "'") 

db_df = pd.read_sql(query,con=cnxn)

@pytest.mark.unittestdb
def test_db():
    assert db_df.name[0] == db_name_test
    assert db_df.catalog_collation_type_desc[0] == "SQL_Latin1_General_CP1_CI_AS"
    assert db_df.edition[0] == "Basic"
    assert db_df.service_objective[0] == "Basic"