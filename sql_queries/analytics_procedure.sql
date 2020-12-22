IF OBJECT_ID(N'analytics') IS NOT NULL
   DROP PROCEDURE analytics
GO
CREATE PROCEDURE [dbo].[analytics]
AS
TRUNCATE TABLE [dbo].[RepoAnalytics];

WITH tmp_rank AS (
SELECT * FROM (
               SELECT *, ROW_NUMBER() OVER(PARTITION BY [RepoID] ORDER BY [RepoID]ASC,C DESC) AS RowNo 
               FROM(
                     SELECT 
                            [RepoID]
                           ,[FileName]
	                       ,COUNT(*) AS C
                     FROM [dbo].[PRFiles]
                     GROUP BY [RepoID],[FileName]
					 ) AS tmp_1
				) AS tmp_2
WHERE RowNo <= 3
),

tmp_files AS (
SELECT TMP_1.[RepoID], TMP_1.[FileName] AS Top1File,
       TMP_2.[FileName] AS Top2File, TMP_3.[FileName] AS Top3File FROM (
	   SELECT [RepoID], [FileName], [RowNo]
	   FROM tmp_rank as tmp) AS TMP_1
LEFT JOIN (SELECT [RepoID], [FileName], [RowNo]
		   FROM tmp_rank as tmp) AS TMP_2 ON TMP_1.[RepoID]=TMP_2.[RepoID]
LEFT JOIN (SELECT [RepoID], [FileName], [RowNo]
		   FROM tmp_rank as tmp) AS TMP_3 ON TMP_1.[RepoID]=TMP_3.[RepoID]
WHERE TMP_1.[RowNo] = 1 AND TMP_2.[RowNo] = 2 AND TMP_3.[RowNo] = 3
)

INSERT INTO [dbo].[RepoAnalytics] ([RepoID], [MinPRTime], [MaxPRTime], [AVGPRTime], [Top1File], [Top2File], [Top3File])
SELECT tmp_analytics.[RepoID]
       ,MIN(DATEDIFF(hour,tmp_analytics.[CreatedAt],tmp_analytics.[MergedAt])) AS MinPRTime
	   ,MAX(DATEDIFF(hour,tmp_analytics.[CreatedAt],tmp_analytics.[MergedAt])) AS MaxPRTime
	   ,AVG(DATEDIFF(hour,tmp_analytics.[CreatedAt],tmp_analytics.[MergedAt])) AS AVGPRTime
	   ,tmp_files.Top1File,tmp_files.Top2File,tmp_files.Top3File
FROM [dbo].[PRMain] AS tmp_analytics
LEFT JOIN tmp_files ON tmp_analytics.[RepoID] = tmp_files.[RepoID]
GROUP BY tmp_analytics.RepoID,tmp_files.Top1File,tmp_files.Top2File,tmp_files.Top3File
GO