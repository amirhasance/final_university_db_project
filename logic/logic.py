import json

from database.queries import Database
from utils.utils import Utils


class AppLogic:
    db_obj = Database()

    def __init__(self):
        pass

    def login(self, username, password):
        try:
            if self.db_obj.is_user_logged_in(username):
                return False, "You are logged in with another account"

        except Exception as e:
            self.do_log(f"logging {username} ", "Error")
            return False, e.__str__()

        hashed_password = Utils.hash_string(password)
        try:
            success, res = self.db_obj.do_login(username, hashed_password)
            self.do_log(res, "Info")
            return success, res
        except Exception as e:
            self.do_log(e.__str__(), "Error")
            return False, e.__str__()

    def register(self, username, password, question, question_ans, fname
                 , lname, phone, email):
        hashed_password = Utils.hash_string(password)
        try:
            self.db_obj.insert_user(username, hashed_password, question, question_ans, fname, lname, phone, email)
            msg = f"user {username} registered successfully "
            self.do_log(msg, level="Info")
            return True, msg
        except Exception as e:
            self.do_log(e.__str__(), level="Error")
            return False, e.__str__()

    def logout(self, username):
        try:
            if not self.db_obj.is_user_logged_in(username):
                pass
            else:
                self.db_obj.logout(username)
                self.do_log(f"user {username} logged out successfully ", "Info")
            return True, "Logged out Successfully"
        except Exception as e:
            self.do_log(f"logouting user {username} with error =  {e.__str__()}", "Error")

    def create_friendship_request(self, from_username, to_username):
        msg = "request is send "
        return msg

    def get_friendship_request(self, username):
        frindship_requests = []
        return frindship_requests

    def accept_friendship(self, username, target_user):
        pass

    def do_block(self, username, target_user):
        pass

    def do_unblock(self, username, target_usere):
        pass

    def get_messages(self, username):
        # read_messagess and unread ones , order by datetime
        pass

    def get_user_friend_list(self, username):
        pass

    def delete_from_user_freind_list(self, username, target_user):
        pass

    def do_like_message(self, username, message_id):
        pass

    def delete_user_account(self, username):
        pass

    def do_log(self, msg, level):
        log_data = {
            "level": level,
            "message": msg
        }
        self.db_obj.insert_log(json.dumps(log_data))
