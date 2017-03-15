# CO
import sqlite3


def add_user(conn, name, pass_hash, perms):
    '''Add a new user with the specified username, password hash, and
    permissions.
    '''

    curs = conn.cursor()
    curs.execute('INSERT INTO Users (user_name, user_password, user_perms) VALUES (?, ?)', (name, pass_hash, perms))
    curs.close()
    conn.commit()


def delete_user(conn, user_id):
    '''Delete the user with the given ID.'''

    curs = conn.cursor()
    curs.execute('DELETE FROM Users WHERE user_id = ?', (user_id))
    curs.close()
    conn.commit()

def retrieve_user_auth(conn, user_id):
    '''Retrieve the user ID of the user with the given name.'''
    curs = conn.cursor()
    curs.execute('SELECT user_perms FROM Users WHERE user_id = ?', (user_id,))
    user_perms = curs.fetchone()[0]
    curs.close()
    conn.commit()
    return user_perms

def update_user_auth(conn, user_id, user_perms ):
    curs = conn.cursor()
    interviews = curs.execute('UPDATE Users set user_perms = ? where user_id = ?',
        (user_perms, user_id)) 
    curs.close()
    conn.commit()

def retrieve_user_name(conn, user_id):
    '''Retrieve the username of the user with the given ID.'''

    curs = conn.cursor()
    curs.execute('SELECT user_name FROM Users WHERE user_id = ?', (user_id))
    username = curs.fetchone()[0]
    curs.close()
    conn.commit()
    return username

def retrieve_user_all(conn):
    '''Retrieve all the users ID's and Names'''
    list_users = []
    curs = conn.cursor()
    users = curs.execute('SELECT user_id, user_name FROM Users')
    for user in users:
        user_name = str(user[1])
        user_id = str(user[0])
        list_users.append((user_name, user_id))
    conn.commit()
    return list_users

def retrieve_user_by_name(conn, username):
    '''Retrieve the user ID of the user with the given name.'''

    curs = conn.cursor()
    curs.execute('SELECT user_id FROM Users WHERE user_name = ?', (username,))
    user_id = curs.fetchone()[0]
    curs.close()
    conn.commit()
    return user_id

def retrieve_user_all(conn):
    '''Retrieve all the users ID's and Names'''
    list_users = []
    curs = conn.cursor()
    users = curs.execute('SELECT user_id, user_name FROM Users')
    for user in users:
        user_name = str(user[1])
        user_id = str(user[0])
        list_users.append(("Username: " + user_name, "ID: " + user_id))
    conn.commit()
    return list_users


def retrieve_user_auth(conn, user_id):
    '''Retrieve the user ID of the user with the given name.'''

    curs = conn.cursor()
    curs.execute('SELECT user_perms FROM Users WHERE user_id = ?', (user_id,))
    user_perms = curs.fetchone()[0]
    curs.close()
    conn.commit()
    return user_perms

def create_interview(conn, interview_id, name, description, user):
    '''Create a new interview with the given name and description.'''

    curs = conn.cursor()
    curs.execute('INSERT INTO Interviews VALUES (?, ?, ?, ?)',
                 (interview_id, name, description, user))
    curs.close()
    conn.commit()


def delete_interview(conn, interview_id):
    '''Delete the interview with the given ID.

    This will also delete any questions where question_interview =
    interview_id.
    '''

    curs = conn.cursor()
    curs.execute('DELETE FROM Interviews WHERE interview_id = ?',
                 (interview_id,))
    curs.execute('DELETE FROM Questions WHERE question_interview = ?',
                 (interview_id,))
    conn.commit()


def retrieve_interview_title(conn, interview_id):
    '''Retrieve the title of the interview with the given ID.'''

    curs = conn.cursor()
    curs.execute('''SELECT interview_name FROM Interviews
                      WHERE interview_id = ?''',
                 (interview_id,))
    title = curs.fetchone()[0]
    curs.close()
    conn.commit()
    return title


def retrieve_interview_all(conn):
    '''Retrieve all the Interview ID's and Names'''
    list_interview = []
    curs = conn.cursor()
    interviews = curs.execute('SELECT interview_id, interview_name FROM Interviews')
    for interview in interviews:
        interview_name = str(interview[1])
        interview_id = str(interview[0])
        list_interview.append((interview_name, interview_id))
    conn.commit()
    return list_interview

def retrieve_interview_by_user(conn,interview_user):
    '''Retrieve all the Interview ID's and Names'''
    list_interview = []
    curs = conn.cursor()
    interviews = curs.execute('SELECT DISTINCT interview_id, interview_name FROM Interviews WHERE interview_user = ?',
     (interview_user,))
    for interview in interviews:
        interview_name = str(interview[1])
        interview_id = str(interview[0])
        list_interview.append((interview_id, interview_name))
    conn.commit()
    return list_interview

