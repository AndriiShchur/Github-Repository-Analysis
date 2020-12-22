IF NOT EXISTS(SELECT * FROM sysobjects WHERE NAME='RepoMain' and xtype='U')
       CREATE TABLE RepoMain (
                    RepoID INT IDENTITY(1,1) PRIMARY KEY,
                    RepoName VARCHAR(255) NOT NULL
					);

IF NOT EXISTS(SELECT * FROM sysobjects WHERE NAME='RepoMain' and xtype='U')
       CREATE TABLE PRMain (
	                RepoID INT FOREIGN KEY
					           REFERENCES RepoMain(RepoID)
					                      ON DELETE CASCADE
										  ON UPDATE NO ACTION,
	                PRID INT PRIMARY KEY,
                    CreatedAt DATETIME,
	                MergedAt DATETIME
					);

IF NOT EXISTS(SELECT * FROM sysobjects WHERE NAME='RepoMain' and xtype='U')
       CREATE TABLE PRFiles (
	                RepoID INT FOREIGN KEY
					           REFERENCES RepoMain(RepoID)
					                      ON DELETE CASCADE
										  ON UPDATE NO ACTION,
                    PRID INT FOREIGN KEY 
					         REFERENCES PRMain(PRID)
							            ON DELETE CASCADE
										ON UPDATE NO ACTION,
                    FileName VARCHAR(255) NOT NULL
					);

IF NOT EXISTS(SELECT * FROM sysobjects WHERE NAME='RepoMain' and xtype='U')
       CREATE TABLE RepoAnalytics (
                    RepoID INT FOREIGN KEY 
					           REFERENCES RepoMain(RepoID)
							              ON DELETE CASCADE
										  ON UPDATE NO ACTION,
                    MinPRTime NUMERIC,
	                MaxPRTime NUMERIC,
	                AVGPRTime NUMERIC,
	                Top1File VARCHAR(255),
	                Top2File VARCHAR(255),
	                Top3File VARCHAR(255)
					)