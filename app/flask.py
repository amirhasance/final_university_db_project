from http.client import HTTPResponse

from flask import Flask
from flask import request
from flask import jsonify
from flask_restful import Api, Resource, reqparse

from database.queries import Database
from logic.logic import AppLogic

app = Flask(__name__)
api = Api(app)

logic_obj = AppLogic()



@app.route("/register", methods=["POST"])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    question = request.form.get('question')
    question_ans = request.form.get('question_ans')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    phone = request.form.get('phone')
    email = request.form.get('email')
    success, message = logic_obj.register(username, password, question, question_ans, fname
                                          , lname, phone, email)

    data = {
        "msg": message,
        "success": success
    }
    return jsonify(data)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    success, msg = logic_obj.login(username, password)
    data = {
        "msg": msg,
        "success": success
    }
    return jsonify(data)


@app.route("/logout", methods=["POST"])
def logout():
    username = request.form.get('username')
    success, msg = logic_obj.logout(username)
    data = {
        "msg": msg,
        "success": success
    }
    return jsonify(data)


@app.route("/find", methods=["POST"])
def find():
    username = request.form.get('username')
    wanted_username = request.args.get('wanted_username')
    found, users = logic_obj.find_users(wanted_username)
    data = {
        "found": found,
        "users": users
    }
    return jsonify(data)


@app.route("/freindship_request", methods=["POST"])
def send_freindship_request():
    username = request.form.get('username')
    target_user = request.args.get("target_user")
    msg = logic_obj.create_friendship_request(username, target_user)
    data = {
        "msg": msg
    }
    return jsonify(data)


@app.route("/frindship_request", methods=["GET"])
def get_friendship_request():
    username = request.form.get('username')
    all_request = logic_obj.get_friendship_request(username)
    data = {
        "your_follow_requests are ": all_request
    }
    return jsonify(data)


@app.route("/accept_frinedship", methods=["POST"])
def accept_friendship():
    username = request.form.get('username')
    follower = request.form.get("follower")
    msg = logic_obj.accept_friendship(username, follower)

    return jsonify({"msg": msg})


@app.route("/do_block", methods=["POST"])
def do_block():
    username = request.form.get('username')
    target_user = request.form.get("follower")






def app_run():
    app.run(host="0.0.0.0")
