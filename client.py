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

# Menu for an admin user
def adminMenu(ssl_socket):
    print('What would you like to do?')
    print('(1) create interview')
    print('(2) review interview')
    print('(3) assign interview')
    print('(4) List users')
    print('(q) Log out and exit')

    correct_input = False
    while(not correct_input):
        response = str(input(' > '))
        if(response != '1' and response != '2' and response != '3' and response.upper() != 'Q'):
            print('Error: Please enter a valid response corresponding to desired action.')
        else:
            correct_input = True
    ssl_socket.send((response).encode())

    correct_input = False
    #confirmation = ssl_socket.recv(1024).decode()
    print(confirmation)
    while(True):
        # admin credential identifier = 3
        cred = 3
        if response == '1':
            create_interview(ssl_socket, cred)
            break
        elif response == '2':
            review_interview(ssl_socket, cred)
            break
        elif response == '3':
            assign_interview(ssl_socket, cred)
            break
        elif response == '4':
            list_users()
            break
        elif response.upper() == 'Q':
            break
        else:
            sys.stdout.flush()
            return

# Menu for an interviewee user
def intervieweeMenu(ssl_socket):
    print('What would you like to do?')
    print('(1) take interview')
    print('(q) Log out and exit')

    correct_input = False
    while(not correct_input):
        response = str(input(' > '))
        if(response != '1' and response != '2' and response != '3' and response.upper() != 'Q'):
            print('Error: Please enter a valid response corresponding to desired action.')
        else:
            correct_input = True
    ssl_socket.send((response).encode())

    #confirmation = ssl_socket.recv(1024).decode()
    print(confirmation)
    while True:
        if response == '1':
            take_interview(ssl_socket)
            break
        elif response.upper() == 'Q':
            break
        else:
            sys.stdout.flush()
            return

# Menu for a lawyer user
def lawyerMenu(ssl_socket):
    print('What would you like to do?')
    print('(1) create interview')
    print('(2) review interview')
    print('(3) assign interview')
    print('(q) Log out and exit')

    correct_input = False
    while(not correct_input):
        response = str(input(' > '))
        if(response != '1' and response != '2' and response != '3' and response.upper() != 'Q'):
            print('Error: Please enter a valid response corresponding to desired action.')
        else:
            correct_input = True
    ssl_socket.send((response).encode())

    #confirmation = ssl_socket.recv(1024).decode()
    print(confirmation)
    while True:
        # lawyer credential identifier = 2
        cred = 2
        if response == '1':
            create_interview(ssl_socket, cred)
            break
        elif response == '2':
            reviewInterview(ssl_socket, cred)
            break
        elif response == '3':
            assignInterview(ssl_socket, cred)
            break
        elif response.upper() == 'Q':
            break
        else:
            sys.stdout.flush()
            return

# =========================================================================
#             LAWYER: INTERVIEW CREATION   
# Status: Incomplete (skeleton finished)
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
# - SYNC: test/refine loop control
# =========================================================================

