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
