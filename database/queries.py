
from datetime import datetime

from database.base_db import BaseDatabase



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
            self.login_wrong_try(username)
            return False, f"Wrong password for user {username}"

    def login_wrong_try(self, username):
        query_set = "update user set try_count = try_count + 1 where username = %s"
        self.cursor.execute(query_set, (username,))
        self.db_conn.commit()

    def is_user_banned(self, username):
        query_set = "select try_count from user where username = %s"
        self.cursor.execute(query_set, (username,))
        res = self.cursor.fetchall()
        return res[0][0] >= 3

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

    def find_by_username(self, search_value: str):
        query_str = f"SELECT first_name , last_name, username FROM user WHERE username LIKE '%{search_value}%' "
        self.cursor.execute(query_str)
        res = self.cursor.fetchall()

        return res

    def create_friendship_request(self, from_user, to_user):
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        query_str = "insert into friendship_request (from_user_id , to_user_id , time) values ( %s, %s , %s )"
        self.cursor.execute(query_str, (from_user, to_user, formatted_date))
        self.db_conn.commit()

    def get_friendship_requests(self, username):
        query_str = "select from_user_id from friendship_request where to_user_id = %s "
        self.cursor.execute(query_str, (username,))
        res = self.cursor.fetchall()
        return res

    def delete_friendship_request(self, from_user, to_user):
        query_str = "delete from friendship_request where from_user_id = %s and to_user_id = %s"
        self.cursor.execute(query_str, (from_user, to_user))
        self.db_conn.commit()

    def accept_friendship(self, from_user, to_user):
        query_str = "insert into friendship (from_user_id , to_user_id) values ( %s , %s)"
        self.cursor.execute(query_str, (from_user, to_user))
        self.db_conn.commit()
        return

    def check_is_there_friendship(self, from_user, to_user):
        query_str = "select count(*) from friendship where from_user_id= %s and to_user_id=%s"
        self.cursor.execute(query_str, (from_user, to_user))
        res = self.cursor.fetchall()
        if len(res):
            return res[0][0] == 1

    def insert_messgae(self, from_user, to_user, message):
        # insert message to Message Relation
        # insert to sending Relation
        # insert into receinving Relation
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

        query_set = "insert into message (text, is_seen, is_liked) values (%s, %s, %s)"
        self.cursor.execute(query_set, (message, False, False))
        self.db_conn.commit()

        msg_id = self.cursor.lastrowid

        query_set = "insert into sending(msg_datetime,message_id,sender_id) values(%s,%s,%s)"
        self.cursor.execute(query_set, (formatted_date, msg_id, from_user))
        self.db_conn.commit()

        query_set = "insert into receiving(msg_datetime,message_id,receiver_id) values(%s,%s,%s)"
        self.cursor.execute(query_set, (formatted_date, msg_id, to_user))
        self.db_conn.commit()

    def get_unread_messages(self, username):

        query_set = "select m.id , m.text ,r.msg_datetime  from receiving as r  inner join  message as m on m.id = r.message_id where r.receiver_id = %s and m.is_seen = %s order by r.msg_datetime "
        self.cursor.execute(query_set, (username, False))
        res = self.cursor.fetchall()

        return res

    def get_read_messages(self, username):
        query_set = "select r.message_id  , m.text , r.msg_datetime from receiving as r  inner join message as m on m.id = r.message_id where r.receiver_id = %s and m.is_seen = %s order by r.msg_datetime "
        self.cursor.execute(query_set, (username, True))
        res = self.cursor.fetchall()

        return res

    def get_all_messages(self, username):
        data = {}
        data["Unread_messages"] = self.get_unread_messages(username)
        data["Read_messages"] = self.get_read_messages(username)
        return data

    def get_friendship(self, username):
        query_set = "select to_user_id from friendship where from_user_id = %s"
        self.cursor.execute(query_set, (username,))
        res = self.cursor.fetchall()
        return res

    def do_like(self, message_id):
        query_set = "update message set is_seen = %s where id = %s"
        self.cursor.execute(query_set, (True, message_id,))
        self.db_conn.commit()

        query_set = "update message set is_liked = %s where id = %s"
        self.cursor.execute(query_set, (True, message_id,))
        self.db_conn.commit()

    def get_message_receiver(self, message_id):
        query_set = "select receiver_id from receiving where message_id = %s"
        self.cursor.execute(query_set, (message_id,))
        res = self.cursor.fetchall()
        if len(res):
            return res[0][0]

    def delete_friendship(self, username, target_user_to_delete):
        query_set = "delete from friendship where from_user_id = %s and to_user_id = %s"
        self.cursor.execute(query_set, (target_user_to_delete, username,))
        self.db_conn.commit()

    def block_user(self, username, target_user):
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            query_set = "insert into block (from_user_id , to_user_id , blocking_datetime) values(%s , %s , %s)"
            self.cursor.execute(query_set, (username, target_user, formatted_date,))
            self.db_conn.commit()
        except Exception as e:
            pass

    def unblock_user(self, username, target_user):
        query_set = "delete from  block where from_user_id = %s and  to_user_id = %s "
        self.cursor.execute(query_set, (username, target_user,))
        self.db_conn.commit()

    def is_user_blockd(self, username, from_user):
        query_set = "select count(*) from block where from_user_id = %s and to_user_id = %s"
        self.cursor.execute(query_set, (from_user, username,))
        res = self.cursor.fetchall()
        if len(res):
            return res[0][0] == 1

    def delete_account(self, username):
        query_set = "delete from user where username = %s "
        self.cursor.execute(query_set, (username))
        self.db_conn.commit()