def create_interview(ssl_socket, cred):
    
    # incoming intro message
    intro_msg = ssl_socket.recv(1024).decode()
    if(len(intro_msg) != 0):
        print(intro_msg)
    
    # incoming name entry request
    name_msg = ssl_socket.recv(1024).decode()
    if(len(name_msg) != 0):
        print(name_msg)
    
    # outgoing name submission
    name_entry = str(input(' > '))
    ssl_socket.send(name_entry.encode() )
    
    # incoming description entry request
    desc_msg = ssl_socket.recv(1024).decode()
    if(len(desc_msg) != 0):
        print(desc_msg)
    
    # outgoing description submission
    desc_entry = str(input(' > '))
    ssl_socket.send(desc_entry.encode() )
    
    ## INTERVIEW CREATION LOOP ##
    while(True):
         
        # incoming question entry request
        question_msg = ssl_socket.recv(1024).decode()
        if(len(question_msg) != 0):
            print(question_msg)
        
        # outgoing question submission (String)
        question_entry = str(input(' > '))
        ssl_socket.send(question_entry.encode() )
        
        # incoming question echo
        echo = ssl_socket.recv(1024).decode()
        if(len(echo) != 0):
            print(echo)
        
        # incoming verify request
        verify_msg = ssl_socket.recv(1024).decode()
        if(len(verify_msg) != 0):
            print(verify_msg)
        
        # outgoing verification (String) Y/N
        verify_entry = str(input(' > ')) 
        ssl_socket.send(verify_entry.encode() )
        
        ## INNER LOOP CONTROL ##
        # Y: save question (terminate loop)
        if verify_entry.upper() == 'Y':
            
            # incoming confirmation message
            confirm_msg = ssl_socket.recv(1024).decode()
            question_id = ssl_socket.recv(1024).decode()
            if(len(confirm_msg) != 0):
                print(confirm_msg, question_id)
        
        # N: redo question (loop again)
        elif verify_entry.upper() == 'N':
            continue
        
        # invalid response
        else:
            invalid_resp = ssl_socket.recv(1024).decode()
            if(len(invalid_resp) != 0):
                print(invalid_resp)    
            
        # incoming request for more questions
        add_msg = ssl_socket.recv(1024).decode()
        if(len(add_msg) != 0):
            print(add_msg)
        
        # outgoing response (String) Y/N
        add_resp = input(str(' > '))
        ssl_socket.send(add_resp.encode() )
        
        # N: add new interview to database (terminate loop)
        if add_resp.upper() == 'N':
            
            # incoming confirmation message and interview id
            db_msg = ssl_socket.recv(1024).decode()
            interview_id = ssl_socket.recv(1024).decode()
            if(len(db_msg) != 0):
                print(db_msg, interview_id)
            break
        
        # Y: add more questions (loop again)
        elif add_resp.upper() == 'Y':
            continue
        
        # invalid response
        else:
            invalid_resp = ssl_socket.recv(1024).decode()
            if(len(invalid_resp) != 0):
                print(invalid_resp)    
        
        ## post-interview display ##
        
        # <PROTOCOL: retrieve interview from database and display full details?>
        
        # END create_interview: back to Lawyer Options
    if cred == 2:
        lawyerMenu(ssl_socket)   
    elif cred == 3:
        adminMenu(ssl_socket)
    
    # remove pass when code is complete
    #pass
       
# ===========================================================================
#             LAWYER: INTERVIEW ASSIGNMENT   
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

def assign_interview(ssl_socket, cred):

    # Get name of Interviewee
    intro = ssl_socket.recv(1024).decode()
    print(intro)
    print('Enter the name of the interviewe you wish to assign:')
    user = str(input(' > '))

    #Confirms that the interviewee exists

    ssl_socket.send(( user ).encode()) 									#User_Search
    user_conf = ssl_socket.recv(1024).decode()

    #if no existing user
    while user_conf != 'User exists':
        print(user_conf)
        user = str(input(' > '))
        ssl_socket.send(( user ).encode())								#User_Search
        if user == 'quit':
            return
        user_conf = ssl_socket.recv(1024).decode()

    print(user_conf)

    # Get name of Interview
    print('Enter the name of the interviewe you wish to assign:')
    interview = str(input(' > '))

    #Confirms that the interview exists

    ssl_socket.send(( interview ).encode())								#Interview_Search
    interview_conf = ssl_socket.recv(1024).decode()			
    #if no existing user
    while interview_conf == 'Interview does not exist, try again.':
        print(interview_conf)
        interview = str(input(' > '))
        ssl_socket.send(( interview ).encode())							#Interview_Search
        if interview == 'quit':
            return
        interview_conf = ssl_socket.recv(1024).decode()

    print(interview_conf)	# Assigning Interview
    interview_conf = ssl_socket.recv(1024).decode() #
    print(interview_conf)	# INTERVIEW has been assigned to USER

    if cred == 2:
        lawyerMenu(ssl_socket)   
    elif cred == 3:
        adminMenu(ssl_socket)

    pass
    
