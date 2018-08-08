-- ToDo database Build
-- V1.0

IF NOT EXISTS	(
					SELECT database_id
					FROM [master].[sys].[databases] WHERE [name] = 'ToDo'
				)
	CREATE DATABASE ToDo;
GO

USE ToDo;
GO

IF OBJECT_ID('dbo.TaskCount')			IS NOT NULL DROP SEQUENCE dbo.TaskCount;
IF OBJECT_ID('dbo.tasks', 'U')			IS NOT NULL DROP TABLE dbo.tasks;
IF OBJECT_ID('dbo.GetActiveTasks', 'P')	IS NOT NULL DROP PROCEDURE dbo.GetActiveTasks;
IF OBJECT_ID('dbo.AddTask', 'P')		IS NOT NULL DROP PROCEDURE dbo.AddTask;
IF OBJECT_ID('dbo.CompleteTask', 'P')	IS NOT NULL DROP PROCEDURE dbo.CompleteTask;
IF OBJECT_ID('dbo.RemoveTask', 'P')		IS NOT NULL DROP PROCEDURE dbo.RemoveTask;
GO

CREATE SEQUENCE dbo.TaskCount
START WITH 1
INCREMENT BY 1;
GO

CREATE TABLE dbo.Tasks
(
    TaskID		INT				NOT NULL,
    TaskDesc	VARCHAR(100)	NULL,
	StartDate	DATE			NULL,
	EndDate		DATE			NULL,
	IsComplete	BIT				NULL
	CONSTRAINT	DF_IsComplete	DEFAULT (0),
	CONSTRAINT	PK_TaskID
	PRIMARY KEY	(TaskID)
);
GO

CREATE PROCEDURE dbo.GetActiveTasks
AS
SELECT	TaskID,
		TaskDesc,
		StartDate
FROM	dbo.Tasks
WHERE	IsComplete = 0;
GO

CREATE PROCEDURE dbo.AddTask
	@TaskText AS VARCHAR(100)
AS
INSERT INTO	dbo.Tasks
VALUES		(NEXT VALUE FOR dbo.TaskCount, @TaskText, GETDATE(), NULL, 0)
GO

CREATE PROCEDURE dbo.CompleteTask
	@SelectedID AS INT
AS
UPDATE	dbo.Tasks
SET		EndDate = GETDATE(),
		IsComplete = 1
WHERE	TaskID = @SelectedID
GO

CREATE PROCEDURE dbo.RemoveTask
	@SelectedID AS INT
AS
DELETE FROM dbo.Tasks
WHERE	TaskID = @SelectedID
GO