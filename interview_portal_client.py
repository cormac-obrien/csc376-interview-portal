# Copyright 2016. DePaul University. All rights reserved. 
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.

from interview_error import CredentialsException

def terminate_session():
    print('Terminating connection to server')
    for i in range(0,10):
        print('.', end = '')
        sys.stdout.flush()
        time.sleep(0.1)
    client_socket.close()
    print('Server socket closed')
    return

def adminMenu():
    for i in range(0,6):
        message = client_socket.recv(1024)
        message = enc.decrypt(message)
        if (len(message) != 0): print(message)
        sys.stdout.flush()
        message = ''

    answer_string = str(input(" > "))
    answer_string = enc.encrypt(answer_string)
    client_socket.send(answer_string)
    response = client_socket.recv(1024)
    response = enc.decrypt(response)

    while True:
        if response == '1':
            createInterview()
            break
        elif response == '2':
            reviewInterview()
            break
        elif response == '3':
            assignInterview()
            break
        elif response == '4':
            listUsers()
            break
        else:
            if (len(response) != 0): print(response)
            sys.stdout.flush()
            answer_string = str(input(" > "))
            answer_string = enc.encrypt(answer_string)
            client_socket.send(answer_string)
            response = client_socket.recv(1024)
            response = enc.decrypt(response)

def listUsers():
    message = client_socket.recv(1024)
    message = enc.decrypt(message)
    if (len(message) != 0): print(message)
    sys.stdout.flush()
    message = ''

    message = client_socket.recv(1024)
    message = enc.decrypt(message)
    while (message != 'End of List'):
        if (len(message) != 0): print('User : ' + message)
        sys.stdout.flush()
        message = ''
        message = client_socket.recv(1024)
        message = enc.decrypt(message)


def reviewInterview():
    for i in range(0,2):
        message = client_socket.recv(1024)
        message = enc.decrypt(message)
        if (len(message) != 0): print(message)
        sys.stdout.flush()
        message = ''
    answer_string = str(input(" > "))
    answer_string = enc.encrypt(answer_string)
    client_socket.send(answer_string)

    message = client_socket.recv(1024)
    message = enc.decrypt(message)
    if (len(message) != 0): print('Interview Name : '+ message)
    sys.stdout.flush()
    message = ''
    message = client_socket.recv(1024)
    message = enc.decrypt(message)
    while (message != 'End of Interview'):
        if (len(message) != 0): print('Question : ' + message)
        sys.stdout.flush()
        message = ''
        message = client_socket.recv(1024)
        message = enc.decrypt(message)
        if (len(message) != 0): print('Answer : ' + message)
        sys.stdout.flush()
        message = ''
        message = client_socket.recv(1024)
        message = enc.decrypt(message)

def credentials():
    prompt=client_socket.recv(1024)
    prompt = enc.decrypt(prompt)
    answer_string=str(input(prompt))
    answer_string = enc.encrypt(answer_string)
    client_socket.send(answer_string)
    prompt=client_socket.recv(1024)
    prompt = enc.decrypt(prompt)
    answer_string=str(input(prompt))
    answer_string = enc.encrypt(answer_string)
    client_socket.send(answer_string)
#string printing loop that prints question from server and returns string answer
def startinterview():
    greeting = client_socket.recv(1024)
    greeting = enc.decrypt(greeting)
    if (len(greeting) != 0): print(greeting)
    interview_string=client_socket.recv(1024)
    interview_string = enc.decrypt(interview_string)

    while (interview_string !="End of Interview"):#keyword could be swapped out for anything
        print(interview_string)
        answer_string=str(input("Answer: "))
        answer_string = enc.encrypt(answer_string)
        client_socket.send(answer_string)
        interview_string = client_socket.recv(1024)
        interview_string = enc.decrypt(interview_string)
    print("End of Interview")

def validate(loggedInAs):
	# KH -- EXCISED PER LICENSING RESTRICTION

def createInterview():
    greeting = client_socket.recv(1024)
    greeting = enc.decrypt(greeting)
    if (len(greeting) != 0): print(greeting)
    sys.stdout.flush()
    interview_string = client_socket.recv(1024)
    interview_string = enc.decrypt(interview_string)
    if (len(greeting) != 0): print(interview_string)
    sys.stdout.flush()
    
    while (interview_string!="End of Interview"):
        answer_string=str(input(" > "))
        answer_string = enc.encrypt(answer_string)
        client_socket.send(answer_string)
        interview_string = client_socket.recv(1024)
        interview_string = enc.decrypt(interview_string)
        print(interview_string)

def assignInterview():
    greeting = client_socket.recv(1024)
    greeting = enc.decrypt(greeting)
    if (len(greeting) != 0): print(greeting)
    sys.stdout.flush()
    interview_string = client_socket.recv(1024)
    interview_string = enc.decrypt(interview_string)
    if (len(greeting) != 0): print(interview_string)
    sys.stdout.flush()
    
    while (interview_string!="End of assigning process"):
        if(interview_string == "Welcome to the interview assigner!"):
            interview_string = client_socket.recv(1024)
            interview_string = enc.decrypt(interview_string)
            if (len(greeting) != 0): print(interview_string)
            sys.stdout.flush()
        else:    
            answer_string=str(input(" > "))
            answer_string = enc.encrypt(answer_string)
            client_socket.send(answer_string)
            interview_string = client_socket.recv(1024)
            interview_string = enc.decrypt(interview_string)
            print(interview_string)
        
def key_exchange():
    dif = diffieHellman()
    client_socket.send(str(dif.publicKey).encode())
    other_key = client_socket.recv(2048).decode()
    other_key = int(other_key)
    key = dif.genKey(other_key)
    return key

if __name__ == "__main__":
    import sys
    import socket
    import time
    from argparse import ArgumentParser
    from DiffieHellman import diffieHellman
    from encrypt import Encrypt
    
    parser = ArgumentParser(description = 'CSC 376 Final Project : Interview Portal')
    parser.add_argument('host', type = str, help = 'Host Address of the Server')
    parser.add_argument('port', type = int, help = 'Port used to connect to Server')
    args = parser.parse_args()
    _HOST = socket.gethostbyname(args.host)
    _PORT = args.port
    #_HOST = 'localhost'
    #_PORT = 55555
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((_HOST, _PORT))
    key = key_exchange()
    enc = Encrypt(key)
    in_data = client_socket.recv(1024)
    in_data = enc.decrypt(in_data)
    print(in_data)
    credentials()
    loggedInAs = client_socket.recv(1024)
    loggedInAs = enc.decrypt(loggedInAs)
    if (validate(loggedInAs)):
        if (loggedInAs == "Interviewee"):
            startinterview()
        elif (loggedInAs == "Lawyer"):
            adminMenu()
        elif (loggedInAs == "System Admin"):
            adminMenu()
        elif (loggedInAs == "Legal Aide"):
            reviewInterview()    
    print("Logging Out...")
