BEGIN
   IF NOT EXISTS (SELECT * FROM [dbo].[PRMain]
                  WHERE PRID = ?)
   BEGIN
       INSERT INTO [dbo].[PRMain] (RepoID, PRID, CreatedAt, MergedAt)
       VALUES (?,?,?,?)
   END
END