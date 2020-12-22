BEGIN
   IF NOT EXISTS (SELECT * FROM [dbo].[RepoMain]
                  WHERE RepoName = ?)
   BEGIN
       INSERT INTO [dbo].[RepoMain] (RepoName)
       VALUES (?)
   END
END