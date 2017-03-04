'''LogIn Page'''
from flask import Flask, session, redirect, url_for, escape, request, render_template
from hashlib import md5
import MySQLdb

app = Flask(__name__)

if __name__ == '__main__':
    dataBase = MySQLdb.connect(host="localhost", user="root", passwd="", dataBase="test")
    cr = dataBase.cursor()
    app.secret_key = ''''the secret key'''

class ServerError(Exception):pass

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('login'))

    username_session = escape(session['username']).capitalize()
    return render_template('index.html', session_user_name=username_session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    error = None
    try:
        if request.method == 'POST':
            username_form  = request.form['username']
            cr.execute("SELECT COUNT(1) FROM users WHERE name = {};"
                        .format(username_form))

            if not cr.fetchone()[0]:
                raise ServerError('Invalid username')

            password_form  = request.form['password']
            cr.execute("SELECT pass FROM users WHERE name = {};"
                        .format(username_form))

            for row in cr.fetchall():
                if md5(password_form).hexdigest() == row[0]:
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))

            raise ServerError('Invalid password')
    except ServerError as e:
        error = str(e)

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


