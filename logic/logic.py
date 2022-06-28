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

    def find_by_username(self, username, search_value):
        if self.db_obj.is_user_logged_in(username):
            users = self.db_obj.find_by_username(search_value)
            if len(users):
                return True, users

        return False, None

    def create_friendship_request(self, from_username, to_username):
        if self.db_obj.is_user_logged_in(from_username):
            self.db_obj.create_friendship_request(from_username, to_username)
            self.do_log(f"friendship request is sent from {from_username} to {to_username}", "Info")
            return "successful"

    def get_friendship_requests(self, username):
        if self.db_obj.is_user_logged_in(username):
            res = self.db_obj.get_friendship_requests(username)
            self.do_log(f"get friendship reqeust of {username}", "Info")
            return res

    def accept_friendship(self, username, target_user):

        # if target_user in friendship_request model ->
        # delete it from this table and create a tuple  in friendship  talble
        if self.db_obj.is_user_logged_in(username):
            self.db_obj.delete_friendship_request(target_user, username)
            self.db_obj.accept_friendship(target_user, username)
            self.do_log(f"{username} accepted freindship_request from {target_user}", "Info")
            return f"accepted request of {target_user}"

    def send_message(self, from_user, to_user, message_text):
        if self.db_obj.is_user_logged_in(from_user):
            if self.db_obj.check_is_there_friendship(from_user, to_user):
                self.db_obj.insert_messgae(from_user, to_user, message_text)
                self.do_log(f"{from_user} send message to {to_user} , message = {message_text}", "Info")

    def do_block(self, username, target_user):

        pass

    def do_unblock(self, username, target_usere):
        pass

    def get_messages(self, username):
        # read_messagess and unread ones , order by datetime
        if self.db_obj.is_user_logged_in(username):
            msg_list = self.db_obj.get_all_messages(username)
            return msg_list
        pass

    def get_user_friend_list(self, username):
        if self.db_obj.is_user_logged_in(username):
            res = self.db_obj.get_friendship(username)
            return {"Your Friendship Network is ": res}

    def delete_from_user_freind_list(self, username, target_user):
        if self.db_obj.is_user_logged_in(username):
            self.db_obj.delete_friendship(username, target_user)

    def do_like_message(self, username, message_id):
        if self.db_obj.is_user_logged_in(username):
            msg_receiver = self.db_obj.get_message_receiver(message_id)
            if msg_receiver == username:
                self.db_obj.do_like(message_id)

    def delete_user_account(self, username):
        pass

    def do_log(self, msg, level):
        log_data = {
            "level": level,
            "message": msg
        }
        self.db_obj.insert_log(json.dumps(log_data))
