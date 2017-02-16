# Copyright 2016. DePaul University. All rights reserved. 
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.


class User():
    def __init__(self, UserID, UserName, UserRoleID, InterviewID):
        self.uid = UserID
        self.user = UserName
        self.permissions = UserRoleID
        self.intid = InterviewID

    def __str__(self):
        return 'UserID: ' + str(self.uid) + ' UserName: ' + str(
            self.user) + ' UserRoleID: ' + str(
                self.permissions) + ' InterviewID: ' + str(self.intid)

    def getID(self):
        return self.uid

    def getName(self):
        return self.user

    def getPer(self):
        return self.permissions

    def getIntID(self):
        return self.intid
