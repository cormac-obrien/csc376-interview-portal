# Copyright 2016. DePaul University. All rights reserved.
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.

import sys
import threading
import time
import db_interaction
from answer import *
from question import *
from active_interview import *
import logging
import logging.config
logger = logging.getLogger(__name__)
from interview_error import CredentialsException
from encrypt import Encrypt
from DiffieHellman import diffieHellman

enc = ""


# Create a threading.Thread class
class ServerThread(threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self._USER_NAME = ''
        self._USER_PW = ''
        self.currentuser = None

    ##################################################
    ##Helper function for giveInterview. Handles all##
    ##looping needed to assure a correct response   ##
    ##################################################

    def adminMenu(self):
        global enc
        greeting = ("Welcome to the Interview Portal")
        greeting = enc.encrypt(greeting)
        self.client_socket.send(greeting)
        time.sleep(0.05)
        message = ("Please select a function :")
        message = enc.encrypt(message)
        self.client_socket.send(message)
        time.sleep(0.05)
        option1 = ("1. Create an Interview")
        option1 = enc.encrypt(option1)
        self.client_socket.send(option1)
        time.sleep(0.05)
        option2 = ("2. Review an Interview")
        option2 = enc.encrypt(option2)
        self.client_socket.send(option2)
        time.sleep(0.05)
        option3 = ("3. Assign an Interview")
        option3 = enc.encrypt(option3)
        self.client_socket.send(option3)
        time.sleep(0.05)
        option3 = ("4. List Interviewees")
        option3 = enc.encrypt(option3)
        self.client_socket.send(option3)
        time.sleep(0.05)

        response = self.client_socket.recv(1024)
        response = enc.decrypt(response)
        response = response.rstrip()

        while True:
            if response == '1':
                echo = enc.encrypt(response)
                self.client_socket.send(echo)
                self.createInterview()
                break
            elif response == '2':
                echo = enc.encrypt(response)
                self.client_socket.send(echo)
                self.reviewInterview()
                break
            elif response == '3':
                echo = enc.encrypt(response)
                self.client_socket.send(echo)
                self.assignInterview()
                break
            elif response == '4':
                echo = enc.encrypt(response)
                self.client_socket.send(echo)
                self.listUsers()
                break
            else:
                error = "Invalid option, try again"
                error = enc.encrypt(error)
                self.client_socket.send(error)
                time.sleep(0.05)
                response = self.client_socket.recv(1024)
                response = enc.decrypt(response)
                response = response.rstrip()

        return

    def listUsers(self):
        interview_list = 'List of Interviewees'
        interview_list = enc.encrypt(interview_list)
        self.client_socket.send(interview_list)
        time.sleep(0.05)

        user_list = db_interaction.getUsers()
        for users in user_list:
            print('User : ' + users.getName())
            user_name = enc.encrypt(users.getName())
            self.client_socket.send(user_name)
            time.sleep(0.05)
        end_list = 'End of List'
        end_list = enc.encrypt(end_list)
        self.client_socket.send(end_list)
        time.sleep(0.05)

    def reviewInterview(self):
        greetingString = "Interview Review Mode"
        greetingString = enc.encrypt(greetingString)
        self.client_socket.send(greetingString)
        time.sleep(0.05)
        request = "Please enter an Interviewee's User Name :"
        request = enc.encrypt(request)
        self.client_socket.send(request)
        time.sleep(0.05)

        response = self.client_socket.recv(1024)
        response = enc.decrypt(response)
        response = response.rstrip()

        interview_id = db_interaction.getUserInterviewID(response)
        rev = db_interaction.reviewInterview(interview_id)
        print('InterviewID: ' + str(rev.getInterviewID()))
        int_name = rev.getInterviewName()
        int_name = enc.encrypt(int_name)
        self.client_socket.send(int_name)
        time.sleep(0.05)

        for question in rev.getQuestions():
            print('QuestionID: ' + str(question.getQuestionID()))
            q_name = question.getQuestionText()
            q_name = enc.encrypt(q_name)
            self.client_socket.send(q_name)
            time.sleep(0.05)

            print('UserAnswerID: ' + str(question.getUserAnswerID()))
            a_name = question.getUserAnswerText()
            a_name = enc.encrypt(a_name)
            self.client_socket.send(a_name)
            time.sleep(0.05)

        end_list = 'End of Interview'
        end_list = enc.encrypt(end_list)
        self.client_socket.send(end_list)
        time.sleep(0.05)

    def sendQuestion(self, messagestring, sendAnswers):
        global enc
        correct = False
        error = False
        while correct == False:
            messagestring = enc.encrypt(messagestring)
            self.client_socket.send(messagestring)
            messagestring = enc.decrypt(messagestring)
            response = self.client_socket.recv(1024)
            response = enc.decrypt(response)
            response = response.rstrip()
            response = response.upper()
            print(response)
            for tup in sendAnswers:
                if response == tup[2]:
                    correct = True
                    return response
                elif error == False:
                    error = True
                    messagestring = "\nINVALID RESPONSE\nPlease enter a letter exactly as it appears above\n" + messagestring

        return response

        #############################################################
        ##Gives the interview by getting the question data, storing##
        ##it in tuples, and sending the question as text. Once a   ##
        ##response is received, it validates the response and then ##
        ##sends another question. Answer data is stored in tuples. ##
        ##Uses key phrase to end the interview                     ##
        ## -Brandon M                                              ##
        #############################################################
    def giveInterview(self):
        global enc
        answerlist = []
        i = 1
        currentinterview = db_interaction.getInterview(
            self.currentuser.getIntID())
        logger.info('User {} started interview {}'.format(
            self.currentuser.getName(), self.currentuser.getIntID()))
        greetingString = "Welcome to your interview!\n" + currentinterview.getInterviewName(
        )
        greetingString = enc.encrypt(greetingString)
        self.client_socket.send(greetingString)
        currentQuestion = currentinterview.getNextQuestion()
        while currentQuestion != "End of Interview":
            answers = currentQuestion.getAnswers()
            sendAnswers = []
            firstletter = 'A'
            for a in answers:
                sendAnswers.append(
                    (a.getAnswerText(), a.getAnswerID(), firstletter))
                firstletter = chr(ord(firstletter) + 1)
            messagestring = "\n" + currentQuestion.getQuestionText() + "\n"
            for tup in sendAnswers:
                messagestring = messagestring + str(tup[2]) + ": " + str(
                    tup[0]) + "\n"
            response = self.sendQuestion(messagestring, sendAnswers)
            responseID = ""
            for tup in sendAnswers:
                if tup[2] == response:
                    responseID = tup[1]
            currentinterview.answerQuestion(responseID)
            currentQuestion = currentinterview.getNextQuestion()
        db_interaction.submitAnswers(currentinterview)
        self.client_socket.send(enc.encrypt("End of Interview"))
        logger.info('User {} completed interview {}'.format(
            self.currentuser.getName(), self.currentuser.getIntID()))
        return

    def createInterview(self):
        global enc
        greetingString = "Welcome to the interview creator!"
        greetingString = enc.encrypt(greetingString)
        self.client_socket.send(greetingString)
        time.sleep(0.05)
        askQuestionString = "What is the name of this interview?"
        askQuestionString = enc.encrypt(askQuestionString)
        self.client_socket.send(askQuestionString)
        time.sleep(0.05)

        name = self.client_socket.recv(1024)
        name = enc.decrypt(name)

        logger.info(
            'User {} created interview {}'.format(self._USER_NAME, name))
        print(name)
        questions = []

        nextQ = True
        nextA = True

        while (nextQ):
            answers = []
            msg = "Please type a QUESTION?"
            msg = enc.encrypt(msg)
            self.client_socket.send(msg)
            question = self.client_socket.recv(1024)
            question = enc.decrypt(question)
            question = question.rstrip()
            print(question)
            while (nextA):
                msg = "Please type an ANSWER?"
                self.client_socket.send(enc.encrypt(msg))

                answer = self.client_socket.recv(1024)
                answer = enc.decrypt(answer)
                answer = answer.rstrip()
                answerObj = Answer(1000, answer)

                answers.append(answerObj)
                print(answer)

                check = True

                while (check):
                    msg = "Would you like to add another ANSWER (Y/N)?"
                    self.client_socket.send(enc.encrypt(msg))

                    checker = self.client_socket.recv(1024)
                    checker = enc.decrypt(checker)
                    checker = checker.rstrip()
                    checker = checker.upper()
                    print(checker)
                    if checker == 'Y':
                        check = False
                        nextA = True
                    elif checker == 'N':
                        check = False
                        nextA = False
                        print("1")
                    else:
                        msg = "Invalid Response!"
                        self.client_socket.send(enc.encrypt(msg))
                        check = True

            questionObj = Question(1000, question, answers)
            questions.append(questionObj)
            nextA = True
            check2 = True

            while (check2):
                msg = 'Would you like to add another QUESTION (Y/N)?'
                self.client_socket.send(enc.encrypt(msg))

                checker = self.client_socket.recv(1024)
                checker = enc.decrypt(checker)
                checker = checker.rstrip()
                checker = checker.upper()
                if checker == 'Y':
                    check2 = False
                    nextQ = True
                elif checker == 'N':
                    check2 = False
                    nextQ = False
                else:
                    msg = "Invalid Response!"
                    self.client_socket.send(enc.encrypt(msg))
                    check = True

        interview = ActiveInterview(1000, name, questions)

        print(questions)

        interviewID = db_interaction.makeNewInterview(interview,
                                                      self.currentuser.getID())
        assigning = True
        msg = 'Would you like to assign this interview to a user (Y/N)?'
        self.client_socket.send(enc.encrypt(msg))

        checker = self.client_socket.recv(1024)
        checker = enc.decrypt(checker)
        checker = checker.rstrip()
        checker = checker.upper()
        while (assigning):
            if checker == 'Y':
                msg = 'Enter a user to assign to :'
                msg = enc.encrypt(msg)
                self.client_socket.send(msg)
                assignTo = self.client_socket.recv(1024)
                assignTo = enc.decrypt(assignTo)
                assignTo = assignTo.rstrip()
                print(assignTo)
                db_interaction.assignUser(interviewID, assignTo)
                assigning = False
            elif checker == 'N':
                assigning = False
                break
            else:
                msg = "Invalid Response!"
                self.client_socket.send(enc.encrypt(msg))

        msg = "End of Interview"
        self.client_socket.send(enc.encrypt(msg))

    def assignInterview(self):
        global enc
        greetingString = "Welcome to the interview assigner!"
        greetingString = enc.encrypt(greetingString)
        self.client_socket.send(greetingString)
        time.sleep(0.05)
        msg = 'Enter a interview number to assign :'
        msg = enc.encrypt(msg)
        self.client_socket.send(msg)
        time.sleep(0.05)
        interviewID = self.client_socket.recv(1024)
        interviewID = enc.decrypt(interviewID)
        interviewID = interviewID.rstrip()

        userAssigned = db_interaction.checkIntAssigned(interviewID)
        if (userAssigned == None):
            msg = 'Enter a user to assign to :'
            msg = enc.encrypt(msg)
            self.client_socket.send(msg)
            assignTo = self.client_socket.recv(1024)
            assignTo = enc.decrypt(assignTo)
            assignTo = assignTo.rstrip()
            print(assignTo)
            if (db_interaction.getUserInterviewID(assignTo) == None):
                db_interaction.assignUser(interviewID, assignTo)
            else:
                msg = 'This user already has an interview assigned to them. Are you sure you want to assign a different interview (Y/N)?'
                self.client_socket.send(enc.encrypt(msg))

                checker = self.client_socket.recv(1024)
                checker = enc.decrypt(checker)
                checker = checker.rstrip()
                checker = checker.upper()
                assigning = True
                while (assigning):
                    if checker == 'Y':
                        db_interaction.assignUser(interviewID, assignTo)
                        assigning = False
                    elif checker == 'N':
                        msg = "End of assigning process"
                        self.client_socket.send(enc.encrypt(msg))
                        assigning = False
                        break
                    else:
                        msg = "Invalid Response!"
                        self.client_socket.send(enc.encrypt(msg))
        else:
            msg = (
                'This interview is already assigned to user {}. Would you like to assign a different interview (Y/N)?'.
                format(userAssigned))
            self.client_socket.send(enc.encrypt(msg))
            checker = self.client_socket.recv(1024)
            checker = enc.decrypt(checker)
            checker = checker.rstrip()
            checker = checker.upper()
            assigning = True
            while (assigning):
                if checker == 'Y':
                    self.assignInterview()
                    assigning = False
                elif checker == 'N':
                    msg = "End of assigning process"
                    self.client_socket.send(enc.encrypt(msg))
                    assigning = False
                else:
                    msg = "Invalid Response!"
                    self.client_socket.send(enc.encrypt(msg))

        msg = "End of assigning process"
        self.client_socket.send(enc.encrypt(msg))

    def validate(self):
        # KH -- EXCISED PER LICENSING RESTRICTION
        pass

    def terminate_session(self):
        global enc
        print('Terminating connection on', self.client_socket)
        logger.info('connection terminated: {}'.format(self.client_socket))
        sys.stdout.flush()
        for i in range(0, 10):
            print('.', end='')
            sys.stdout.flush()
            time.sleep(0.15)
        self.client_socket.close()
        print('Socket closed')
        sys.stdout.flush()

    def key_exchange(self):
        dif = diffieHellman()
        other_key = self.client_socket.recv(2048).decode()
        other_key = int(other_key)
        self.client_socket.send(str(dif.publicKey).encode())
        key = dif.genKey(other_key)
        return key

    def run(self):
        global enc
        key = self.key_exchange()
        enc = Encrypt(key)
        self.client_socket.send(
            enc.encrypt(('Welcome to the Interview Portal')))
        time.sleep(0.1)
        _LOGIN_STATUS = self.validate()
        if _LOGIN_STATUS == True:
            print('User', self._USER_NAME, 'has a log in status of',
                  str(_LOGIN_STATUS))
            logger.info('User {} has a login status of {}'.format(
                self._USER_NAME, str(_LOGIN_STATUS)))
        else:
            logger.warning('Invalid login attempt with username {}'.format(
                self._USER_NAME))
            CredentialsException()
            self.terminate_session()
            return
        ##This assumes that the user is trying to take an interview. Additional##
        ##user options could be added easily by making the giveInterview call  ##
        ##conditional
        user_role = self.currentuser.getPer()
        self.client_socket.send(
            enc.encrypt(
                str('{}'.format(db_interaction.getUserRole(user_role)))))

        if (user_role == 4):
            self.giveInterview()
        elif (user_role == 1):
            self.adminMenu()
        elif (user_role == 2):
            self.adminMenu()
        elif (user_role == 3):
            self.reviewInterview()

        self.terminate_session()
