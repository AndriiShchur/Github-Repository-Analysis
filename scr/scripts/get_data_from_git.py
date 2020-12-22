#!/usr/bin/python

import sys
import os
import getpass
import pyodbc
from github import Github
import pandas as pd
import numpy as np 
from dotenv import load_dotenv
import os

print("Load env variables")
project_folder = os.getcwd()  # adjust as appropriate
load_dotenv(os.path.join(project_folder, 'env.dist'))
server = os.getenv("SERVER")
database = os.getenv("DB_NAME_TEST")
username = os.getenv("USER")
password = os.getenv("PASSWORD")
git_token = os.getenv("GIT_TOKEN")
script_insert_repo_info = input("Script For Insert New Repository in DB: ")
script_insert_pr_info = input("Script For Insert New PRs in DB: ")
script_insert_file_info = input("Script For Insert New PR's Files in DB: ")

print ("Connecting to GitHub")
new_repo_name = new_repo_name
g = Github(login_or_token = git_token)
git_repo = g.get_repo(new_repo_name)

print ("Connecting via ODBC")
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';\
                       DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
print ("Connected!\n")

print('Inserting new record in RepoMain table')
inputdir = 'sql_queries'
script_name_1 = 'insert_new_repo.sql'
with open(inputdir+'\\' + script_name_1,'r') as inserts:
    sqlScript = inserts.read()
    sqlScript = sqlScript.replace('\n', ' ')
cursor.execute(sqlScript, new_repo_name,new_repo_name)
cnxn.commit()
print('Insert success')

print('Get RepoID for new Repository in DB')
query = ("SELECT [RepoID] FROM [dbo].[RepoMain] WHERE [RepoName] = " + "'" + new_repo_name + "'") 
RepoID = pd.read_sql(query,con=cnxn).RepoID[0]

print("Get PR's information from Git")
rows_id_dates = []
rows_files = []

try:
    for pull in git_repo.get_pulls('closed'):
        if(pull.merged_at is None):
            print(" Status: %s " %("PR not merged"), end="\r")
        else:
            rows_id_dates.append([RepoID, int(str(RepoID) + str(pull.number)), pull.created_at, pull.merged_at])
            files = pull.get_files()
            for file in files.reversed:
                rows_files.append( [RepoID, int(str(RepoID) + str(pull.number)), file.filename])
                print(" Status: %s " %("PR merged"), end="\r")
except:
    print("github.GithubException.RateLimitExceededException: 403")

PRMain_df = pd.DataFrame(rows_id_dates, columns=["RepoID", "PRID",
                                                 "CreatedAt", "MergedAt"])
PRFiles_df = pd.DataFrame(rows_files, columns=["RepoID","PRID","FileName"])
print("PR's information is ready to update")

print('Inserting new record in PRMain and PRFiles')
with open(inputdir+'\\' + script_insert_pr_info,'r') as inserts:
    sqlScript_2 = inserts.read()
    sqlScript_2 = sqlScript_2.replace('\n', ' ')
    
with open(inputdir+'\\' + script_insert_file_info,'r') as inserts:
    sqlScript_3 = inserts.read()
    sqlScript_3 = sqlScript_3.replace('\n', ' ')

cursor = cnxn.cursor()
for index, row1 in PRMain_df.iterrows():
    print("Insert PRID: %s " %(str(row1.PRID)), end="\r")
    cursor = cnxn.cursor()
    cursor.execute(sqlScript_2, row1.PRID, row1.RepoID, row1.PRID, row1.CreatedAt, row1.MergedAt)
    cnxn.commit()
    cursor.close()
    for index2, row2 in PRFiles_df[PRFiles_df.PRID == row1.PRID].iterrows():
        cursor = cnxn.cursor()
        cursor.execute(sqlScript_3, row1.RepoID, row2.PRID, row2.FileName)
        cnxn.commit()
        cursor.close()
print('Insert success')