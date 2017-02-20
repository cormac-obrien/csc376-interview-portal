# Copyright 2016. DePaul University. All rights reserved. This work is
# distributed pursuant to the Software License for Community Contribution of
# Academic Work, dated Oct. 1, 2016. For terms and conditions, please see the
# license file, which is included in this distribution.


# an object that consists of an Interview object and a dictionary consisting of
# key value pair's, (QuestionNumber,Question) object can store and return a
# list of Answers, Answers can be stored one at a time with putAnswer() a list
# of questions may be submitted during the construction of the object or added
# one at a time after construction
class ActiveInterview():
    def __init__(self, InterviewID, InterviewName, Questions=None):
        self.interviewID = InterviewID
        self.interviewName = InterviewName
        self.questions = [] if Questions is None else Questions
        self.iter = 0
        self.InterviewLength = len(self.questions)

    def putQuestion(self, question):
        self.questions.add(question)

    def getInterviewID(self):
        return self.interviewID

    def getInterviewName(self):
        return self.interviewName

    def getQuestions(self):
        return self.questions

    def getQuestion(self):
        return self.questions[self.iter]

    def answerQuestion(self, AnswerID):
        self.questions[self.iter - 1].answerQuestion(AnswerID)

    def resetIter(self):
        self.iter = 0

    # returns the current question and increments the iter
    def getNextQuestion(self):
        print("self.interviewlength=", self.InterviewLength, "\n iter=",
              self.iter)
        if self.iter == self.InterviewLength:
            return "End of Interview"
        else:
            res = self.questions[self.iter]
            self.iter = self.iter + 1
            return res

    def __str__(self):
        ret = '\n'
        for question in self.questions:
            ret = ret + '\t' + str(question) + '\n'
        return '{ InterviewID: ' + str(
            self.interviewID) + ' InterviewName: ' + str(
                self.interviewName) + ret + '}'
