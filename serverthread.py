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
        db.create_interview(conn, interview_id, name, desc, None)

        ## INTERVIEW CREATION LOOP ##
        sequence_num = 1; # question number
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
                db.add_question(conn, question_id, interview_id, question, sequence_num)
                # increment question number
                sequence_num += 1 
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
    
    # ===========================================================================
    #             LAWYER: INTERVIEW ASSIGNMENT   
    # Status: Complete
    # 
    # Precondition(s): 
    # - interview exists
    # - interviewee exists
    #
    # Postcondition:
    # - interviewee can access interview
    #
    # =============================================================================
    def assign_interview(self):
        
        # intro message
        self.client_socket.send( ('Interview Assignment').encode( ))

        #Receives a username from client
        User_Search = self.client_socket.recv(1024).decode() # "Enter the username of the interviewee:"

        ###CHECK DATABASE FOR###
        # import sqlite3 first
        
        conn= sqlite3.connect( 'interview.db' )
        interview_user = ''
        while True:
            try:
                interview_user = db.retrieve_user_by_name(conn, User_Search)
                break
            except TypeError:
                #if no existing user
                self.client_socket.send( ('User does not exist, try again.').encode() )
                if interview_user == 'quit':
                    return
                User_Search = self.client_socket.recv(1024).decode()
                #interview_user = db.retrieve_user_by_name(conn, User_Search)

        self.client_socket.send( ('User exists').encode() )#user_conf
        #User_Found = User_Row[0]
        
        #else
        #display list of available interviews
        conn= sqlite3.connect( 'interview.db' )
        interviews = db.retrieve_interview_all(conn)
        for interview in interviews:
             self.client_socket.send( ('(' + str(interview[0]) + ') ' + interview[1]).encode() )
        #Receives a interview from client

        self.client_socket.send( ('end').encode() )


        interview_id = self.client_socket.recv(1024).decode()

        
        while True:
            try:
                interview_name = db.retrieve_interview_title(conn, interview_id)
                break
            except TypeError:
                self.client_socket.send( ('Interview does not exist, try again.').encode() )
                if interview_name == 'quit':
                    return
                interview_id = self.client_socket.recv(1024).decode()       

        self.client_socket.send( ('Assigning Interview').encode() ) #interview_conf

        ###ADD INTERVIEW TO USER'S INBOX###
        db.assign_interview(conn, interview_id, interview_user )
        self.client_socket.send( (interview_name + " has been assigned to " + User_Search + ".").encode() ) #interview_conf

        conn.close()
        return
    
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
            
            # intro message
            self.client_socket.send( ('Created Interview Management').encode() )
            
            # options (manage_interviews loop control)
            self.client_socket.send( ('What would you like to do? (choose one)').encode() )
            self.client_socket.send( ('E: Edit/View an interview').encode() )
            self.client_socket.send( ('D: Delete an interview').encode() )
            self.client_socket.send( ('Q: Back to Lawyer Options').encode() )
            # incoming option choice
            option = self.client_socket.recv(1024).decode()
            
            # db connection
            conn = sqlite3.connect('interview.db') 

            # E: edit interview (go through edit process then repeat loop)
            if option.upper() == 'E':
                
                ## INTERVIEW SUMMARY ##
                self.client_socket.send( ('Created Interviews:').encode() )
                interviews = db.retrieve_interview_all(conn)
                
                # no interviews exist
                if (len(interview) == 0):
                    self.client_socket.send( ('No Interviews available!').encode() )
                    conn.close()
                    return
                # one or more interviews exist 
                for interview in interviews:
                    self.client_socket.send( ('(' + str(interview[0]) + ') ' + interview[1]).encode() )
                # outgoing signal to terminate client display loop
                self.client_socket.send( ('end').encode() )
                
                ## INTERVIEW SELECTION ##
                # outgoing selection request
                self.client_socket.send( ('Enter the interview ID of the created interview you wish to edit').encode() )
                # incoming selection input
                interview_id = int(self.client_socket.recv(1024).decode())
                
                ## EDITING OPTIONS ##
                while(True):
                    
                    ## OPTIONS DISPLAY ##
                    self.client_socket.send( ('What changes would you like to make?').encode() )
                    self.client_socket.send( ('N: Edit interview name').encode() )
                    self.client_socket.send( ('Q: Edit questions').encode() )
                    self.client_socket.send( ('R: Return to Created Interview Management options').encode() )
                    edit_option = self.client_socket.recv(1024).decode()
                    
                    ## OPTIONS ##
                    # N: edit name
                    if edit_option.upper() == 'N':
                        
                        # outgoing name change request
                        self.client_socket.send( ('Enter a new name').encode() )
                        # incoming name change input
                        new_name = str(self.client_socket.recv(1024).decode()) 
                        curs = conn.cursor()
                        curs.execute("UPDATE Interviews SET interview_name = ? WHERE interview_id =?",(new_name, interview_id) )
                        conn.commit()
                        
                        # outgoing name change confirmation
                        name_conf = retrieve_interview_title(conn, interview_id)
                        self.client_socket.send( ('Interview name has been successfully changed to: ' + name_conf).encode() )
            
                    # Q: edit question
                    elif edit_option.upper() == 'Q':
                        
                        while(True):
                        
                            ## INTERVIEW QUESTIONS DISPLAY ##
                            questions = retrieve_questions(conn, interview_id)
                            for question in questions:
                                # display: question number) question text
                                self.client_socket.send( (str(question[1]) + ') ' + str(question[0])).encode() )
                            # outgoing signal to terminate client display loop
                            self.client_socket.send( ('end').encode() )
                           
                            ## QUESTION EDITING ## 
                            # outgoing question selection request
                            self.client_socket.send( ('Enter the number of the question you would like to edit').encode() )
                            # incoming sequence number input
                            q_choice = int(self.client_socket.recv(1024).decode())
                            
                            # retrieve question and display current text 
                            curs = conn.cursor()
                            q_edit = curs.execute('SELECT question_text WHERE question_interview = ? AND question_sequence = ?', 
                                                  (interview_id, q_choice))
                            conn.commit()
                            self.client_socket.send( ('Current question text: ' + str(q_edit[0])).encode() )
                            
                            # outgoing question change request
                            self.client_socket.send( ('Enter question change').encode() )
                            # incoming question change input
                            q_change = str(self.client_socket.recv(1024).decode())
                            
                            # update question
                            curs = conn.cursor()
                            curs.execute('UPDATE Questions SET question_text = ? WHERE question_interview = ? AND question_sequence = ?',
                                         (q_change, interview_id, q_choice))
                            conn.commit()
                            
                            ## CONFIRMATION ##
                            # outgoing question change confirmation
                            q_conf = curs.execute('SELECT question_text FROM Questions Where question_interview = ? AND question_sequence = ?',
                                                  (interview_id, q_choice))
                            conn.commit()
                            self.client_socket.send( ('Interview name has been successfully changed to: ' + q_conf).encode() )
                            
                            ## LOOP CONTROL ##
                            self.client_socket.send( ('Would you like to edit another question? Y/N').encode() )
                            choice = str(self.client_socket.recv(1024).decode())
                            
                            # Y: add more questions (repeat loop)
                            if choice.upper() == 'Y':
                                continue
                            # N: return to Editing Options
                            elif choice.upper() == 'N':
                                break
                            # invalid response
                            else:
                                self.client_socket.send( ('Invalid Input!').encode() )
                                
                    # R: return to manage interview options
                    elif edit_option.upper() == 'R':
                        break
                    
                    # invalid response
                    else:
                        self.client_socket.send( ('Invalid Input!').encode() )

            # D: delete interview (go through delete process then repeat loop)
            elif option.upper() == 'D':
                
                # verification loop
                while(True):
                    
                    ## INTERVIEW SUMMARY ##
                    self.client_socket.send( ('Created Interviews:').encode() )
                    interviews = db.retrieve_interview_all(conn)
                
                    # no interviews exist
                    if (len(interview) == 0):
                        self.client_socket.send( ('No Interviews available!').encode() )
                        conn.close()
                        return
                    # one or more interviews exist 
                    for interview in interviews:
                        self.client_socket.send( ('(' + str(interview[0]) + ') ' + interview[1]).encode() )
                    # outgoing signal to terminate client display loop
                    self.client_socket.send( ('end').encode() )
                
                    ## INTERVIEW SELECTION ##
                    
                    # outgoing interview selection request
                    self.client_socket.send( ('Enter the ID of the interview you wish to delete').encode() )
                    interview_id = int(self.client_socket.recv(1024).decode())
                    
                    ## VERIFICATION LOOP CONTROL ##
                    name_conf = retrieve_interview_title(conn, interview_id)
                    self.client_socket.send('Remove ' + name_conf + ' from database? Y/N')
                    verify = str(self.client_socket.recv(1024))
                    
                    # Y: remove interview from database (terminate loop)
                    if verify == 'Y':
                        
                        ## DELETE AND CONFIRM ##
                        delete_interview(conn, interview_id)
                        self.client_socket.send( (name_conf + ' removed.').encode() )
                        break
                    
                    # N: make a different selection
                    elif verify == 'N':
                        continue
                    
                    # invalid response
                    else:
                        self.client_socket.send('Invalid Input! Please answer with Y or N')

            # Q: return to main menu (terminate loop)
            elif option.upper() == 'Q':
                break

            # invalid response
            else:
                self.client_socket.send( ('Invalid Input!').encode() )

        # END manage_interviews: return to Lawyer Options
        conn.close()
        return
        
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
            cred = '2'
            # CHANGE cred TO USER CREDENTIAL IDENTIFIER BELOW
            self.client_socket.send( (cred).encode() )
        
        while(True):
            response = str(self.client_socket.recv(1024).decode())
            print(response)
            if(cred == '1'):    #INTERVIEWEE
                if response == '1':
                    self.take_interview()
                elif response.upper() == 'Q':
                    break
            elif(cred == '2'):    #LAWYER
                if response == '1':
                    self.create_interview()
                elif response == '2':
                    self.review_submissions()
                elif response == '3':
                    self.assign_interview()
                elif response.upper() == 'Q':
                    return
            elif(cred == '3'):      #ADMIN
                if response == '1':
                    self.create_interview()
                elif response == '2':
                    self.review_submissions()
                elif response == '3':
                    self.assign_interview()
                elif response.upper() == 'Q':
                    return
        else:
            self.client_socket.send( ("Invalid Username").encode() )

            self.terminate_session()
            return


        self.terminate_session()
         
