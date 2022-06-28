import mysql.connector
from datetime import datetime

from database.base_db import BaseDatabase
from utils.utils import Utils


class Database(BaseDatabase):

    def __init__(self):
        super().__init__()

    def logout(self, username):
        query = "update user set is_logged_in = %s where username = %s"
        self.cursor.execute(query, (False, username))
        self.db_conn.commit()
        return

    def is_user_logged_in(self, username: str):
        query = "select is_logged_in from user where username = %s"
        self.cursor.execute(query, (username,))
        res = self.cursor.fetchall()
        if not res:
            raise Exception(f"there is not user {username}")
        else:
            if res[0][0] == 1:
                return True
        return False

    def do_login(self, username, password):
        query = "select password from user where username = %s"
        self.cursor.execute(query, (username,))
        res = self.cursor.fetchall()
        if res[0][0] == password:
            query = "update user set is_logged_in = %s where username = %s"
            self.cursor.execute(query, (True, username,))
            self.db_conn.commit()
            return True, f"{username} is logged in successfull"
        else:
            return False, f"Wrong password for user {username}"

    def insert_log(self, log_message: str):
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        res = self.cursor.execute('insert into log (message, time) values(%s, %s)', (log_message, formatted_date))
        self.db_conn.commit()
        return res

    def insert_user(self, username, password, question, question_ans, fname
                    , lname, phone, email):
        self.cursor.execute(
            "insert into user (first_name, last_name, phone, email, "
            "username,password,security_question,sec_question_answer,is_logged_in ) values ( %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                fname, lname, phone, email, username, password, question, question_ans, False
            ))
        self.db_conn.commit()
