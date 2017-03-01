# Copyright 2016. DePaul University. All rights reserved. 
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.

#from interview_error import CredentialsException

def terminate_session():
    print('Terminating connection to server')
    for i in range(0,10):
        print('.', end = '')
        sys.stdout.flush()
    ssl_socket.close()
    print('Server socket closed')
    return

def adminMenu(ssl_socket):
    print("What would you like to do?")
    print("(1) create interview")
    print("(2) review interview")
    print("(3) assign interview")
    print("(4) List users")
    print("(q) Log out and exit")

    response = str(input(" > "))

    ssl_socket.send((response).encode())

    confirmation = ssl_socket.recv(1024).decode()
    print(confirmation)
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
            #print()
            #terminate_session()
            #if (len(response) != 0): print(response)
            sys.stdout.flush()
            return
            #answer_string = str(input(" > "))
            #answer_string = enc.encrypt(answer_string)
            #ssl_socket.send(answer_string)
            #response = ssl_socket.recv(1024)
            #response = enc.decrypt(response)


def createInterview():
	pass
def reviewInterview():
	pass

       
# ===========================================================================
#             INTERVIEW ASSIGNMENT   
# Status: Incomplete
# 
# Precondition(s): 
# - interview exists
# - interviewee exists
#
# Postcondition:
# - interviewee can access interview
#
# TO DO
# - encrypt/decrypt messages
# - finalize interview assignment design (e.g. single or multiple assignment?)
# =============================================================================

def assignInterview():

	# Get name of Interviewee
	print("Enter the username of the interviewee:")
	user = str(input(" > "))

	#Confirms that the interviewee exists

	ssl_socket.send(( user ).encode()) 									#User_Search
	user_conf = ssl_socket.recv(1024).decode()

	#if no existing user
	while user_conf != "User does not exist, try again.":
		print(user_conf)
		user = str(input(" > "))
		ssl_socket.send(( user ).encode())								#User_Search
		if user == 'quit':
			return
		user_conf = ssl_socket.recv(1024).decode()
		
	print(user_conf)

	# Get name of Interview
	print("Enter the name of the interviewer you wish to assign:")
	interview = str(input(" > "))

	#Confirms that the interview exists

	ssl_socket.send(( interview ).encode())								#Interview_Search
	interview_conf = ssl_socket.recv(1024).decode()			
	#if no existing user
	while interview_conf != "Interview does not exist, try again.":
		print(interview_conf)
		interview = str(input(" > "))
		ssl_socket.send(( interview ).encode())							#Interview_Search
		if interview == 'quit':
			return
		interview_conf = ssl_socket.recv(1024).decode()

	print(interview_conf)	# Assigning Interview
	interview_conf = ssl_socket.recv(1024).decode() #
	print(interview_conf)	# INTERVIEW has been assigned to USER

	pass

def validate(loggedInAs):
    # KH -- EXCISED PER LICENSING RESTRICTION
    pass
    
# CURRENT CERTIFICATE'S HOSTNAME IS 'localhost'
# won't work if not using 'localhost' unless you create a new certificate with new host address as the certificate's commonName
def ssl_connection(client_socket):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_verify_locations("cert.pem")
    # wrap client_socket, uses RSA encryption, certificate required
    ssl_socket = ssl.wrap_socket(client_socket, ciphers="RSA:!COMPLEMENTOFALL", ca_certs="cert.pem", cert_reqs=ssl.CERT_REQUIRED)
    # make connection
    ssl_socket.connect((_HOST, _PORT))
    # verify certificate and do handshake
    cert = ssl_socket.getpeercert()
    ssl.match_hostname(cert, _HOST)
    ssl_socket.do_handshake()
    return ssl_socket
    
# use:
# openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout cert.pem
# on the cmd line to generate new certificate (update ssl.match_hostname() parameter)
if __name__ == "__main__":
    import sys
    import socket
    import ssl

    argc = len(sys.argv)

    if (argc != 3):
        _HOST = str(input("Enter HOST name: "))
        _PORT = int(input("Enter PORT number: "))
    else:
        _HOST = str(sys.argv[1])
        _PORT = int(sys.argv[2])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_socket = ssl_connection(client_socket)

    #Server greets client
    greeting_msg = ssl_socket.recv(1024)
    greeting_msg = (greeting_msg).decode()
    print(greeting_msg)

    #Prompt For Password and Username
    USER_NAME = str(input("Username: "))
    ssl_socket.send((USER_NAME).encode())
    USER_PW   = str(input("Password: "))
    ssl_socket.send((USER_PW).encode())

    confirmation= str(ssl_socket.recv(1024).decode()) # confirms credentials
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
        adminMenu(ssl_socket)
        #admin_interface
    elif cred == 3:
        print("other?")
        #review_answers

    terminate_session()
    print("Logging Out...")
