# Copyright 2016. DePaul University. All rights reserved. 
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.

#from interview_error import CredentialsException
from loginauth import LoginAuthentication
#DG
_HOST = "localhost"
_PORT = 8001
#DG

import os
from OpenSSL import crypto, SSL
from os.path import exists, join

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
    print('(4) manage users')
    print('(q) Log out and exit')

    while(True):
        response = str(input(' > '))
        if(response != '1' and response != '2' and response != '3' and response != '4' and response.upper() != 'Q'):
            print('Error: Please enter a valid response corresponding to desired action.')
        else:
            break
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
            review_submissions(ssl_socket, cred)
            break
        elif response == '3':
            assign_interview(ssl_socket, cred)
            break
        elif response == '4':
            manage_users(ssl_socket)
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

    while(True):
        response = str(input(' > '))
        if(response != '1' and response != '2' and response != '3' and response.upper() != 'Q'):
            print('Error: Please enter a valid response corresponding to desired action.')
        else:
            break
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

    while(True):
        response = str(input(' > '))
        if(response != '1' and response != '2' and response != '3' and response.upper() != 'Q'):
            print('Error: Please enter a valid response corresponding to desired action.')
        else:
            break
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
            review_submission(ssl_socket, cred)
            break
        elif response == '3':
            assign_interview(ssl_socket, cred)
            break
        elif response.upper() == 'Q':
            break
        else:
            sys.stdout.flush()
            return
def staffMenu(ssl_socket):
    print('What would you like to do?')
    #print('(1) create interview')
    print('(1) review interview')
    #print('(3) assign interview')
    print('(q) Log out and exit')

    while(True):
        response = str(input(' > '))
        if(response != '1' and response.upper() != 'Q'):
            print('Error: Please enter a valid response corresponding to desired action.')
        else:
            break
    ssl_socket.send((response).encode())

    #confirmation = ssl_socket.recv(1024).decode()
    print(confirmation)
    while True:
        # lawyer credential identifier = 2
        cred = 2
        if response == '1':
            review_submissions(ssl_socket, cred)
            break
        elif response.upper() == 'Q':
            break
        else:
            sys.stdout.flush()
            return
# =========================================================================
#             LAWYER: INTERVIEW CREATION   
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
        add_resp = str(input(' > '))
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

def assign_interview(ssl_socket, cred):

    # Get name of Interviewee
    intro = ssl_socket.recv(1024).decode()
    print(intro)
    print('Enter the name of the interviewee you wish to assign:')
    user = str(input(' > '))

    #Confirms that the interviewee exists

    ssl_socket.send(( user ).encode())                                  #User_Search
    user_conf = ssl_socket.recv(1024).decode()

    #if no existing user
    while user_conf != 'User exists':
        print(user_conf)
        user = str(input(' > '))
        ssl_socket.send(( user ).encode())                              #User_Search
        if user == 'quit':
            return
        user_conf = ssl_socket.recv(1024).decode()

    print(user_conf)
    interview= ''
    while (interview != 'end'):
        interview = ssl_socket.recv(1024).decode()
        print(interview)
    # Get name of Interview
    print('Enter the number of the interview you wish to assign to the user:')
    interview = str(input(' > '))

    #Confirms that the interview exists

    ssl_socket.send(( interview ).encode())                             #Interview_Search
    interview_conf = ssl_socket.recv(1024).decode()         
    #if no existing user
    while interview_conf == 'Interview does not exist, try again.':
        print(interview_conf)
        interview = str(input(' > '))
        ssl_socket.send(( interview ).encode())                         #Interview_Search
        if interview == 'quit':
            return
        interview_conf = ssl_socket.recv(1024).decode()

    print(interview_conf)   # Assigning Interview
    interview_conf = ssl_socket.recv(1024).decode() #
    print(interview_conf)   # INTERVIEW has been assigned to USER

    '''if cred == 2:
        lawyerMenu(ssl_socket)   
    elif cred == 3:
        adminMenu(ssl_socket)
    '''
    if cred == 2:
        lawyerMenu(ssl_socket)   
    elif cred == 3:
        adminMenu(ssl_socket)
    