def assign_interview(conn, interview_id, interview_user):
    curs = conn.cursor()
    curs.execute('UPDATE Interviews set interview_user = ? where interview_id = ?',
                 (interview_user, interview_id))
    curs.close()
    conn.commit()


def add_question(conn, question_id, interview, text, sequence_number):
    '''Add a new question with the given text to the given interview.'''

    curs = conn.cursor()
    curs.execute('INSERT INTO Questions VALUES (?, ?, ?, ?)',
                 (question_id, interview, text, sequence_number))
    curs.close()
    conn.commit()


def delete_question(conn, question_id):
    '''Delete the question with the given ID.'''

    curs = conn.cursor()
    curs.execute('DELETE FROM Questions WHERE question_id = ?', (question_id))
    curs.execute('DELETE FROM Answers WHERE answer_question = ?',
                 (question_id))
    curs.close()
    conn.commit()


def retrieve_question(conn, question_id):
    '''Retrieve the question with the given ID.'''

    curs = conn.cursor()
    curs.execute('SELECT question_text FROM Questions WHERE question_id = ?', (question_id,))
    text = curs.fetchone()[0]
    curs.close()
    conn.commit()
    return text


#def retrieve_questions(conn, interview_id):
   # curs = conn.cursor()
   # questions = curs.execute('''SELECT question_text, question_sequence, question_id
   #                               FROM Questions
   #                               WHERE question_interview = ?
   #                               ORDER BY question_sequence ASC''',
   #                          (interview_id,))
   # conn.commit()
   # return questions

def retrieve_questions(conn, interview_id):
    '''Retrieve all the users ID's and Names'''
    list_questions = []
    curs = conn.cursor()
    questions = curs.execute('''SELECT question_text, question_sequence, question_id
                                  FROM Questions
                                  WHERE question_interview = ? 
                                  ORDER BY question_sequence ASC''', (interview_id,))
    list_questions = []
    for question in questions:
        question_text = str(question[0])
        question_sequence = str(question[1])
        question_id = str(question[2])
        list_questions.append((question_sequence + ".) " + question_text + " || Question ID: " +question_id))
    conn.commit()

    return list_questions


def add_answer(conn, user_id, question_id, text, interview_id):
    '''Add an answer by user_id to question_id with the given text.'''

    curs = conn.cursor()
    curs.execute('''INSERT INTO Answers (answer_user, answer_question, answer_text, answer_interview)
                      VALUES (?, ?, ?, ?)''', (user_id, question_id, text, interview_id))
    curs.close()
    conn.commit()


def delete_answer(conn, answer_id):
    '''Delete the answer with the given ID.'''

    curs = conn.cursor()
    curs.execute('DELETE FROM Answers WHERE answer_id = ?', (answer_id))
    curs.close()
    conn.commit()


def retrieve_answer(conn, user_id, question_id):
    '''Retrieve the given user's answer to the given question.'''

    curs = conn.cursor()
    curs.execute('''SELECT answer_text FROM Answers
                      WHERE answer_user = ?
                      AND answer_question = ?''',
                 (user_id, question_id))
    ans = curs.fetchone()[0]
    curs.close()
    conn.commit()
    return ans

def retrieve_answers(conn, user_id, interview_id):
    '''Retrieve the given user's answer to the given question.'''

    curs = conn.cursor()
    curs.execute('''SELECT answer_text FROM Answers
                      WHERE answer_user = ?
                      AND answer_question = ?''',
                 (user_id, question_id))
    ans = curs.fetchone()[0]
    curs.close()
    conn.commit()
    return ans

#Kevin
def retrieve_answer_id_by_question(conn, user_id, question_id):
    '''retrieve answer id of the question id and user id gevin'''
    curs = conn.cursor()
    curs.execute('SELECT answer_id FROM Answers WHERE answer_user = ? AND answer_question = ?', (user_id, question_id))
    answer_id = curs.fetchone()[0]
    curs.close()
    conn.commit()
    return answer_id

def retrieve_interview_by_answer(conn, answer_user):
    '''Retrieve name of interviews for a spacific user'''
    curs = conn.cursor()
    interviews = curs.execute('SELECT DISTINCT answer_interview FROM Answers WHERE answer_user = ?', (answer_user,))
    conn.commit()
    return interviews
    
#Kevin
def update_answer(conn, answer_text, answer_id):
    '''Add an answer by user_id to question_id with the given text.'''
    curs = conn.cursor()
    curs.execute('UPDATE Answers set answer_text = ? where answer_id = ?', (answer_text, answer_id))
    curs.close()
    conn.commit()
# CO
