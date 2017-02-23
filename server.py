# Copyright 2016. DePaul University. All rights reserved. 
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.

if __name__ == "__main__":
    import sys
    import socket
    from serverthread import ServerThread

    argc = len(sys.argv)

    if (argc != 3):
    	_HOST = str(input("Enter HOST name: "))
    	_PORT = int(input("Enter PORT number: "))
    else:
    	_HOST = str(sys.argv[1])
    	_PORT = int(sys.argv[2])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind( (_HOST, _PORT ) )
    print('SERVER > Server established on :', _HOST)
    print('SERVER > Listening on port :', _PORT)
    server_socket.listen(5)

    while True:
    	client_socket, client_addr = server_socket.accept()
    	print("New client connecting")
    	ServerThread(client_socket).start()

    print('SERVER > Server terminating' )
    server_socket.close()