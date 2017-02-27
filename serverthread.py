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
    # - question details recorded in database
    #
    # TO DO
    # - encrypt/decrypt messages
    # - add database interactions
    # - finalize interview structure (e.g. multiple answers or single answers?)
    # =========================================================================
    def create_interview(self):
        
        # interview creation intro
        self.client_socket.send('Interview Creation')
        
        # interview name entry
        self.client_socket.send('Enter a name for the interview')
        name = self.client_socket.recv(1024)
        
        # < name recorded here >
        
        # QUESTION CREATION LOOP
        while(True):
            
            # question entry
            self.client_socket.send('Enter a question')
            print('You entered:')
            print(self.client_socket.recv(1024))
            
            # ANSWER CREATION LOOP
            while(True):
                
                #answer entry
                self.client_socket.send('Enter the answer to the question')
                print(self.client_socket.recv(1024))
                
                # < answer recorded here >
                
                
                # < multiple answers? >
                
                break
                
            # SUBSEQUENT QUESTIONS LOOP
            self.client_socket.send('Would you like to add another question?')
            response = self.client_socket.recv(1024)
            
            # N - interview complete
            if response == 'N':
                
                # < interview finalized here >
                
                break
            # Y continue adding questions (repeat loop)
            elif response == 'Y':
                continue
            # invalid response
            else:
                self.client_socket.send('Invalid Response!')
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
        
