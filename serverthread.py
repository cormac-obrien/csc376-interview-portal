# Copyright 2016. DePaul University. All rights reserved. 
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.

import sys
import threading
import socket
import sqlite3
import db
import random

class ServerThread(threading.Thread):    
    def __init__(self, client_socket, connection_id):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self._USER_NAME = ''
        self._USER_PW = ''
        self.connection_id = connection_id

    def terminate_session(self):
        print('Terminating connection', self.connection_id)
        sys.stdout.flush()
        self.client_socket.close()
        print('Socket closed')
        sys.stdout.flush()
     
      
    # =========================================================================
    #             LAWYER: INTERVIEW CREATION   
    #
    # Status: needs testing and refinement
    # 
    # Precondition: 
    # - Lawyer/Staff access
    # - create interview option selected
    #
    # Postcondition:
    # - interview recorded in database
    #
    # TO DO
    # - PROTOCOL: add database interactions
    # - ENCRYPTION: add redirect to Lawyer Options
    # - SYNC: test/refine loop control
    # - SYNC: fix input transition to control loop
    # =========================================================================
    def create_interview(self):
        
        # interview creation intro
        self.client_socket.send( ('Interview Creation').encode() )
        # db connection
        conn = sqlite3.connect( 'interview.db' )
        
        # interview name entry
        self.client_socket.send( ('Enter a name for the interview').encode() )
        name = self.client_socket.recv(1024).decode()
        
        # interview description entry
        self.client_socket.send( ('Enter a description for the interview').encode() )
        desc = self.client_socket.recv(1024).decode()

        # generates a pseudorandom, unique ID for this INTERVIEW
        unique = False
        while(not unique):
            interview_id = random.randrange(1, 99999)
            if(interview_id not in conn.execute('SELECT interview_id FROM Interviews')):
                unique = True

        # create interview
        db.create_interview(conn, interview_id, name, desc)

        ## INTERVIEW CREATION LOOP ##
        while(True):

            # generates a pseudorandom, unique ID for this QUESTION
            unique = False
            while(not unique):
                question_id = random.randrange(1, 99999)
                if(question_id not in conn.execute('SELECT question_id FROM Questions')):
                    unique = True            
            
            # question entry
            self.client_socket.send( ('Enter a question').encode() )
            question = self.client_socket.recv(1024).decode()
            # echo entry
            self.client_socket.send( ('You entered:' + question).encode() )
                            
            # question verification (verification loop control)
            self.client_socket.send( ('Add this question to the interview? Y/N').encode() )
            verify = self.client_socket.recv(1024).decode()
            
            # Y: link question to interview (terminate loop)
            if verify.upper() == 'Y':

                # add question to database
                db.add_question(conn, question_id, interview_id, question)
                self.client_socket.send( ('Question saved! ID:').encode() )
                self.client_socket.send( str(question_id).encode() )
                print('Question ID:', question_id)
            
            # N: re-enter question (repeat loop)
            elif verify.upper() == 'N':
                continue

            # invalid (error msg)
            else:
                self.client_socket.send( ('Error: Please answer with Y or N').encode() )
                    
            ## interview progression (interview creation loop control) ##
            self.client_socket.send( ('Would you like to add another question? Y/N').encode() )
            response = self.client_socket.recv(1024).decode()
            
            # N: submit interview to database (terminate loop)
            if response.upper() == 'N':
                # confirmation message
                self.client_socket.send( ('Interview creation finished! ID:').encode() )
                self.client_socket.send( str(interview_id).encode() )
                print('Interview ID:', interview_id)
                break
            # Y: continue adding questions (repeat loop)
            elif response.upper() == 'Y':
                continue
            # invalid response (error msg)
            else:
                self.client_socket.send( ('Error.').encode() )
        
        ## post-creation display ##
        
        # TODO: retrieve and display name and description
        
        # TODO: retrieve and display questions
                
        # END create_interview: go back to Lawyer Options
        
        # remove pass when code is complete
        #pass
    
    # ===========================================================================
    #             LAWYER: INTERVIEW ASSIGNMENT   
    # Status: Incomplete 
    # 
    # Precondition(s): 
    # - completed interview
    # - interviewee exists
    #
    # Postcondition:
    # - interviewee can access interview
    #
    # TO DO
    # - encrypt/decrypt messages
    # - add database interactions:
    #   - assign interview to interviewee Inbox 
    # - finalize interview assignment design (e.g. single or multiple assignment?)
    # =============================================================================
    def assign_interview(self):
        
        # < followup on interview creation or unique menu? >
        self.client_socket.send( ('Interview Assignment').encode( ))

        #Recieves a username from client
        User_Search = self.client_socket.recv(1024).decode() # "Enter the username of the interviewee:"

        ###CHECK DATABASE FOR###
        # import sqlite3 first
        conn= sqlite3.connect( 'interview.db' )
        #conn.row_factory = sqlite3.Row
        User_Row = conn.execute("SELECT user_id, user_name FROM Users WHERE user_name = ?", (User_Search,)).fetchone() 

        #if no existing user
        while User_Row == None: #invalid user
            self.client_socket.send( ('User does not exist, try again.').encode() )
            if User_Search == 'quit':
                return
            User_Search = self.client_socket.recv(1024).decode()
            conn.row_factory = sqlite3.Row
            User_Row = conn.execute("SELECT user_id, user_name FROM Users WHERE user_name = ?", (User_Search,)).fetchone() 
        
        self.client_socket.send( ('User exists').encode() )#user_conf
        User_Found = User_Row[0]
        
        #else
        #Recieves a interview from client


        Interview_Search = self.client_socket.recv(1024).decode()

        ###CHECK DATABASE FOR INTERVIEW###
        #conn.row_factory = sqlite3.Row
        Interview_Row = conn.execute("SELECT interview_name FROM Interviews WHERE interview_name = ?", (Interview_Search,)).fetchone()


        #if no existing user
        while Interview_Row == None:
            self.client_socket.send( ('Interview does not exist, try again.').encode() )
            if Interview_Search == 'quit':
                return
            Interview_Search = self.client_socket.recv(1024).decode()
            conn.row_factory = sqlite3.Row
            Interview_Row = conn.execute("SELECT interview_name FROM Interviews WHERE interview_name = ?", (Interview_Search,)).fetchone() 
        Interview_Found = Interview_Row['interview_name']

        self.client_socket.send( ('Assigning Interview').encode() ) #interview_conf

        ###ADD INTERVIEW TO USER'S INBOX###

        self.client_socket.send( (Interview_Search + " has been assigned to " + User_Search + ".").encode() ) #interview_conf

        conn.close()
        pass
    
    # ===========================================================================
    #             LAWYER: REVIEW SUBMISSIONS  
    # Status: Incomplete
    # 
    # Precondition(s):
    # - assigned interview completed by interviewee
    # - interview recorded in database
    #
    # Postcondition: 
    # - can be viewed by Lawyer/Staff
    #
    # TO DO
    # - encrypt/decrypt messages
    # - add database interactions
    # - finalize interview review design 
    # =============================================================================
    def review_submissions(self):

        # interview review intro
        self.client_socket.send( ('Interview Inbox').encode() )
        
        # interview retrieval
        # < search criteria? name, id? >
        self.client_socket.send( ('').encode() )
        self.client_socket.recv(1024).decode()
        
        # < retrieve interview from database >
        # < send ID details >
        self.client_socket.send( ('').encode() )
        
        # < INTERVIEW QUESTIONS LOOP >
        
        pass
    
    # ===========================================================================
    #             LAWYER: MANAGE INTERVIEWS
    # Status: Incomplete (skeleton finished)
    # 
    # Precondition(s):
    # - Lawyer/Staff account session
    #
    # Postcondition: 
    # - interview edited in database, interview deleted from database, or
    #   return to main menu
    #
    # TO DO
    # - PROTOCOL: add database interactions
    # - ENCRYPTION: add redirect to main menu
    # - test/refine loop control
    # =============================================================================
    def manage_interviews(self):
        
        ## MANAGE_INTERVIEWS LOOP ##
        while(True):

            # options (manage_interviews loop control)
            self.client_socket.send( ('What would you like to do? (choose one)').encode() )
            self.client_socket.send( ('E: Edit/View an interview').encode() )
            self.client_socket.send( ('D: Delete an interview').encode() )
            self.client_socket.send( ('Q: Back to Lawyer Options').encode() )
            option = self.client_socket.recv(1024).decode()
            
            conn = splite3.connect('interview.db') #temporary database

            # E: edit interview (go through edit process then repeat loop)
            if option == 'E':
                # interview summary
                self.client_socket.send( ('Created Interviews:').encode() )

                # <PROTOCOL: generate interview list from database >
                cur = conn.execute("SELECT interview_id, interview_name from Interviews")
                curLen = len(cur)
                if (cur == None):
                    self.client_socket.send( ('No Interviews available').encode() )
                    conn.close()
                    return
                for row in cur:
                    print ("( ", row[0], " ) ", row[1] )

                # display <none> if none exist
                
                # interview selection <PROTOCOL: search by sequence number>
                self.client_socket.send( ('Select an interview to edit').encode() )

                interview_ind = int(self.client_socket.recv(1024).decode())

                #j
                

                # <PROTOCOL: 
                new_name = str(self.client_socket.recv(1024).decode()) #Enter the new name of the interview

                #    - ask for name change; if yes, make database changes
                cur.execute("UPDATE Interviews set interview_name = ? where interview_id =?",(new_name, interview_ind) )
                conn.commit()
                #    - generate loop for each question
                #    - ask for question edit; if yes, make database changes>


        
                self.client_socket.send( ('All changes saved.').encode() )


            # D: delete interview (go through delete process then repeat loop)
            elif option == 'D':
                
                # verification loop
                while(True):
                    
                    # interview summary
                    self.client_socket.send( ('Created Interviews:').encode() )
                    # <PROTOCOL: generate interview list from database >
                    cur = conn.execute("SELECT interview_id, interview_name from Interviews")
                    for row in cur:
                        print ("( ", row[0], " ) ", row[1])

                    # display <none> if none exist
                
                    # interview selection <PROTOCOL: search by sequence number>
                    self.client_socket.send( ('Select an interview to delete').encode() )
                    interview_ind = int(self.client_socket.recv(1024).decode())
                    
                    # loop control
                    self.client_socket.send('Remove <INTERVIEW NAME> from database? Y/N')
                    verify = self.client_socket.recv(1024)
                    
                    # Y: remove selection from database (terminate loop)
                    if verify == 'Y':
                        # <PROTOCOL: delete interview from database>
                        cur.execute("DELETE from Interviews where interview_id =?",(interview_ind,))
                        conn.commit()
                        
                        self.client_socket.send( ('<INTERVIEW NAME> removed.').encode() )
                        break
                    # N: make a different selection
                    elif verify == 'N':
                        continue
                    # invalid response
                    else:
                        self.client_socket.send('Invalid Input! Please answer with Y or N')

            # Q: return to main menu (terminate loop)
            elif option == 'Q':
                break

            # invalid response
            else:
                self.client_socket.send( ('Invalid Input!').encode() )

                        
        # END manage_interviews: return to Lawyer Options

            
        # remove pass when code is done
        conn.close()
        pass
        
    # ===========================================================================
    #             INTERVIEWEE: TAKE INTERVIEW   
    # Status: Incomplete (skeleton finished)
    # 
    # Precondition(s):
    # - interviewee account session
    # - interview linked to interviewee
    #
    # Postcondition: 
    # - answers linked to questions of interview in database
    #
    # TO DO
    # - PROTOCOL: add database interactions
    # - SYNC: test/refine loop control
    # =============================================================================
    def take_interview(self):    
            
        # interview review intro
        self.client_socket.send( ('Your available interviews:').encode() )
           
        # assigned interview list
        # <PROTOCOL: generate interviewee's interview list from database?>
        # display <none> if none exist
            
        # interview selection <PROTOCOL: search by sequence number?>
        self.client_socket.send( ('Select an interview to take').encode() )
        interview_sel = self.client_socket.recv(1024).decode()
        
        # <PROTOCOL: 
        #    - retrieve interview based on criteria
        #    - generate loop for each question
        #    - for each question, ask for answer, link it to question
        #    - add interview to review list>
        
        self.client_socket.send( ('Interview complete').encode() )
 
        # END take_interview: go back to Interviewee Options
        
        # remove pass when code is done
        pass
    
    def run(self):
    #greet and request username and password
        self.client_socket.send( ('Welcome to the Interview Portal').encode() )

        conn= sqlite3.connect( 'interview.db' )
        cur = conn.cursor()

        #Creating a new user
        response = str(self.client_socket.recv(1024).decode()) # User chooses to login or create a new account
        if (response == '2'):
            self._USER_NAME = str(self.client_socket.recv(1024).decode())
            self._USER_AUTH = int(self.client_socket.recv(1024).decode())
            cur.execute("INSERT INTO Users ( user_name, user_perms) VALUES ( ?, ?);", (self._USER_NAME, self._USER_AUTH))
            conn.commit()

        self._USER_NAME = str(self.client_socket.recv(1024).decode())
        self._USER_PW   = str(self.client_socket.recv(1024).decode())

        ##Authentication stuff
        ##
        ##
        ##
        #Searches database for username and password

        User_Row = conn.execute("SELECT user_name FROM Users WHERE user_name = ?", (self._USER_NAME,)).fetchone()
        conn.close()
     
        ##
        ##
        ##
        ##
        ##

        _LOGIN_STATUS = (User_Row != None)

        if _LOGIN_STATUS == True:
            self.client_socket.send( ('2').encode() )
            response = str(self.client_socket.recv(1024).decode())
            print(response)
            if response == '1':
                self.create_interview()
                return
            elif response == '2':
                self.review_submissions()
                
            elif response == '3':
                self.assign_interview()
                return
            elif response == '4':
                self.manage_interviews()
                return
            elif response == '4':
                self.take_interview()
                return
        else:
            self.client_socket.send( ("Invalid Username").encode() )

            self.terminate_session()
            return


        self.terminate_session()
         