def review_submissions():
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
def manage_interviews(ssl_socket, cred):
    
    ## MANAGE_INTERVIEWS LOOP ##
    while(True):
        
        ## options display ##
    
        # incoming option messages
        option_msg = ssl_socket.recv(1024).decode()
        option_e = ssl_socket.recv(1024).decode()
        option_d = ssl_socket.recv(1024).decode()
        option_q = ssl_socket.recv(1024).decode()
        
        if(option_msg != 0 and
           option_e   != 0 and
           option_d   != 0 and 
           option_q   != 0    ):
            print(option_msg)
            print(option_e)
            print(option_d)
            print(option_q)
         
        ## LOOP CONTROL ##
            
        # outgoing option response
        option_resp = str(input(' > '))
        ssl_socket.send(option_resp.encode() )
        
        # E: edit/view created interviews
        if option_resp == 'E':
            
            # incoming edit/view intro message
            edit_msg = ssl_socket.recv(1024).decode()
            if(len(edit_msg) != 0):
                print(edit_msg)
                
            # <PROTOCOL: generate interview list from database >
            # display <none> if none exist
            
            # incoming interview selection message
            select_msg = ssl_socket.recv(1024).decode()
            if(len(select_msg) != 0):
                print(select_msg)
                
            # outgoing interview selection entry
            select_entry = str(input(' > '))
            ssl_socket.send( select_entry.encode() )
            
            # <PROTOCOL: 
            #    - retrieve interview based on criteria
            #    - ask for name change; if yes, make database changes
            #    - generate loop for each question
            #    - ask for question edit; if yes, make database changes>
            
            # incoming confirmation message
            confirm_msg = ssl_socket.recv(1024).decode()
            if(len(confirm_msg) != 0):
                print(confirm_msg)
        
        # D: remove created interview
        elif option_resp == 'D':
            
            ## verification loop ##
            while(True):
                
                # incoming delete intro message
                delete_msg = ssl_socket.recv(1024).decode()
                if(len(delete_msg) != 0):
                    print(delete_msg)
                    
                # <PROTOCOL: generate interview list from database >
                # display <none> if none exist
                
                # incoming interview selection message
                select_msg = ssl_socket.recv(1024).decode()
                if(len(select_msg) != 0):
                    print(select_msg)
                
                # outgoing interview selection entry
                select_entry = str(input(' > '))
                ssl_socket.send(select_entry.encode() )
                
                ## LOOP CONTROL ##
                
                # incoming verify request
                verify_msg = ssl_socket.recv(1024).decode()
                if(len(verify_msg) != 0):
                    print(verify_msg)
            
                # outgoing verification (String) Y/N
                verify_entry = str(input(' > ')) 
                ssl_socket.send(verify_entry.encode() )
                
                # Y: confirm selection
                if verify_entry == 'Y':
                    
                    # incoming confirmation message
                    confirm_msg = ssl_socket.recv(1024).decode()
                    if(len(confirm_msg) != 0):
                        print(confirm_msg)
                    break
                
                # N: redo selection
                elif verify_entry == 'N':
                    continue
                
                # invalid response
                else:
                    
                    invalid_resp = ssl_socket.recv(1024).decode()
                    if(len(invalid_resp) != 0):
                        print(invalid_resp)    
                
        
        # Q: return to Lawyer Options
        elif option_resp == 'Q':
            break
        
        # invalid response
        else:
            
            invalid_resp = ssl_socket.recv(1024).decode()
            if(len(invalid_resp) != 0):
                print(invalid_resp)    
    
    if cred == 2:
        lawyerMenu(ssl_socket)   
    elif cred == 3:
        adminMenu(ssl_socket)
    # remove pass when code is complete    
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
def take_interview(ssl_socket):
    
    # incoming intro message
    intro_msg = ssl_socket.recv(1024).decode()
    if(len(intro_msg) != 0):
        print(intro_msg)
        
    # assigned interview list
    # <PROTOCOL: generate interviewee's interview list from database?>
    # display <none> if none exist
    
    # incoming interview selection request
    select_msg = ssl_socket.recv(1024).decode()
    if(len(select_msg) != 0):
        print(select_msg)
    
    # outgoing interview selection entry
    select_entry = input(str(' > '))
    ssl_socket.send(select_entry.encode() )
    
    # <PROTOCOL: 
    #    - retrieve interview based on criteria
    #    - generate loop for each question
    #    - for each question, ask for answer, link it to question
    #    - add interview to review list>
    
    # incoming confirmation message
    confirm_msg = ssl_socket.recv(1024).decode()
    if(len(confirm_msg) != 0):
        print(confirm_msg)
        
    # END take_interview: return to Interviewee Options
    
    # remove pass when code is complete
    pass



