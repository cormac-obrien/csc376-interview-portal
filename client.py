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
    client_socket.close()
    print('Server socket closed')
    return

def adminMenu():
    print("What would you like to do?")
    print("(1) create interview")
    print("(2) review interview")
    print("(3) assign interview")
    print("(4) List users")
    print("(q) Log out and exit")

    response = str(input(" > "))

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
            print()
            terminate_session()
            if (len(response) != 0): print(response)
            sys.stdout.flush()
            answer_string = str(input(" > "))
            answer_string = enc.encrypt(answer_string)
            client_socket.send(answer_string)
            response = client_socket.recv(1024)
            response = enc.decrypt(response)



def validate(loggedInAs):
    # KH -- EXCISED PER LICENSING RESTRICTION
    pass



if __name__ == "__main__":
    import sys
    import socket

    argc = len(sys.argv)

    if (argc != 3):
        _HOST = str(input("Enter HOST name: "))
        _PORT = int(input("Enter PORT number: "))
    else:
        _HOST = str(sys.argv[1])
        _PORT = int(sys.argv[2])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((_HOST, _PORT))

    #Server greets client
    greeting_msg = client_socket.recv(1024) 
    greeting_msg = (greeting_msg).decode()
    print(greeting_msg)

    #Prompt For Password and Username
    USER_NAME = str(input("Username: "))
    client_socket.send((USER_NAME).encode())
    USER_PW   = str(input("Password: "))
    client_socket.send((USER_PW).encode())

    confirmation= str(client_socket.recv(1024).decode()) # confirms credentials
    print(confirmation)                             #print credentials
    try:
        cred = int(confirmation)
        
    except ValueError:
        terminate_session()
        sys.exit()
        

    if cred == 1:
        print("interviewee")
        #take interview
    elif cred == 2:
        print("lawyer")
        #admin_interface
    elif cred == 3:
        print("other?")
        #review_answers

    terminate_session()
    print("Logging Out...")
