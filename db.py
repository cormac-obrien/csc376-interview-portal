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


def create_interview(conn, name, description):
    '''Create a new interview with the given name and description.'''

    curs = conn.cursor()
    curs.execute('INSERT INTO Interviews (interview_name, interview_description) VALUES (?, ?)', (name, description))
    curs.close()
    conn.commit()


def delete_interview(conn, interview_id):
    '''Delete the interview with the given ID.

    This will also delete any questions where question_interview =
    interview_id.
    '''

    curs = conn.cursor()
    curs.execute('DELETE FROM Interviews WHERE interview_id = ?',
                 (interview_id))
    curs.execute('DELETE FROM Questions WHERE question_interview = ?',
                 (interview_id))
    curs.close()
    conn.commit()


def add_question(conn, interview, text):
    '''Add a new question with the given text to the given interview.'''

    curs = conn.cursor()
    curs.execute('INSERT INTO Questions (question_interview, question_text) VALUES (?, ?)', (interview, text))
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


def add_answer(conn, user_id, question_id, text):
    '''Add an answer by user_id to question_id with the given text.'''

    curs = conn.cursor()
    curs.execute('INSERT INTO Answers (answer_user, answer_question,) VALUES (?, ?, ?)', user_id, question_id, text)
    curs.close()
    conn.commit()


def delete_answer(conn, answer_id):
    '''Delete the answer with the given ID.'''

    curs = conn.cursor()
    curs.execute('DELETE FROM Answers WHERE answer_id = ?', (answer_id))
    curs.close()
    conn.commit()


if __name__ == '__main__':
    conn = sqlite3.connect('interview.db')
