-- Copyright 2016. DePaul University. All rights reserved. 
-- This work is distributed pursuant to the Software License
-- for Community Contribution of Academic Work, dated Oct. 1, 2016.
-- For terms and conditions, please see the license file, which is
-- included in this distribution.

BEGIN TRANSACTION;
CREATE TABLE "UserRole" (
	`UserRoleID`	INTEGER NOT NULL UNIQUE,
	`UserRoleDescription`	TEXT NOT NULL,
	`CreateInterview`	INTEGER NOT NULL DEFAULT 0,
	`ViewInterview`	INTEGER NOT NULL DEFAULT 0,
	`CreateQuestion`	INTEGER NOT NULL DEFAULT 0,
	`ModifyQuestions`	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY(`UserRoleID`)
);
INSERT INTO `UserRole` (UserRoleID,UserRoleDescription,CreateInterview,ViewInterview,CreateQuestion,ModifyQuestions) VALUES (1,'System Admin',1,1,1,1),
 (2,'Lawyer',1,1,1,1),
 (3,'Legal Aide',1,1,0,0),
 (4,'Interviewee',0,0,0,0);
CREATE TABLE "UserInformation" (
	`UserID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`UserRoleID`	INTEGER NOT NULL DEFAULT 1,
	`UserName`	TEXT NOT NULL UNIQUE,
	`Password`	TEXT NOT NULL,
	`FirstName`	TEXT NOT NULL,
	`LastName`	TEXT NOT NULL,
	`StreetAddress`	TEXT NOT NULL,
	`City`	TEXT NOT NULL,
	`State`	TEXT NOT NULL,
	`ZIP`	TEXT NOT NULL,
	`InterviewID`	INTEGER UNIQUE,
	FOREIGN KEY(`UserRoleID`) REFERENCES `UserRole`(`UserRoleID`),
	FOREIGN KEY(`InterviewID`) REFERENCES InterviewInfo(InterviewID)
);
INSERT INTO `UserInformation` (UserID,UserRoleID,UserName,Password,FirstName,LastName,StreetAddress,City,State,ZIP,InterviewID) VALUES (1,1,'jking','pw123','Jimmy','King','222 S. Riverside Plaza','Chicago','IL','60606',NULL),
 (2,4,'NYjohn','pw123','John','Doe','123 Sesame St.','New York','NY','12345',NULL),
 (3,2,'adossaji','pw123','Adnan','Dossaji','555 Somestreet Apt 3','Chicago','IL','60006',NULL),
 (4,3,'akhan','pw123','Arshad','Khan','888 Another St.','Chicago','IL','65432',NULL),
 (5,4,'bmeng','pw123','Brandon','Meng','412 This Ave.','Chicago','IL','60123',NULL),
 (6,1,'ccastino','pw123','Cody','Castino','777 Park Pl.','Chicago','IL','60321',NULL),
 (7,4,'kcardenas','pw123','Karen','Cardenas','9876 North Ave','Chicago','IL','60526',1),
 (8,4,'kzonca','pw123','Keaton','Zonca','5432 South Ave','Chicago','IL','60625',2),
 (9,4,'kalrawaf','pw123','Khalid','Alrawaf','1098 East Ave','Chicago','IL','61854',3),
 (10,4,'mcurrent','pw123','Matthew','Current','7654 West Ave','Chicago','IL','62965',NULL),
 (11,4,'tplutz','pw123','Tom','Plutz','3333 Center St.','Chicago','IL','65748',NULL);
CREATE TABLE "QuestionRelation" (
	`QuestionID`	INTEGER NOT NULL,
	`AnswerID`	INTEGER NOT NULL,
	FOREIGN KEY(`QuestionID`) REFERENCES `QuestionInfo`(`QuestionID`),
	FOREIGN KEY(`AnswerID`) REFERENCES `AnswerInfo`(`AnswerID`)
);
INSERT INTO `QuestionRelation` (QuestionID,AnswerID) VALUES (1,1),
 (1,2),
 (1,3),
 (1,4),
 (1,5),
 (2,12),
 (2,13),
 (2,14),
 (3,8),
 (3,9),
 (3,10),
 (4,6),
 (4,7),
 (4,11),
 (5,14),
 (5,13),
 (5,12),
 (6,1),
 (6,2),
 (6,11),
 (7,3),
 (7,4),
 (7,5);
CREATE TABLE "QuestionInfo" (
	`QuestionID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`QuestionText`	TEXT NOT NULL
);
INSERT INTO `QuestionInfo` (QuestionID,QuestionText) VALUES (1,'Is this working?'),
 (2,'How are you doing today?'),
 (3,'Which is more likely?'),
 (4,'Can you resist?'),
 (5,'No really, how are you doing?'),
 (6,'Seriously, its that bad?'),
 (7,'Are you sure it is working?');
CREATE TABLE "InterviewRelation" (
	`InterviewID`	INTEGER NOT NULL,
	`QuestionID`	INTEGER NOT NULL,
	`UserAnswerID`	INTEGER NOT NULL DEFAULT -1,
	FOREIGN KEY(`InterviewID`) REFERENCES `InterviewInfo`(`InterviewID`),
	FOREIGN KEY(`QuestionID`) REFERENCES `QuestionInfo`(`QuestionID`),
	FOREIGN KEY(`UserAnswerID`) REFERENCES `AnswerInfo`(`AnswerID`)
);
INSERT INTO `InterviewRelation` (InterviewID,QuestionID,UserAnswerID) VALUES (1,1,-1),
 (3,2,-1),
 (1,7,-1),
 (2,3,-1),
 (2,4,-1),
 (3,6,-1),
 (3,5,-1),
 (1,4,-1),
 (2,7,-1),
 (1,2,-1);
CREATE TABLE "InterviewInfo" (
	`InterviewID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`InterviewName`	TEXT NOT NULL UNIQUE
);
INSERT INTO `InterviewInfo` (InterviewID,InterviewName) VALUES (1,'Test Interview 1'),
 (2,'Welness Check'),
 (3,'What is more likely?');
CREATE TABLE "AnswerInfo" (
	`AnswerID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`AnswerText`	TEXT NOT NULL
);
INSERT INTO `AnswerInfo` (AnswerID,AnswerText) VALUES (1,'Yes'),
 (2,'No'),
 (3,'Maybe'),
 (4,'Probably'),
 (5,'Never'),
 (6,'Do not choose this answer no matter what!'),
 (7,'Pick me! Me me me!'),
 (8,'The Cubs will win the World Series in 2016.'),
 (9,'Donald Trump will become president of the United States.'),
 (10,'Earth will get hit by a meteor leading to mass extinction.'),
 (11,'I REFUSE!'),
 (12,'I''m doing well, thanks!'),
 (13,'Put me in Cryo-Stasis for 4 years, please!'),
 (14,'I have no opinion.');
COMMIT;