def review_submissions(ssl_socket, cred):

   # Get name of Interviewee
    intro = ssl_socket.recv(1024).decode()
    print(intro)
    print('Enter the name of the interviewee to review:')
    user = str(input(' > '))

    #Confirms that the interviewee exists

    ssl_socket.send(( user ).encode())                                  #User_Search
    user_conf = ssl_socket.recv(1024).decode()

    #if no existing user
    while user_conf != 'User exists':
        print(user_conf)
        user = str(input(' > '))
        ssl_socket.send(( user ).encode())                              #User_Search
        if user == 'quit':
            return
        user_conf = ssl_socket.recv(1024).decode()

    print(user_conf)
    interview= ''

    while (interview != 'end'):
        interview = ssl_socket.recv(1024).decode()
        print(interview)
    #interviews = list(ssl_socket.recv(1024).decode())
    #for interview in interviews:
    #    print('(' + interview[0] + ') '+ interview[1] )


    # Get name of Interview
    print('Enter the ID of the interview to review:')
    interview = str(input(' > '))

    #Confirms that the interview exists

    ssl_socket.send(( interview ).encode())
    print('just sent input')                             #Interview_Search
    interview_conf = ssl_socket.recv(1024).decode()
    #print(interview_conf)         
    #if no existing user
    while interview_conf == 'Interview does not exist, try again.':
        print(interview_conf)
        interview = str(input(' > '))
        ssl_socket.send(( interview ).encode())                         #Interview_Search
        if interview == 'quit':
            return
        interview_conf = ssl_socket.recv(1024).decode()

    print(interview_conf) 
    review = ''
    while (review != 'End of Interview'):
        review = (ssl_socket.recv(1024).decode())
        print(review)
    #print(interview_conf)   # Assigning Interview
    #interview_conf = ssl_socket.recv(1024).decode() #
    #print(interview_conf)   # INTERVIEW has been assigned to USER

    '''if cred == 2:
        lawyerMenu(ssl_socket)   
    elif cred == 3:
        adminMenu(ssl_socket)
    '''
    if cred == 2:
        lawyerMenu(ssl_socket)   
    elif cred == 3:
        adminMenu(ssl_socket)

