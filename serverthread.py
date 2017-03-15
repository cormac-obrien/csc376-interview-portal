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
import bcrypt
import getpass
import ClientLogin
from loginauth import LoginAuthentication

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
    # Author(s):
    # - Architecture: LA 
    # - Testing/Optimization: PD
    # 
    # Status: Complete
    # 
    # Precondition: 
    # - Lawyer/Staff access
    # - create interview option selected
    #
    # Postcondition:
    # - interview recorded in database
    #
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
        #db.assign_interview(conn, interview_id, interview_user )
        #self.client_socket.send( (interview_name + " has been assigned to " + User_Search + ".").encode() ) #interview_conf
        conn= sqlite3.connect( 'interview.db' )
        questions = db.retrieve_questions(conn, interview_id)

        for question in questions:
            db.add_answer(conn, interview_user, question[0], None, interview_id)
            print('created answer space for question: ' + str(question[0]))

            #self.client_socket.send( ('(' + str(interview[0]) + ') ' + interview[1]).encode() )
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
        self.client_socket.send( ('Review Submissions').encode( ))

        #Receives a username from client
        User_Search = self.client_socket.recv(1024).decode() # "Enter the username of the interviewee:"

        ###CHECK DATABASE FOR USER###
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
        interview_ids = db.retrieve_interview_by_answer(conn, interview_user)
        for interview_id in interview_ids:
            interview_name = db.retrieve_interview_title(conn, interview_id[0])
            self.client_socket.send(("ID: " + str(interview_id[0]) + " Name: " + str(interview_name)).encode())
        #self.client_socket.send( str(interviews).encode() )
        #Receives a interview from client

        self.client_socket.send( ('end').encode() )


        interview_id = self.client_socket.recv(1024).decode()

        interview_name = ''
        while True:
            try:
                interview_name = db.retrieve_interview_title(conn, interview_id)
                break
            except TypeError:
                self.client_socket.send( ('Interview does not exist, try again.').encode() )
                if interview_name == 'quit':
                    return
                interview_id = self.client_socket.recv(1024).decode()       

        self.client_socket.send( ('Displaying Interview').encode() ) #interview_conf

        ###ADD INTERVIEW TO USER'S INBOX###

        conn= sqlite3.connect( 'interview.db' )
        questions = db.retrieve_questions(conn, interview_id)

        for question in questions:
            questionStr = str(question[4:])
            print('ind 1 = '+ questionStr)
            print('ind 0 = '+ str(question[0]))
            answer = str( db.retrieve_answer(conn, interview_user, str(question[0]) ))
            self.client_socket.send( ('Q: ' + questionStr + '\nA: ' + answer).encode() ) #interview_conf
        self.client_socket.send( ('End of Interview').encode() ) #interview_conf

        print('End of Interview')

    
    # ===========================================================================
    #             LAWYER: MANAGE INTERVIEWS
    # 
    # Author(s):
    # - Architecture: LA
    # - Testing/Optimization: TW
    #
    # Status: Complete
    #
    # Precondition(s):
    # - Lawyer/Staff account session
    #
    # Postcondition: 
    # - interview edited in database, interview deleted from database, or
    #   return to main menu
    #
    # =============================================================================
    def manage_interviews(self):
        
        ## MANAGE_INTERVIEWS LOOP ##
        while(True):
            
            # intro message
            self.client_socket.send( ('= Created Interview Management =').encode() )
            
            # options (manage_interviews loop control)
            self.client_socket.send( ('What would you like to do? (choose one)').encode() )
            self.client_socket.send( ('E: Edit/View an interview').encode() )
            self.client_socket.send( ('D: Delete an interview').encode() )
            self.client_socket.send( ('Q: Back to Options').encode() )
            # outgoing signal to terminate client display loop
            self.client_socket.send( ('end').encode() )
            
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
                if (len(interviews) == 0):
                    self.client_socket.send( ('No Interviews available!').encode() )
                    # outgoing signal to terminate client display loop
                    conn.close()
                # one or more interviews exist 
                else:
                    self.client_socket.send((str(interviews)).encode())
                # outgoing signal to terminate client display loop

                
                ## INTERVIEW SELECTION ##
                # outgoing selection request
                self.client_socket.send( ('Enter the interview ID of the created interview you wish to edit').encode() )
                # incoming selection input
                interview_id = self.client_socket.recv(1024).decode()
                
                ## EDITING OPTIONS ##
                while(True):
                    
                    ## OPTIONS DISPLAY ##
                    self.client_socket.send( ('What would you like to do?').encode() )
                    self.client_socket.send( ('N: Edit interview name').encode() )
                    self.client_socket.send( ('Q: Edit questions').encode() )
                    self.client_socket.send( ('R: Return to Created Interview Management options').encode() )
                    # outgoing signal to terminate client display loop
                    self.client_socket.send( ('end').encode() )
                    
                    # incoming edit option choice
                    edit_option = self.client_socket.recv(1024).decode()
                    
                    ## OPTIONS ##
                    # N: edit name 
                    if edit_option.upper() == 'N':
                        changing_name = True
                        while changing_name:
                            try:
                                # outgoing name change request
                                self.client_socket.send( ('Enter a new name').encode() )
                                # incoming name change input
                                new_name = str(self.client_socket.recv(1024).decode()) 
                                curs = conn.cursor()
                                curs.execute("UPDATE Interviews SET interview_name = ? WHERE interview_id =?",(new_name, interview_id) )
                                conn.commit()
                                self.client_socket.send(("Success").encode())
                                # outgoing name change confirmation
                                name_conf = db.retrieve_interview_title(conn, interview_id)
                                self.client_socket.send( ('Interview name has been successfully changed to: ' + name_conf).encode() )
                                changing_name = False

                            except:
                                error = "Error"
                                self.client_socket.send(error.encode())
                                self.client_socket.send(("Error occured. Please try again."))

                        
            
                    # Q: edit question
                    elif edit_option.upper() == 'Q':
                        
                        while(True):
                        
                            ## INTERVIEW QUESTIONS DISPLAY ##
                            questions = db.retrieve_questions(conn, interview_id)
                            # display example: 1) question text
                            self.client_socket.send( str(questions).encode() )
                            # outgoing signal to terminate client display loop
                            ## QUESTION EDITING ## 
                            # outgoing question selection request
                            self.client_socket.send( ('Enter the ID of the question you would like to edit').encode() )
                            # incoming sequence number input
                            
                            # retrieve question and display current text 
                            find_q = True
                            while find_q:
                                try:
                                    q_choice = int(self.client_socket.recv(1024).decode())
                                    q_text = db.retrieve_question(conn, q_choice)
                                    self.client_socket.send(("Found").encode())
                                    self.client_socket.send( (('Current question text: ' + str(q_text)).encode()))
                                    find_q = False
                                except:
                                    self.client_socket.send(("Error").encode())
                                    self.client_socket.send(("Invalid Question ID Number. Please try again.").encode())
                            # outgoing question change request
                            self.client_socket.send( ('Enter question change').encode() )
                            # incoming question change input
                            q_change = str(self.client_socket.recv(1024).decode())
                            
                            # update question
                            curs = conn.cursor()
                            curs.execute('UPDATE Questions SET question_text = ? WHERE question_interview = ? AND question_id = ?',
                                         (q_change, interview_id, q_choice))
                            conn.commit()
                            
                            ## CONFIRMATION ##
                            # outgoing question change confirmation
                            q_conf = curs.execute('SELECT question_text FROM Questions Where question_interview = ? AND question_id = ?',
                                                  (interview_id, q_choice)).fetchone()
                            conn.commit()
                            self.client_socket.send( ('Interview question has been successfully changed to: ' + str(q_conf)).encode() )
                            
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
                 
                
                    # no interviews exist
                    interviews = db.retrieve_interview_all(conn)
                
                    # no interviews exist
                    if (len(interviews) == 0):
                        self.client_socket.send( ('No Interviews available!').encode() )
                        # outgoing signal to terminate client display loop
                        conn.close()
                    # one or more interviews exist 
                    else:
                        self.client_socket.send((str(interviews)).encode())    # outgoing signal to terminate client display loop
                
                    ## INTERVIEW SELECTION ##
                    
                    # outgoing interview selection request
                    #valid_id = True
                    #while valid_id:
                    self.client_socket.send( ('Enter the ID of the interview you wish to delete').encode() )
                    interview_id = int(self.client_socket.recv(1024).decode())
                    
                    ## VERIFICATION LOOP CONTROL ##
                    name_conf = db.retrieve_interview_title(conn, interview_id)
                    # outgoing verify request
                    self.client_socket.send(('Remove ' + str(name_conf) + ' from database? Y/N').encode())
                    # incoming verify input
                    verify = str(self.client_socket.recv(1024).decode())
                    
                    # Y: remove interview from database (terminate loop)
                    if verify.upper() == 'Y':
                        
                        ## DELETE AND CONFIRM ##
                        db.delete_interview(conn, interview_id)
                        self.client_socket.send( (name_conf + ' removed.').encode() )
                        break
                    
                    # N: make a different selection
                    elif verify.upper() == 'N':
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
            
            # Take interview intro
            self.client_socket.send( ('Your available interviews:').encode() )

           # db connection
            conn = sqlite3.connect('interview.db')
            # try:
            #
            #     interview_ids = db.retrieve_interview_by_answer(conn, self._USER_ID)
            # except TypeError:
            #     self.client_socket.send( ('You have no assigned interviews.').encode() )


            #retrieve interviews using self object
            user_id = db.retrieve_user_by_name(conn, self._USER_NAME)

            interview_ids = db.retrieve_interview_by_answer(conn, user_id)
            # one or more interviews exist
            for interview_id in interview_ids:
                interview_name = db.retrieve_interview_title(conn, interview_id[0])
                self.client_socket.send(("ID: " + str(interview_id[0]) + " Name: " + str(interview_name)).encode())
            # outgoing signal to terminate client display loop
            self.client_socket.send( ('end').encode() )

           ## INTERVIEW SELECTION ##
            # outgoing selection request
            self.client_socket.send( ('Enter the interview ID you wish to take').encode() )
            # incoming selection input
            interview_id = int(self.client_socket.recv(1024).decode())

           # <PROTOCOL:
            #    - retrieve interview based on criteria
            questions = db.retrieve_questions(conn, interview_id)
            #    - generate loop for each question
            for question in questions:
                self.client_socket.send( ('(' + str(question[0]) + ') ' + question[4:]).encode() )

               #    - for each question, ask for answer, link it to question
                answer = str(self.client_socket.recv(1024).decode())

                answer_id = int(db.retrieve_answer_id_by_question(conn, user_id, question[0]))
                db.update_answer(conn, answer, answer_id)
            self.client_socket.send( ('end').encode() )



           #    - add interview to review list>

            self.client_socket.send( ('Interview complete').encode() )
            conn.close()
            
           # END take_interview: go back to Interviewee Options


    # ===========================================================================
    #             ADMIN: MANAGE USERS   
    # Status: complete (may neeed further testing)
    # 
    # Precondition(s):
    # - Users exist
    #
    # Postcondition: 
    # - 
    #
    # TO DO
    # -
    # - 
    # =============================================================================

    def manage_users(self):
        self.client_socket.send( ('Welcome to User Management').encode() )
        conn = sqlite3.connect('interview.db')
        while(True):
            option = self.client_socket.recv(1024).decode()
            if (option == '1'):
                users = str(db.retrieve_user_all(conn))
                self.client_socket.send((users).encode())
                check_user = self.client_socket.recv(1024).decode()
                print("check user" + check_user)
                user_id = ''
                user_conf= ''
                try:
                    user_id = db.retrieve_user_by_name(conn, check_user)
                    user_conf = check_user
                    self.client_socket.send( (user_conf).encode() )
                except TypeError:
                    user_conf = 'User does not exist'
                    self.client_socket.send( (user_conf).encode() )
                    break
                    

                #self.client_socket.send( (user_conf).encode() )

                new_auth = self.client_socket.recv(1024).decode()
                if (new_auth == 'Invalid Authorization Level'):
                    print(new_auth)
                    break
                print('Assigning new Authorization Level')
                db.update_user_auth(conn, user_id, new_auth)
                conf = ('User ' + check_user + ' has been reassigned an Authorization level')
                self.client_socket.send( (conf).encode() )
                break

            elif (option == '2'):
                users = str(db.retrieve_user_all(conn))
                self.client_socket.send((users).encode())
                check_user = self.client_socket.recv(1024).decode()
                user_id = ''
                user_conf= ''
                try:
                    user_id = str(db.retrieve_user_by_name(conn, check_user))
                    user_conf = check_user
                    self.client_socket.send( (user_conf).encode() )
                except TypeError:
                    user_conf = 'User does not exist'
                    self.client_socket.send( (user_conf).encode() )
                    break



                second_conf = self.client_socket.recv(1024).decode()
                response = ''
                if (second_conf.upper() == 'Y'):
                    db.delete_user(conn, user_id)
                    response = ('user ' + check_user + ' has been deleted')
                else:
                    response = ('Operation has been cancelled')
                
                self.client_socket.send( (response).encode() )
                break

            else:
                break
        print('Exiting User Management')
        return

    def checkpassword(self, password, hashedpw):

        if bcrypt.checkpw(password.encode('utf-8'), hashedpw.encode('utf-8')):
            return True
        else:
            return False

    
    def run(self):
    #greet and request username and password

        self.client_socket.send( ('Welcome to the Interview Portal').encode() )

        sqlFile = 'schema.sql'
        qry = open(sqlFile, 'r').read()
        conn= sqlite3.connect( 'interview.db' )
        cur = conn.cursor()
        cur.executescript(qry)
        new_USER_PW = LoginAuthentication.get_hashed_password("admin")
        cur.execute("INSERT OR IGNORE INTO Users ( user_name, user_password, user_perms) VALUES ( ?, ?, ?);",
                                ("sysadmin", new_USER_PW, 0))
                    
        conn.commit()

        #Creating a new user
        response = str(self.client_socket.recv(1024).decode()) # User chooses to login or create a new account
        if (response == '1'):
            checking_pass = True
            while (checking_pass):
                try:
                    self._USER_NAME = str(self.client_socket.recv(1024).decode())
                    self._USER_PW   = str(self.client_socket.recv(1024).decode())
                    cur.execute("SELECT * FROM Users WHERE user_name== ? ", (self._USER_NAME,))
                    conn.commit()
                    hashed_password = cur.fetchone()[2]
                    if (self.checkpassword(self._USER_PW, hashed_password)):
                        self.client_socket.send(("Logging In").encode())
                        self.client_socket.send(("Redirecting...").encode())
                        checking_pass = False
                    else:
                        self.client_socket.send(("Failed in else").encode())
                        self.client_socket.send(("Username or password did not match. Try again:").encode())
        
                except:
                    self.client_socket.send(("Failed").encode())
                    self.client_socket.send(("Username or password did not match. Try again:").encode())
        
        if (response == '2'):

            exists = True
            while exists:
                try:
                    self._USER_NAME = str(self.client_socket.recv(1024).decode())
                    #self._USER_AUTH = int(self.client_socket.recv(1024).decode())
                    self._USER_PW = str(self.client_socket.recv(1024).decode())
                    cur.execute("INSERT INTO Users ( user_name, user_password, user_perms) VALUES ( ?, ?, ?);",
                                (self._USER_NAME, self._USER_PW, 3))
                    conn.commit()
                    self.client_socket.send(("Succesful").encode())
                    self.client_socket.send(("Account created successfully").encode())
                    exists = False
                    pass
                except:
                    error = "Integrity Error"
                    self.client_socket.send((error).encode())
                    self.client_socket.send(("Username already exists. Please choose a different one.").encode())        
       


        User_Row = conn.execute("SELECT user_name FROM Users WHERE user_name = ?", (self._USER_NAME,)).fetchone()
        user_id = db.retrieve_user_by_name(conn, self._USER_NAME)
        cred = str(db.retrieve_user_auth(conn, user_id))
        conn.commit()
     
        ##
        ##
        ##
        ##
        ##

        _LOGIN_STATUS = (User_Row != None)


        if _LOGIN_STATUS == True:
            # CHANGE cred TO USER CREDENTIAL IDENTIFIER BELOW
            self.client_socket.send((cred).encode())
        
            while(True):
                response = str(self.client_socket.recv(1024).decode())
                print(response)
                if(cred == '0'):      #ADMIN
                    if response == '1':
                        self.create_interview()
                    elif response == '2':
                        self.review_submissions()
                    elif response == '3':
                        self.assign_interview()
                    elif response == '4':
                        self.manage_users()
                    elif response == '5':
                        self.manage_interviews()
                    elif response.upper() == 'Q':
                        break
                elif(cred == '1'):    #LAWYER
                    if response == '1':
                        self.create_interview()
                    elif response == '2':
                        self.review_submissions()
                    elif response == '3':
                        self.assign_interview()
                    elif response == '4':
                        self.manage_interviews()
                    elif response.upper() == 'Q':
                        return
                elif(cred == '3'):    #INTERVIEWEE
                    if response == '1':
                            self.take_interview()
                    elif response.upper() == 'Q':
                        break
        else:
            self.client_socket.send( ("Invalid Username").encode() )

            self.terminate_session()
            return


        self.terminate_session()
         
