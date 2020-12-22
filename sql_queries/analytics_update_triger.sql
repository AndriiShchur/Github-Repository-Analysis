IF OBJECT_ID(N'analytics_update') IS NOT NULL
   DROP TRIGGER analytics_update
GO
CREATE TRIGGER [dbo].[analytics_update]
ON [dbo].[PRFiles]
AFTER INSERT, DELETE
AS
BEGIN
    EXEC analytics
END
GO