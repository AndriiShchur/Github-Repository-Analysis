CREATE TRIGGER [dbo].[analytics_update]
ON [dbo].[PRFiles]
AFTER INSERT, DELETE
AS
BEGIN 
    EXEC analytics
END
GO

ALTER TABLE [dbo].[PRFiles] ENABLE TRIGGER [analytics_update]
GO