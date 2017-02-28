# Copyright 2016. DePaul University. All rights reserved. 
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.

import sys
import threading
import socket

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

    def run(self):
        #greet and request username and password
        self.client_socket.send(('Greetings to the Interview Portal').encode())

        #client_socket.send(encode("Enter Username"))
        self._USER_NAME = str(self.client_socket.recv(1024).decode())
        #client_socket.send(encode("Enter Password"))
        self._USER_PW  = str(self.client_socket.recv(1024).decode())

        ##Authentication stuff
        ##
        ##
        _LOGIN_STATUS = (self._USER_NAME == self._USER_PW)

        #_LOGIN_STATUS = self.validate()
       
        if _LOGIN_STATUS == True:
            self.client_socket.send(('2').encode())
        else:
            self.client_socket.send(("Invalid Username").encode())

            self.terminate_session()
            return

    
        self.terminate_session()
     
      
    # =========================================================================
    #             INTERVIEW CREATION   
    # Status: Incomplete
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
    # - ENCRYPTION: add redirect to main menu
    # - test/refine loop control
    # =========================================================================
    def create_interview(self):
        
        # interview creation intro
        self.client_socket.send('Interview Creation')
        
        # interview name entry
        self.client_socket.send('Enter a name for the interview')
        name = self.client_socket.recv(1024)
        
        # < name recorded here >
        
        # INTERVIEW CREATION LOOP
        while(True):
            
            # verification loop
            while(True):            
                
                # question entry
                self.client_socket.send('Enter a question')
                print('You entered:')
                print(self.client_socket.recv(1024))
                
                # question verification (verification loop control)
                self.client_socket.send('Add this question to the interview? Y/N')
                verify = self.client_socket.recv(1024)
                
                # Y: link question to interview (terminate loop)
                if verify == 'Y':
                    # <PROTOCOL: record question to database >
                    self.client_socket.send('Question added to interview.')
                    break
                # N: re-enter question (repeat loop)
                elif verify == 'N':
                    continue
                # invalid (error msg)
                else:
                    self.client_socket.send('Invalid Input!  Please answer with Y or N')
                    
            # interview progression (interview creation loop control)
            self.client_socket.send('Would you like to add another question? Y/N')
            response = self.client_socket.recv(1024)
            
            # N: submit interview to database (terminate loop)
            if response == 'N':
                # <PROTOCOL: interview added to database >
                self.client_socket.send('Interview added to database.')
                break
            # Y: continue adding questions (repeat loop)
            elif response == 'Y':
                continue
            # invalid response (error msg)
            else:
                self.client_socket.send('Invalid Response!')
        
        # post-interview completion options
        self.client_socket.send('What would you like to do now? (choose one)')
        self.client_socket.send('A: Assign recently completed interview to interviewee(s)')
        self.client_socket.send('I: Create another interview')        
        self.client_socket.send('Q: Log out and return to main menu')
        option = self.client_socket.recv(1024)
        
        # A: assign interview (terminate loop)
        if option == 'A':
            # <PROTOCOL: assignment function/process here >
            break
        # I: create another interview (repeat loop)
        elif option == 'I':
            continue
        # Q: return to main menu (terminate loop)
        elif option == 'Q':
            # <ENCRYPTION: redirect to main menu >
            break
        # invalid response (error msg)
        else:
            self.client_socket.send('Invalid Response!')   
        
        # remove pass when code is complete
        pass
    
    # ===========================================================================
    #             INTERVIEW ASSIGNMENT   
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
    # - add database interactions
    # - finalize interview assignment design (e.g. single or multiple assignment?)
    # =============================================================================
    def assign_interview(self):
        
        # < followup on interview creation or unique menu? >
        
        pass
    
    # ===========================================================================
    #             INTERVIEW REVIEW  
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
    def review_interview(self):

        # interview review intro
        self.client_socket.send('Interview Inbox')
        
        # interview retrieval
        # < search criteria? name, id? >
        self.client_socket.send('')
        self.client_socket.recv(1024)
        
        # < retrieve interview from database >
        # < send ID details >
        self.client_socket.send()
        
        # < INTERVIEW QUESTIONS LOOP >
        
        pass
        
    # ===========================================================================
    #             TAKE INTERVIEW   
    # Status: Incomplete
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
    # - ENCRYPTION: add redirect to main menu
    # - test/refine loop control
    # =============================================================================
    def take_interview(self):
        
        # INTERVIEW LOOP
        while(True):
            
            # interview review intro
            self.client_socket.send('Your available interviews:')
            # <PROTOCOL: generate interviewee's interview list from database >
            # display <none> if none exist
            
            # interview selection <PROTOCOL: search criteria?>
            self.client_socket.send('Select an interview to take')
            self.client_socket.recv(1024)
        
            # <PROTOCOL: 
            #    - retrieve interview based on criteria
            #    - generate loop for each question
            #    - for each question, ask for answer, link it to question
            #    - add interview to review list>
        
            self.client_socket.send('Interview complete')
            
            # post-interview options (interview loop control)
            self.client_socket.send('What would you like to do now? (choose one)')
            self.client_socket.send('I: Take another interview')
            self.client_socket.send('Q: Log out and return to main menu')
            option = self.client_socket.recv(1024)
            
            # I: take another interview (repeat loop)
            if option == 'I':
                continue
            # Q: return to main menu (terminate loop)
            elif option == 'Q':
                # <ENCRYPTION: redirect to main menu>
                break
            # invalid response
            else:
                self.client_socket.send('Invalid Input!')
        
        # remove pass when code is done
        pass
    
    # ===========================================================================
    #             MANAGE INTERVIEW   (extra feature)
    # Status: Incomplete
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
    def manage_interview(self):
        
        # EDIT INTERVIEW LOOP
        while(True):

            # edit options (edit interview loop control)
            self.client_socket.send('What would you like to do? (choose one)')
            self.client_socket.send('E: Edit/View an interview')
            self.client_socket.send('D: Delete an interview')
            self.client_socket.send('Q: Log out and return to main menu')
            option = self.client_socket.recv(1024)
            
            # E: edit interview (go through edit process then repeat loop)
            if option == 'E':
                # interview summary
                self.client_socket.send('Created Interviews:')
                # <PROTOCOL: generate interview list from database >
                # display <none> if none exist
                
                # interview selection <PROTOCOL: search criteria?>
                self.client_socket.send('Select an interview to edit')
                self.client_socket.recv(1024)
        
                # <PROTOCOL: 
                #    - retrieve interview based on criteria
                #    - ask for name change; if yes, make database changes
                #    - generate loop for each question
                #    - ask for question edit; if yes, make database changes>
        
                self.client_socket.send('All changes saved.')
            # D: delete interview (go through delete process then repeat loop)
            elif option == 'D':
                # interview summary
                self.client_socket.send('Created Interviews:')
                # <PROTOCOL: generate interview list from database >
                # display <none> if none exist
                
                # interview selection <PROTOCOL: search criteria?>
                self.client_socket.send('Select an interview to delete')
                self.client_socket.recv(1024)
        
                # <PROTOCOL: delete interview from database>
                self.client_socket.send('Interview removed.')
            # Q: return to main menu (terminate loop)
            elif option == 'Q':
                # <ENCRYPTION: redirect to main menu>
                break
            # invalid response
            else:
                self.client_socket.send('Invalid Input!')
                        
        # remove pass when code is done
        pass