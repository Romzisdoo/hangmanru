import sqlite3
import time
import math
import re
from flask import url_for

class methodsMyApp:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def add_user(self, name, surname, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM hangman_users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count']>0:
                print("Vartotojas su tokiu el. paštu jau yra registruotas")
                return False

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO hangman_users VALUES (NULL, ?, ?, ?, ?, ?)", (name, surname, email, hpsw, tm)) 
            self.__db.commit()
    
        except sqlite3.Error as e:
            print("Klaida įvedant vartotoją" + str(e))
            return False
        return True

    def get_user(self, user_id):
        try:
            self.__cur.execute(f"SELECT *FROM hangman_users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Vartotojas nerastas")
                return False

            return res
        except sqlite3.Error as e:
            print("Gavome klaidą gaunant duomenis iš duomenų bazės" + str(e))

        return False

    def get_user_by_email(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM hangman_users WHERE email =  '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Nerandama vartotojo")
                return False

            return res
        except sqlite3.Error as e:
            print("Klaida gaunant duomenis iš DB" + str(e))

        return False