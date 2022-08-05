import datetime
import json

from database.queries import Database
from utils.utils import Utils


class AppLogic:
    db_obj = Database()

    def __init__(self):
        pass

    def login(self, username, password):
        try:
            if self.db_obj.is_user_banned(username):
                return False, "Ooops :/ ! Maximum attemp to login :/"
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
        return False, "you were not logged in"


    def find_by_username(self, username, search_value):
        if self.db_obj.is_user_logged_in(username):
            users = self.db_obj.find_by_username(search_value)
            if len(users):
                return True, users

        return False, None

    def create_friendship_request(self, from_username, to_username):

        if self.db_obj.is_user_logged_in(from_username):
            if self.db_obj.is_user_blockd(from_username, to_username):
                return "WTF , You Are blocked A"
            self.db_obj.create_friendship_request(from_username, to_username)
            self.do_log(f"friendship request is sent from {from_username} to {to_username}", "Info")
            return "successful"

    def get_friendship_requests(self, username):
        if self.db_obj.is_user_logged_in(username):
            res = self.db_obj.get_friendship_requests(username)
            self.do_log(f"get friendship reqeust of {username}", "Info")
            return res

    def accept_friendship(self, username, target_user):

        if self.db_obj.is_user_logged_in(username):
            self.db_obj.delete_friendship_request(target_user, username)
            self.db_obj.accept_friendship(target_user, username)
            self.do_log(f"{username} accepted freindship_request from {target_user}", "Info")
            return f"accepted request of {target_user}"

    def send_message(self, from_user, to_user, message_text):
        if self.db_obj.is_user_logged_in(from_user):
            if self.db_obj.is_user_blockd(from_user, to_user):
                return f"You are blocked and cannot send message to {to_user}"
            else:
                if self.db_obj.check_is_there_friendship(from_user, to_user):
                    self.db_obj.insert_messgae(from_user, to_user, message_text)
                    self.do_log(f"{from_user} send message to {to_user} , message = {message_text}", "Info")
                    return f"message sent to {to_user}"
                else:
                    return f"There is not Friendship to {to_user}"
        else:
            return "Your not Logged in :/"

    def do_block(self, username, target_user):
        # procedure , delete friendship and friendship reqeust and block user
        self.db_obj.block_user(username, target_user)
        self.db_obj.delete_friendship_request(target_user, username)
        self.db_obj.delete_friendship(target_user, username)
        self.db_obj.delete_friendship(username, target_user)
        self.do_log(f"{username} blocked {target_user}")
        return f"You blocked {target_user}"

    def do_unblock(self, username, target_usere):
        self.db_obj.unblock_user(username, target_usere)
        self.do_log(target_usere)
        return f"U unblocked {target_usere}"

    def get_messages(self, username):
        # read_messagess and unread ones , order by datetime
        if self.db_obj.is_user_logged_in(username):
            msg_list = self.db_obj.get_all_messages(username)
            return msg_list
        return "you are not logged in"

    def get_user_friend_list(self, username):
        if self.db_obj.is_user_logged_in(username):
            res = self.db_obj.get_friendship(username)
            return {"Your Friendship Network is ": res}
        return "you are not logged in"

    def delete_from_user_freind_list(self, username, target_user):
        if self.db_obj.is_user_logged_in(username):
            self.db_obj.delete_friendship(username, target_user)
            self.do_log(f"{username} deleted {target_user} from friend list ")
        return "you are not logged in"

    def do_like_message(self, username, message_id):
        if self.db_obj.is_user_logged_in(username):
            msg_receiver = self.db_obj.get_message_receiver(message_id)
            if msg_receiver == username:
                self.db_obj.do_like(message_id)
                self.do_log(f"{username} liked {message_id}")
                return f"Successfuly Like message {message_id}"
            else:
                return "you are not the reciver of this message"
        return "You are not logged in"

    def delete_user_account(self, username):
        if self.db_obj.is_user_logged_in(username):
            self.db_obj.delete_account(username)
            self.do_log(f"{username} has been deleted")
            return "You are deleted :/ . come back soon , we are missed of you"

    def delete_friendship(self, username, target_user):
        self.db_obj.delete_friendship(username, target_user)
        self.db_obj.delete_friendship(target_user, username)
        self.do_log(f"{username} deleted freindship of {target_user}")

    def do_log(self, msg, level=None):
        if level is None:
            level = "Info"
        log_data = {
            "time": str(datetime.datetime.now()),
            "level": level,
            "message": msg
        }
        print(log_data)
        self.db_obj.insert_log(json.dumps(log_data))