# ===========================================================================
#             LAWYER: MANAGE INTERVIEWS
# Status: Near Complete
# 
# Precondition(s):
# - Lawyer/Staff account session
#
# Postcondition: 
# - interview edited in database, interview deleted from database, or
#   return to main menu
#
# TO DO
# - debug
# =============================================================================
def manage_interviews(ssl_socket, cred):
    
    ## MANAGE_INTERVIEWS LOOP ##
    while(True):
        
        ## INTRO AND OPTIONS ##
    
        # incoming manage_interviews intro message
        mi_msg = ssl_socket.recv(1024).decode()
        if(len(mi_msg) != 0):
            print(mi_msg) 
        
        # incoming option messages
        msgs = ''
        while(msgs != 'end'):
            msgs = str(ssl_socket.recv(1024).decode())
            if(len(msgs) != 0):
                print(msgs)
         
        ## LOOP CONTROL ##
        # outgoing option response
        option_resp = str(input(' > '))
        ssl_socket.send(option_resp.encode() )
        
        # E: edit/view created interviews
        if option_resp.upper() == 'E':
            
            ## INTERVIEW SUMMARY ##
            # incoming edit/view intro message
            edit_msg = ssl_socket.recv(1024).decode()
            if(len(edit_msg) != 0):
                print(edit_msg)
                
            # incoming lawyer-created interviews list
            interview_list = ''
            while (interview_list != 'end'):
                interview_list = ssl_socket.recv(1024).decode()
                if(len(interview_list) != 0):
                    print(interview_list)
                if(interview_list == 'No Interviews available!'):
                    return
            
            ## INTERVIEW SELECTION ##
            # incoming interview selection prompt
            select_msg = ssl_socket.recv(1024).decode()
            if(len(select_msg) != 0):
                print(select_msg)
                
            # outgoing interview selection entry
            select_entry = str(input(' > '))
            ssl_socket.send( select_entry.encode() )
            
            ## EDITING OPTIONS ##
            while(True):
                
                # incoming editing options
                msgs = ''
                while(msgs != 'end'):
                    msgs = str(ssl_socket.recv(1024).decode())
                    if(len(msgs) != 0):
                        print(msgs)
            
                # outgoing edit option choice (N, Q, or R)
                edit_choice = str(input(' > '))
                ssl_socket.send(option_resp.encode() )
            
                # N: edit name
                if edit_choice.upper() == 'N':
                    
                    # incoming name change prompt
                    name_req = ssl_socket.recv(1024).decode()
                    if(len(name_req) != 0):
                        print(name_req)
                    
                    # outgoing name change input    
                    new_name = str(input(' > '))
                    ssl_socket.send(new_name.encode() )
                    
                    # incoming name change confirmation message
                    name_conf = ssl_socket.recv(1024).decode()
                    if(len(name_conf) != 0):
                        print(name_conf)
                
                # Q: edit question
                elif edit_choice.upper() == 'Q':
                    
                    while(True):
                        
                        ## INTERVIEW QUESTIONS DISPLAY ##
                        question_list = ''
                        while (question_list != 'end'):
                            question_list = ssl_socket.recv(1024).decode()
                            if(len(question_list) != 0):
                                print(question_list)
                            
                        ## QUESTION EDITING ##
                        # incoming question selection request
                        q_select = ssl_socket.recv(1024).decode()
                        if(len(q_select) != 0):
                            print(q_select)
                        
                        # outgoing question selection choice 
                        q_choice = str(input(' > '))
                        ssl_socket.send(q_choice.encode() )
                    
                        # incoming current question text display
                        q_current = ssl_socket.recv(1024).decode()
                        if(len(q_current) != 0):
                            print(q_current)
                        
                        # incoming question change request
                        q_req = ssl_socket.recv(1024).decode()
                        if(len(q_req) != 0):
                            print(q_req)
                        
                        # outgoing question change input
                        q_change = str(input(' > '))
                        ssl_socket.send(q_change.encode() )
                        
                        ## QUESTION CHANGE CONFIRMATION ##
                        q_conf = ssl_socket.recv(1024).decode()
                        if(len(q_conf) != 0):
                            print(q_conf)
                            
                        ## LOOP CONTROL ##
                        # incoming prompt to add more questions (Y/N)
                        q_continue = ssl_socket.recv(1024).decode()
                        if(len(q_continue) != 0):
                            print(q_continue)
                            
                        # Y:
                        if q_continue.upper() == 'Y':
                            continue
                        # N:
                        elif q_continue.upper() == 'N':
                            break
                        # invalid response
                        else:
                            invalid_resp = ssl_socket.recv(1024).decode()
                            if(len(invalid_resp) != 0):
                                print(invalid_resp)
                    
                    
                # R: return to Created Interview Options
                elif edit_choice.upper() == 'R':
                    break
                # invalid response
                else:
                    invalid_resp = ssl_socket.recv(1024).decode()
                    if(len(invalid_resp) != 0):
                        print(invalid_resp)  
        
        # D: remove created interview
        elif option_resp.upper() == 'D':
            
            ## verification loop ##
            while(True):
                
                # incoming delete intro message
                delete_msg = ssl_socket.recv(1024).decode()
                if(len(delete_msg) != 0):
                    print(delete_msg)
                    
                # incoming lawyer-created interviews list
                interview_list = ''
                while (interview_list != 'end'):
                    interview_list = ssl_socket.recv(1024).decode()
                    if(len(interview_list) != 0):
                        print(interview_list)
                    if(interview_list == 'No Interviews available!'):
                        return
                
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
                if verify_entry.upper() == 'Y':
                    
                    # incoming confirmation message
                    confirm_msg = ssl_socket.recv(1024).decode()
                    if(len(confirm_msg) != 0):
                        print(confirm_msg)
                    break
                
                # N: redo selection
                elif verify_entry.upper() == 'N':
                    continue
                
                # invalid response
                else:
                    invalid_resp = ssl_socket.recv(1024).decode()
                    if(len(invalid_resp) != 0):
                        print(invalid_resp)    
                
        
        # Q: return to Lawyer Options
        elif option_resp.upper() == 'Q':
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
    # display <none> if none exist
    # incoming lawyer-created interviews list

    interview= ''
    while (interview != 'end'):
            interview = ssl_socket.recv(1024).decode()
            print(interview)

   # incoming interview selection request
    select_msg = ssl_socket.recv(1024).decode()
    if(len(select_msg) != 0):
        print(select_msg)

   # outgoing interview selection entry
    select_entry = input(str(' > '))
    ssl_socket.send(select_entry.encode() )

   #    - retrieve interview based on criteria
    #    - generate loop for each question
    question= ''
    while (question != 'end'):
            question = ssl_socket.recv(1024).decode()
            print(question)
            #- for each question, ask for answer, link it to question
            if (question != 'end'):
                answer = input(str(' > '))
                ssl_socket.send(answer.encode())

   #    - add interview to review list>

   # incoming confirmation message
    confirm_msg = ssl_socket.recv(1024).decode()
    if(len(confirm_msg) != 0):
        print(confirm_msg)

   # END take_interview: return to Interviewee Options
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

