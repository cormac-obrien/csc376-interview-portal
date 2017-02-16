# Copyright 2016. DePaul University. All rights reserved.
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.

import db_interaction


class CredentialsException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, "Username or password incorrect.", **kwargs)
        print("Username or password incorrect.")

    def startInterview(self, InterviewID):
        try:
            self.Interview = db_interaction.getInterview(self.InterviwID)
        except:
            print('Sorry No Interview Found')
            raise CredentialsException('No Ineterview Found!')
        else:
            print('Now Starting the Interview')
