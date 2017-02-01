# Copyright 2016. DePaul University. All rights reserved. 
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.

import sqlite3
import user
import answer
import question
import interview
import active_interview
from interview_error import CredentialsException


def getUser( username, password):
        conn= sqlite3.connect( 'interview_portal.db' )
        conn.row_factory = sqlite3.Row
        select = "SELECT UserID, UserName, UserRoleID, InterviewID "
        table = "FROM UserInformation "

        row = conn.execute(select + table + "WHERE UserName = ? AND Password = ?",(username,password)).fetchone()

        if (row != None):
                res = user.User(row['UserID'],row['UserName'],row['UserRoleID'],row['InterviewID'])
                conn.close()
                return res

def getUserRole(userRoleID):
        conn= sqlite3.connect( 'interview_portal.db' )
        conn.row_factory = sqlite3.Row
        select = "SELECT UserRoleDescription "
        table = "FROM UserRole "

        row = conn.execute(select + table + "WHERE UserRoleID = ?",(str(userRoleID))).fetchone()

        return row['UserRoleDescription']


def getInterview(InterviewID):
        conn= sqlite3.connect( 'interview_portal.db' )
        conn.row_factory = sqlite3.Row
        SELECT = "SELECT ii.InterviewName, ir.QuestionID, qi.QuestionText, qr.AnswerID, a.AnswerText "
        FROM = "FROM InterviewInfo ii "
        JOINS = "INNER JOIN InterviewRelation ir ON ii.InterviewID = ir.InterviewID INNER JOIN QuestionInfo qi ON ir.QuestionID = qi.QuestionID INNER JOIN QuestionRelation qr ON qi.QuestionID = qr.QuestionID INNER JOIN AnswerInfo a on qr.AnswerID = a.AnswerID "
        rows = conn.execute(SELECT + FROM + JOINS + "WHERE ii.InterviewID = ?",(InterviewID,)).fetchall()

        try:
            InterviewName = rows[0]['InterviewName']
        except IndexError:
            res = active_interview.ActiveInterview(-1, "No interview available", [])
            return res

        Questions = {}
        for row in rows:
        	if row['QuestionID'] in Questions:
        		Questions[row['QuestionID']].putAnswer(answer.Answer(row['AnswerID'],row['AnswerText']))
        	else :
        		Questions[row['QuestionID']] = question.Question(row['QuestionID'],row['QuestionText'])
        		Questions[row['QuestionID']].putAnswer(answer.Answer(row['AnswerID'],row['AnswerText']))

        res = active_interview.ActiveInterview(InterviewID,InterviewName,list(Questions.values()))
        conn.close()
        return res


def reviewInterview(interviewID):
		res = getInterview(interviewID)
		conn= sqlite3.connect( 'interview_portal.db' )
		conn.row_factory = sqlite3.Row
		SELECT = "SELECT QuestionID, UserAnswerID "
		FROM = "FROM InterviewRelation "
		rows = conn.execute(SELECT + FROM + "WHERE InterviewID = ?", (interviewID,)).fetchall()

		Q = res.getNextQuestion()
		while Q != "End of Interview":
			id = str(Q.getQuestionID())
			for row in rows:
				if str(row['QuestionID']) == id:
					res.answerQuestion(row['UserAnswerID'])
					break
			Q = res.getNextQuestion()
		res.resetIter()
		return res


	# accept's a list of the Answer objects and inserts each into the database
def submitAnswers(ActiveInterview):
        conn= sqlite3.connect( 'interview_portal.db' )
        conn.row_factory = sqlite3.Row
        for Question in ActiveInterview.getQuestions():
        	conn.execute("UPDATE InterviewRelation SET UserAnswerID = (?) WHERE InterviewID = ? and QuestionID = ?",(Question.getUserAnswerID(), ActiveInterview.getInterviewID(), Question.getQuestionID()))
        conn.commit()
        conn.close()

	# accept's an activeInterview object and UserID and inserts the data into the database
def makeNewInterview(activeInterview, UserID):
        conn= sqlite3.connect( 'interview_portal.db' )
        conn.row_factory = sqlite3.Row
        qlist = activeInterview.getQuestions()
        IntID = conn.execute("insert into InterviewInfo(InterviewID,InterviewName) values (?,?)", (None, activeInterview.getInterviewName())).lastrowid
        for Q in qlist:
                QID = conn.execute("insert into QuestionInfo(QuestionID, QuestionText) values (?,?)", (None,Q.getQuestionText())).lastrowid
                conn.execute("insert into InterviewRelation(InterviewID, QuestionID, UserAnswerID) values (?,?,?)", (IntID, QID, -1))
                alist = Q.getAnswers()
                for A in alist:
                	AID = conn.execute("insert into AnswerInfo(AnswerID, AnswerText) values(?,?)", (None, A.getAnswerText())).lastrowid
                	conn.execute("insert into QuestionRelation(QuestionID, AnswerID) values (?,?)", (QID, AID))
                # conn.execute("insert into UserInformation(InterviewID) where UserID = ? vaules(?)", (UserID, IntID))
        conn.commit()
        conn.close()
        return IntID

def getUsers():
        conn= sqlite3.connect( 'interview_portal.db' )
        conn.row_factory = sqlite3.Row
        select = "SELECT UserID, UserName, InterviewID "
        table = "FROM UserInformation "

        rows = conn.execute(select + table + "WHERE UserRoleID = 4").fetchall()
        users = []
        for row in rows:
                users.append(user.User(row['UserID'], row['UserName'], 4, row['InterviewID']))
        return users


def getUserInterviewID(userName):
        conn= sqlite3.connect( 'interview_portal.db' )
        conn.row_factory = sqlite3.Row
        select = "SELECT InterviewID "
        table = "FROM UserInformation "

        row = conn.execute(select + table + "WHERE UserName = ?",(userName,)).fetchone()

        return row['InterviewID']

def checkIntAssigned(InterviewID):
        conn= sqlite3.connect( 'interview_portal.db' )
        conn.row_factory = sqlite3.Row
        select = "SELECT UserName "
        table = "FROM UserInformation "

        row = conn.execute(select + table + "WHERE InterviewID = ?",(str(InterviewID))).fetchone()

        if (row == None):
                return None
        else:
                return row['UserName']


def assignUser(InterviewID, UserName):
        conn= sqlite3.connect( 'interview_portal.db' )
        conn.row_factory = sqlite3.Row
        conn.execute("UPDATE UserInformation SET InterviewID = ? WHERE UserName = ?", (InterviewID, UserName))
        conn.commit()
        conn.close()