def manage_users(ssl_socket):
    print (ssl_socket.recv(1024).decode()) #Wlecome to User Management
    while(True):
        
        print( 'What would you like to do?')
        print('(1) Change a user\'s authorization')
        print('(2) Delete a user')
        print('(q) Exit to menu')
        option = str(input('>'))
        ssl_socket.send((option).encode())

        #Update a user's authorization level
        if (option == '1'):

            print('Please the user ')
            check_user = str(input('>'))
            ssl_socket.send((check_user).encode())
            user_conf = ssl_socket.recv(1024).decode()
            print(user_conf)
            if (user_conf != check_user): #user does not exist
                #print(user_conf)
                break
            else:

                print('Please input new authorization level')
                print('(0) Admin')
                print('(1) Attorney')
                print('(2) Staff')
                print('(3) User')
                new_auth = str(input('>'))

                if (new_auth != '0' and new_auth != '1' and new_auth != '2' and new_auth != '3'):
                    print('Invalid authorization level.')
                    ssl_socket.send(('Invalid Authorization Level').encode())
                    break
                    
                else:
                    ssl_socket.send((new_auth).encode())
                    print (ssl_socket.recv(1024).decode())
                    break

        #Delete a selected user
        elif (option == '2'):
            print('Enter name of user to delete')
            check_user = str(input('>'))
            ssl_socket.send((check_user).encode())
            user_conf = ssl_socket.recv(1024).decode()
            print(user_conf)
            if (user_conf != check_user):
                
                break
            else:
                print('Are you sure you wish to delete '+ check_user+ '? (Y/N')
                second_conf = str(input('>'))
                ssl_socket.send((second_conf).encode())
                print( ssl_socket.recv(1024).decode() ) #response
                break

        else:
            print('Exiting User Managment')
            break


            # interviewscoming lawyer-created interviews list
    adminMenu(ssl_socket)

    
def validate(loggedInAs):
    # KH -- EXCISED PER LICENSING RESTRICTION
    pass
    
