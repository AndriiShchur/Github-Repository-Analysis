import os
import getpass
import pyodbc

print("Load env variables")
project_folder = os.getcwd()  # adjust as appropriate
load_dotenv(os.path.join(project_folder, 'env.dist'))
server = os.getenv("SERVER")
database = os.getenv("DB_NAME_TEST")
username = os.getenv("USER")
password = os.getenv("PASSWORD")
script_name_proc = input("Procedurce Script: ")
script_name_trig = input("Trigger Script: ")

print ("Connecting via ODBC")

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

print ("Connected!\n")

print('Run SQL query to create new TABLES if NOT EXISTS')

inputdir = 'sql_queries'
scripts = [script_name_proc, script_name_trig]

print('Run '+ script_name)

for script in scripts:
    with open(inputdir+'\\' + script,'r') as inserts:
        sqlScript = inserts.read()
        sqlScript = sqlScript.replace('\n', ' ')
        for statement in sqlScript.split(';'):
            cursor.execute(statement)
    print('Finished ' + script)

cnxn.close()