# Copyright 2016. DePaul University. All rights reserved.
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.

if __name__ == "__main__":
    import socket
    import time
    from argparse import ArgumentParser
    from interview_portal_serverthread import ServerThread
    import logging
    import logging.config

    logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
    logger = logging.getLogger(__name__)

    parser = ArgumentParser(
        description='CSC 376 Final Project : Interview Portal')
    parser.add_argument(
        'port', type=int, help='Port used to connect to Server')
    args = parser.parse_args()
    _PORT = args.port
    _HOST = 'localhost'

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((_HOST, _PORT))
    print('SERVER > Server established on :', _HOST)
    print('SERVER > Listening on port :', _PORT)
    server_socket.listen(5)

    logger.info('server established on: {} and listening on port: {} '.format(
        _HOST, _PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('SERVER > New client connected :', client_socket)
        logger.info('New client connected : {}'.format(client_socket))
        ServerThread(client_socket).start()

    time.sleep(5)

    print('SERVER > Server terminating')
    logger.info('Server terminated: {}'.format(server_socket))
    server_socket.close()