def generate_server_self_cert():
	CERT_FILE = "InterviewPortal.crt"
	KEY_FILE = "InterviewPortal.key"
	cert_dir = os.getcwd()

	# if a certificate already exists, a new one will be generated
	if(not exists(join(cert_dir, CERT_FILE)) or not os.path.exists(join(cert_dir, KEY_FILE))):
	    key = crypto.PKey()
	    key.generate_key(crypto.TYPE_RSA, 1024)
	    cert = crypto.X509()
	    cert.get_subject().C = "US"
	    cert.get_subject().ST = "Illinois"
	    cert.get_subject().L = "Chicago"
	    cert.get_subject().O = "CSC 376"
	    cert.get_subject().OU = "Interview Portal"
	    cert.get_subject().CN = _HOST
	    cert.set_serial_number(1000)
	    cert.gmtime_adj_notBefore(0)
	    cert.gmtime_adj_notAfter(10*365*24*60*60)
	    cert.set_issuer(cert.get_subject())
	    cert.set_pubkey(key)
	    cert.sign(key, 'sha1')

	    open(join(cert_dir, CERT_FILE), "wb").write(
	        crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
	    open(join(cert_dir, KEY_FILE), "wb").write(
	        crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
	return

# CERTIFICATE'S HOSTNAME WILL BE 'localhost'
def ssl_connection(client_socket):
    generate_server_self_cert()
    # wrap client_socket, uses RSA encryption, certificate required
    ssl_socket = ssl.wrap_socket(client_socket, ciphers='RSA:!COMPLEMENTOFALL', ca_certs='InterviewPortal.crt', cert_reqs=ssl.CERT_REQUIRED)
    # make connection
    ssl_socket.connect((_HOST, _PORT))
    # verify certificate and do handshake
    cert = ssl_socket.getpeercert()
    ssl.match_hostname(cert, _HOST)
    ssl_socket.do_handshake()
    return ssl_socket

if __name__ == '__main__':
    import sys
    import socket
    import ssl
    import ClientLogin

    ssl_socket = ssl_connection(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

    # Server greets client
    greeting_msg = ssl_socket.recv(1024).decode()
    print(greeting_msg)

    # Ask user to login or create new account
    print('(1) Login.')
    print('(2) Create New User.')

    correct_input = False
    while (not correct_input):
        response = str(input(' > '))
        if (response != '1' and response != '2' and response.upper() != 'L' and response.upper() != 'C'):
            print('Error: Please enter a valid number corresponding to desired action.')
        else:
            correct_input = True
    ssl_socket.send((response).encode())
    if (response == '2'):
        new_USER_NAME = str(input('Enter Username: '))
        ssl_socket.send((new_USER_NAME).encode())
        USER_AUTH = str(input('Enter Authorization: '))
        ssl_socket.send((USER_AUTH).encode())
        new_USER_PW = str (input('Enter Password:'))
        new_USER_PW = LoginAuthentication.get_hashed_password(new_USER_PW)
        ssl_socket.send(new_USER_PW)

    # Prompt For Password and Username
    USER_NAME = str(input('Username: '))
    ssl_socket.send((USER_NAME).encode())
    USER_PW = str(input('Password: '))
    ssl_socket.send((USER_PW).encode())

    confirmation = str(ssl_socket.recv(1024).decode())  # confirms credentials
    print('conf = ' + str(confirmation))  # print credentials
    try:
        cred = int(confirmation)

    except ValueError:
        terminate_session()
        sys.exit()

    if cred == 3:
        print('Interviewee')
        intervieweeMenu(ssl_socket)
    if cred == 2:
        print('Staff')
        staffMenu(ssl_socket)
    elif cred == 1:
        print('Lawyer')
        lawyerMenu(ssl_socket)
    elif cred == 0:
        print('Admin')
        adminMenu(ssl_socket)

    terminate_session()
    print('Logging Out...')