# Copyright 2016. DePaul University. All rights reserved. 
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.

class Interview():
	def __init__(self,IntID,Title,NumQs):
		self.intid = IntID
		self.title = Title
		self.numqs = NumQs
		
	def __str__(self):
		return 'ID: ' + str(self.intid) + ' Title: ' + str(self.title) + ' NumQs: ' + str(self.numqs)
		
	def getIntID(self):
		return self.intid
		
	def getName(self):
		return self.title
		
	def getNumQs(self):
		return self.numqs