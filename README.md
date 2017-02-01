# Interview Portal
/*
 * Copyright 2016. DePaul University. All rights reserved. 
 * This work is distributed pursuant to the Software License
 * for Community Contribution of Academic Work, dated Oct. 1, 2016.
 * For terms and conditions, please see the license file, which is
 * included in this distribution.
 */

CSC 376 Distributed Systems
Fall 2016-2017
DePaul University
Karen Heart, Instructor

Project: Structured Interviews

# Usage

## RUNNING THE APPLICATIONS

Server : python3 interview_portal_server {port}
Client : python3 interview_portal_client {host} {port}

## How to create an Interview:
1. sign into the client portal lawyer permissions or higher
2. select 1 and press enter 
3. enter the name of the interview and press enter
4. enter a question, then an answer. if you would like to add more than one answer type 'Y' and press enter
5. when you are finished adding the questions you can assign the interview to a user by entering 'Y'

## How to take an Interview:
1. sign into the client portal with interviewee permissions using the username and password given
2. the assigned interview should show up with the first question. 
3. Answer by typing one of the letter options shown and pressing enter
3. continue answering the questions until the interview ends and you are logged out
4. the program will automatically save your answers and will be available to the lawyer who assigned it for a later date

## How to assign an Interview:
1. log into the client portal with lawyer permissions
2. select option 3
3. enter the interview ID number you would like to assign
4. if the interview you wish to assign is already taken you have to option to assign a different interview

## How to review an Interview:
1. log in with the correct credentails
2. select option 2
3. enter the username of the interviewee you would like to view the interview for

![alt tag](ProgramDiagram.png?raw=true "Optional Title")

# Documentation

### **User(** *UserID, UserName, UserRoleID, InterviewID* **)**
A basic user class that is used to model our User table in our database

**\__str\__()** > return String

**getID()** > return UserID

**getName()** > return UserName

**getPer()** > return UserRoleID

**getIntID()** > return InterviewID


### **Question(** *QuestionID, QuestionText, Answers* **)**
A basic question class that is used to model our Question table in our database

**\__str\__()** > return String

**getQuestionId()** > return QuestionID

**getQuestionText()** > return QuestionText

**getAnswers()** > return Answers

**getAnswer()** > return String

**putAnswer()**

**answerQuestion()**

**getUserAnswer()** > return String


### **Answer(** *AID, Answer* **)**
A basic answer class that is used to model our Answer table in our database

**\__str\__()** > return String

**getAnswerText()** > return Answer

**getAnswerID()** > return AID


### **Interview(** *IntID, Title, NumQs* **)**
A basic interview class that is used to model our Interview table in our database

**getIntID()** > return IntID

**getName()** > return Title

**getNumQs()** > return NumQs

### **ActiveInterview(** *InterviewID, InterviewName, Questions* **)**
An active interview class that is used keep an active interview in session

**putQuestion()**

**getInterviewID()** > return InterviewID

**getInterviewName()** > return InterviewName

**getQuestions()** > return Questions

**getQuestion()** > return Question()

**answerQuestion(** *AnswerID* **)**

**resetIter()**

**getNextQuestion(** *AnswerID* **)** return String

**\__str\__()** > return String


### **CredentialsException(** *Exception* **)**
A basic exception class to handle authentication exceptions

**startInterview(** *InterviewID* **)** raise CredentiasException()


### **diffieHellman()**
The diffie hellman key exchange class is an algorithm used to establish a shared secret between two parties. In our case the client and server.

**genRandom(** *bits* **)** > return Integer

**genKey(** *otherKey* **)** > return String


### **Encrypt(** *key* **)**
The encryption class takes a string 16, 24,or 32 digit key as a string and is converted to bytes by the constructor. Use by instantiating anEncrypt object with the key passed and callencrypt or decrypt with a string passed as msg.

**encrypt(** *message, key_size*, **)** > return byteString

**decrypt(** *ciphertext* **)** > return String
