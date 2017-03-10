# Copyright 2016. DePaul University. All rights reserved. 
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.
#Anna 

#Client Login
import socket
from loginauth import LoginAuthentication
 
def Main():
	host = '127.0.0.1'
	port = 5001
	
	mySocket = socket.socket()
	mySocket.connect((host,port))
	menu()
				
	mySocket.close()

if __name__ == '__main__':
	Main()

def terminate_session():
    print('Terminating connection to server')
    for i in range(0,10):
        print('.', end = '')
        sys.stdout.flush()
    ssl_socket.close()
    print('Server socket closed')
    return

# Menu for an admin user
def menu(ssl_socket):
    print('Welcome')
	print('Choose one of the following')
	print('Type (1) to login')
	print('Type (2) to Register')
	print('Type (3) to login as Admin')
	print('Type (4) to login as Lawyer')
	print('Type (q) to exit')

    correct_input = False
    while(not correct_input):
        response = str(input(' > '))
        if(response != '1' and response != '2' and response != '3' and response != 'q'):
            print('Error: Please enter a valid response corresponding to desired action.')
        else:
            correct_input = True
    ssl_socket.send((response).encode())

    correct_input = False
    #confirmation = ssl_socket.recv(1024).decode()
    print(confirmation)
    while(True):
        if response == '1':
            user_login(ssl_socket)
            break
        elif response == '2':
            user_register(ssl_socket)
            break
        elif response == '3':
            admin_login(ssl_socket)
            break
		elif response == '4':
			lawyer_login(ssl_socket)
			break
        else:
            sys.stdout.flush()
            return
			
def user_login(ssl_socket):
	Print('Login ')
	user = input('Enter your username')
	psw = input ('Enetr your password')
	
	if login(user,pswd)==False:
		print('username and password combination is incorrect')
		user_login(ssl_socket)
	else:
		print('Username and password are correct')
		print('redirecting to another page')
		intervieweeMenu(ssl_socket)
	
def user_register(ssl_socket):
Print('Register')
	name = input('Enter your name')
	user = input('Enter your username')
	psw = input ('Enetr your password')
	authkey = 'Something'
	
	if register==False:
	print('username and password are taken')
	print('Choose another username and password')
		user_login(ssl_socket)
	else:
	print('Name, Username and password have been recorded')
	print('redirecting to another page')
	intervieweeMenu(ssl_socket)
	
	
def admin_login(ssl_socket):
Print(' Admin Login ')
	user = input('Enter your username')
	psw = input ('Enetr your password')
	
	if login(user,pswd)==False:
		print('username and password combination is incorrect')
		admin_login(ssl_socket)
	else:
		print('Username and password are correct')
		print('redirecting to another page')
		adminMenu(ssl_socket)
		
def lawyer_login(ssl_socket):
Print(' Lawyer Login ')
	user = input('Enter your username')
	psw = input ('Enetr your password')
	
	if login(user,pswd)==False:
		print('username and password combination is incorrect')
		lawyer_login(ssl_socket)
	else:
		print('Username and password are correct')
		print('redirecting to another page')
		lawyerMenu(ssl_socket)
	
	
	
		
	

	
		
	
	