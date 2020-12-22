# Github-Repository-Analysis
This project help you to get data from Github with Github API and create analytics database

## Cloning

Use [GitHub CLI](https://git-scm.com/docs/git-clone) to copy this project on your machine.

```gh
gh repo clone AndriiShchur/Github-Repository-Analysis
```
## Usage
Fist of all create DB, in my Example I use Azure SQL.
I will use the following schema:

![alt text](https://github.com/AndriiShchur/Github-Repository-Analysis/blob/main/sql_queries/github_repo_db_diagram.JPG)

**Create  env.dist files with credential:**

```
SERVER="sql server name"
DB="main"
USER="your sql server name user"
PASSWORD="your sql server name password"
DB_NAME_TEST="your new db for analytics"
GIT_TOKEN = "your git token"
```

**To create DB run:**

```CMD
python scr\scripts\create_db.py
```
Insert sql script name `create_db.sql` and change DB configuration inside file if it necessary.

**To create TABLES run:**

```CMD
python scr\scripts\create_tables.sql
```
Insert sql script name `create_tables.sql` and change TABLE's schema inside file if it necessary.

**To create PROCEDURCE AND TRIGER for ANALYTICS TABLE run:**

```CMD
python scr\scripts\create_sql_proc_and_trig.sql
```
Insert sql script name `analytics_procedure.sql` for procedurce name and `analytics_update_triger.sql` for trigger name, than change parametrs inside files if it necessary.

**To get data from GitHub repository and INSERT to SQL DB run:**

```CMD
python scr\scripts\get_data_from_git.py
```
Insert sql script name `insert_new_repo.sql` to load new Repository name in `RepoMain` table, `insert_records_in_pr_main.sql`to load new PR's information in `PRMai`n TABLE,
`insert_records_in_pr_files.sql`to load new PR's files information in `PRFile` TABLE. The `RepoAnalytics` TABLE will update automaticly, when last record in `PRFile` TABLE will bee INSERT.

**To get analytic's results run:**

```SQL
SELECT ra.[RepoID]
      ,rm.[RepoName]
      ,ra.[MinPRTime]
      ,ra.[MaxPRTime]
      ,ra.[AVGPRTime]
      ,ra.[Top1File]
      ,ra.[Top2File]
      ,ra.[Top3File]
FROM [dbo].[RepoAnalytics] AS ra
LEFT JOIN RepoMain AS rm ON ra.RepoID=rm.RepoID
```
I will see the foloowinf results (*Example*):

![alt text](https://github.com/AndriiShchur/Github-Repository-Analysis/blob/main/sql_queries/results_exmp.JPG)

## Testing

To test scripts result, you can use unit test in *test/unit* folder

**To test DB creation run:**

```CMD
python -m pytest tests/unit -k "unittestdb"
```
It will test, if new DB *created/exists* and check it cofiguration.

**To test DB's schema run:**

```CMD
python -m pytest tests/unit -m "unittesttableexc"
```
It will test, if new TABLES *created/exists* and check it schema

**To test DB's schema run:**

```CMD
python -m pytest tests/unit -m "unittesttableexc"
python -m pytest tests/unit -m "unittesttablestr"
```
It will test, if new TABLES *created/exists* and check it schema

**To test If the last Repository in RepoMain TABLE have Analytics run:**

```CMD
python -m pytest tests/unit -m "unittestresults"
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
