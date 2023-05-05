import mysql.connector
import mysql.connector.errorcode as MYSQL_errorcodes

import random

from dotenv import load_dotenv
from mysql.connector import Error as MYSQL_ERROR

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
    
    else:
        print(f'{err} occoured')

def close_conn():
    if userdb.is_connected():
        cursor.close()
        userdb.close()
        

class Student:
    def __init__(self, username, passw:str, board, target, userclass, email, DOB):
        self.id = 0
        self.username = username
        self.passw = passw
        self.board = board
        self.target=target
        self.user_class = userclass
        self.email = email
        self.DOB = DOB

        user = search_user_with_email(email=self.email)
        if user[0] == False:
            if (input("student does not exist do you want to make new student? y/n: ").lower() == 'y'):
                add_user(username = self.username, 
                         passwhash = str(hashlib.md5(self.passw.encode("utf-8")).hexdigest()), 
                         board = self.board, 
                         target = self.target, 
                         userclass = self.user_class, 
                         email = self.email, 
                         DOB = self.DOB)
                
                self.id = search_user_with_email(self.email)[1]
            else:
                return
        else:
            self.id = user[1]

def add_user(username:str, passwhash:str, board:str, target:str, userclass:int, email:str, DOB:str):
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

    
def search_user_with_email(email):
    count = 0
    cursor.execute("SELECT id from users WHERE email = %s", (email,))
    searchresult = cursor.fetchall()
    for x in searchresult:
        print(x)
        count += 1
    if count>=1:
        return (True, searchresult)
    else:
        return (False, [])

def delete_user(email):
    cursor.execute("DELETE FROM `users` WHERE (email=%s)", (email,))
    userdb.commit()

def fetch_user_data(email):
    cursor.execute("SELECT * from users where (email = %s)", (email, ))
    students = cursor.fetchall()
    print(students)

if __name__ == "__main__":
    Student('MrBlue', '1234', 'CBSE', 'JEE', 12, 'debojyotiganguly70@gmail.com','24/01/2006')
    fetch_user_data('debojyotiganguly70@gmail.com')

    if(input("test_delete: ").lower() == "y"):
        delete_user('debojyotiganguly70@gmail.com')
    close_conn()
