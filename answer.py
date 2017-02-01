# Copyright 2016. DePaul University. All rights reserved. 
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.

class Answer():
	def __init__(self,AID,Answer):
		self.answer = Answer
		self.aid = AID
		
	def __str__(self):
		return '[ AnswerID: ' + str(self.aid) + ' AnswerText: ' + str(self.answer) + ']\n'
		
	def getAnswerText(self):
		return self.answer
		
	def getAnswerID(self):
		return self.aid
		
		