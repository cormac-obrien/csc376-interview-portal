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
    # - add database interactions
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
                    # < record question to database >
                    self.client_socket.send('Question added to interview.')
                    break
                # N: re-enter question (repeat loop)
                elif verify == 'N':
                    continue
                # invalid (error msg + repeat verification loop)
                else:
                    self.client_socket.send('Invalid Input!  Please answer with Y or N')
                    
            # interview progression (interview creation loop control)
            self.client_socket.send('Would you like to add another question? Y/N')
            response = self.client_socket.recv(1024)
            
            # N: submit interview to database (terminate loop)
            if response == 'N':
                # < interview added to database >
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
        self.client_socket.send('Q: Return to main menu')
        option = self.client_socket.recv(1024)
        
        if option == 'A':
            # < assignment function/process here >
            pass
        elif option == 'I':
            continue
        elif option == 'Q':
            # < redirect to main menu >
            break
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
    #             INTERVIEW Review   
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

        # interview creation intro
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
        