def validate(loggedInAs):
    # KH -- EXCISED PER LICENSING RESTRICTION
    pass
    
# CURRENT CERTIFICATE'S HOSTNAME IS 'localhost'
# won't work if not using 'localhost' unless you create a new certificate with new host address as the certificate's commonName
def ssl_connection(client_socket):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_verify_locations('cert.pem')
    # wrap client_socket, uses RSA encryption, certificate required
    ssl_socket = ssl.wrap_socket(client_socket, ciphers='RSA:!COMPLEMENTOFALL', ca_certs='cert.pem', cert_reqs=ssl.CERT_REQUIRED)
    # make connection
    ssl_socket.connect((_HOST, _PORT))
    # verify certificate and do handshake
    cert = ssl_socket.getpeercert()
    ssl.match_hostname(cert, _HOST)
    ssl_socket.do_handshake()
    return ssl_socket

"""
def generate_server_self_cert(cert_dir): #takes a directory to save the certificate in
   CERT_FILE = 'InterviewPortal.crt'
   KEY_FILE = 'InterviewPortal.key'

   if not exists(join(cert_dir, CERT_FILE)) \
            or not exists(join(cert_dir, KEY_FILE)):
            # create a key pair
        publicKey = crypto.PKey()
        publicKey.generate_key(crypto.TYPE_RSA, 1024)

       # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = 'US'
        cert.get_subject().ST = 'Illinois'
        cert.get_subject().L = 'Chicago'
        cert.get_subject().O = 'CSC 376'
        cert.get_subject().OU = 'Interview Portal'
        cert.get_subject().CN = socket.gethostname()
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10*365*24*60*60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(publicKey)
        cert.sign(publicKey, 'sha1')

        open(join(cert_dir, CERT_FILE), 'wb').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        open(join(cert_dir, KEY_FILE), 'wb').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, publicKey))
   else:
        print('Certificate/Key already exist! New one will not be generated.')
 """

# use:
# openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout cert.pem
# on the cmd line to generate new certificate (update ssl.match_hostname() parameter)
if __name__ == '__main__':
    import sys
    import socket
    import ssl

    argc = len(sys.argv)

    if (argc != 3):
        _HOST = str(input('Enter HOST name: '))
        _PORT = int(input('Enter PORT number: '))
    else:
        _HOST = str(sys.argv[1])
        _PORT = int(sys.argv[2])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_socket = ssl_connection(client_socket)

    #Server greets client
    greeting_msg = ssl_socket.recv(1024).decode()
    print(greeting_msg)

    #Ask user to login or create new account
    print('(1) Login.')
    print('(2) Create New User.')

    correct_input = False
    while(not correct_input):
        response = str(input('> '))
        if(response != '1' and response != '2' and response.upper() != 'L' and response.upper() != 'C'):
            print('Error: Please enter a valid number corresponding to desired action.')
        else:
            correct_input = True
    ssl_socket.send((response).encode())
    if (response == '2'):
    	new_USER_NAME = str(input('Enter Username: '))
    	ssl_socket.send((new_USER_NAME).encode())
    	USER_AUTH     = str(input('Enter Authorization: '))
    	ssl_socket.send((USER_AUTH).encode())

    #Prompt For Password and Username
    USER_NAME = str(input('Username: '))
    ssl_socket.send((USER_NAME).encode())
    USER_PW   = str(input('Password: '))
    ssl_socket.send((USER_PW).encode())

    confirmation= str(ssl_socket.recv(1024).decode()) # confirms credentials
    print(confirmation)                             #print credentials
    try:
        cred = int(confirmation)
        
    except ValueError:
        terminate_session()
        sys.exit()
        
    if cred == 1:
        print('interviewee')
        intervieweeMenu(ssl_socket)
    elif cred == 2:
        print('lawyer')
        lawyerMenu(ssl_socket)
    elif cred == 3:
        print('admin')
        adminMenu(ssl_socket)

    terminate_session()
    print('Logging Out...')
