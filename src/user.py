import mysql.connector
import mysql.connector.errorcode as MYSQL_errorcodes

from mysql.connector import Error as MYSQL_ERROR
import random

from dotenv import load_dotenv

import os
import hashlib


load_dotenv()

try:
    userdb = mysql.connector.connect(host='localhost', user='root', password='1234', database='users')
    cursor = userdb.cursor()
    print('database already existed')
except MYSQL_ERROR as err:
    if err.errno == MYSQL_errorcodes.ER_BAD_DB_ERROR:
        userdb = mysql.connector.connect(host='localhost', 
                                         user=os.getenv('MYSQL_USER'), 
                                         password=os.getenv('MYSQL_USER_PASSW'))
        cursor = userdb.cursor()
        cursor.execute('CREATE DATABASE users')
        print('database created')
        print('created table')
    
    else:
        print(f'{err} occoured')

def close_conn():
    if userdb.is_connected():
        cursor.close()
        userdb.close()
        

class User:
    def __init__(self, username, passw:str, board, target, userclass, email, DOB):
        self.username = username
        self.passw = passw
        self.board = board
        self.target=target
        self.user_class = userclass
        self.email = email
        self.DOB = DOB

    def add_user(self, username, passwhash, board, target, userclass, email, DOB):
        try:    
            cursor.execute(
                "INSERT INTO users (id, name, passwhash, class, board, target, email, DOB) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                (random.choice(range(100000)), 
                username, 
                passwhash, 
                userclass, 
                board, 
                target, 
                email,
                DOB))
            
            userdb.commit()
            print(f'{cursor.rowcount} record inserted')
        except MYSQL_ERROR as err:
            if str(err) == f"1062 (23000): Duplicate entry '{email}' for key 'users.email_UNIQUE'":
                print(f'user with email "{email}" already exists')
            else:
                print(err)

    
    def search_user(self, email):
        count = 0
        cursor.execute("SELECT id from users WHERE email = %s", (email))
        searchresult = cursor.fetchall()

        for x in searchresult:
            print(x)
            count += 1

        if count>=1:
            return (True, searchresult)
        else:
            return (False, [])

if __name__ == "__main__":
    User('MrBlue', '1234', 'CBSE', 'JEE', 12, 'debojyotiganguly70@gmail.com','24/01/2006')
    close_conn()
    