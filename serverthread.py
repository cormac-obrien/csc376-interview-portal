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
