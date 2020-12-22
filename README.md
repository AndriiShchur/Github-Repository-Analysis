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

To create DB run:

```CMD
python scr\scripts\create_db.py
```
Insert sql script name `create_db.sql` and change DB configuration inside if it necessary.
