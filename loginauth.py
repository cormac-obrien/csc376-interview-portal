import sys
import hashlib
import getpass
import sqlite3
from passlib.hash import sha256_crypt

class LoginAuthentication:

    def passcheck(user_input):

        password = "abc"

        pass_try = 0
        x = 3
        if user_input == password:
            print('User is logged in!\n')
            return
        elif user_input != password:
            pass_try += 1
        while (pass_try < x):
            user_input = str(input("Password: "))
            if user_input != password:
                pass_try += 1
                print('Incorrect Password, ' + str(x - pass_try) + ' more attempts left\n')
            else:
                pass_try = x + 1

        if pass_try == x and user_input != password:
            sys.exit('Incorrect Password, terminating... \n')

        print ('User is logged in!\n')


    def pass_crypt(str):

        hash_pass = sha256_crypt.encrypt(str)
        return hash_pass

    def pass_verify(str, db_pass):

        varify_pass = sha256_crypt.verify(str, db_pass)
        return varify_pass


    def passstore(self,password):
        def main(argv):

            if input('The file ' + sys.argv[
                1] + ' will be erased or overwrite if exsting.\nDo you wish to continue (Y/n): ') not in ('Y', 'y'):
                sys.exit('\nChanges were not recorded\n')

            user_name = input('Please Enter a User Name: ')
            password = hashlib.sha224(getpass.getpass('Please Enter a Password: ')).hexdigest()

            try:
                file_conn = open(sys.argv[1], 'w')
                file_conn.write(user_name + '\n')
                file_conn.write(password + '\n')
                file_conn.close()
            except:
                sys.exit('There was a problem writing to the file!')

            print
            ('\nPassword safely stored in ' + sys.argv[1] + '\n')

    def login(self, username, password):

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Login WHERE username == ? AND password == ?", (username, password))

        user = cursor.fetchone()
        if user is None:
            return False
        elif user[0] == username:
            return True
        else:
            return 0


    def register(self, username, password, authkey):
        self.lock.acquire()
        created = False
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO Login(username, password, authkey) VALUES(?,?,?)", (username, password, authkey))
            self.conn.commit()
            created = True

        except sqlite3.Warning:
            print('unsucessful')
        except Exception as e:
            print('Exception in register:', e)
        finally:
            self.lock.release()
            return created