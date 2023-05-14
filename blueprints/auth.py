from flask import Blueprint, request, jsonify, session, make_response
from models.user import User
from models.cam import Cam
from exts import db as datebase

db = Blueprint("auth", __name__, url_prefix='/user')

@db.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    username = data['username']
    password = data['password']
    manager = User.query.filter(User.username == username).first()
    if manager != None:
        if manager.password != password:
            return jsonify({
                "errno": 1,
                "errmsg": '密码错误'
            })
        else:
            session["username"] = username
            return jsonify({
                "errno": 0,
                "errmsg": '',
            })
    else:
        return jsonify({
            "errno": 1,
            "errmsg": '用户不存在'
        })


@db.route("/session", methods=["POST"])
def check_session():
    user = session.get("username")
    if user:
        manager = User.query.filter(User.username == user).first()
        return jsonify({
            "errno": 0,
            "errmsg": '',
            "data": manager.to_json()
        })
    else:
        return jsonify({
            "errno": 1,
            "errmsg": '用户未登录',
        })


@db.route("/logout", methods=["DELETE"])
def logout():
    session.pop("username")
    return jsonify(msg="退出登录成功")

@db.route('/adduser', methods=['POST'])
def addUser():
    data = request.get_json(silent=True)
    username = data.get('username')
    password = data.get('password')
    state = data.get('state')
    name = data.get('name')
    sex = data.get('sex')
    birth = data.get('birth')
    telephone = data.get('telephone')
    mailbox = data.get('mailbox')
    userpic = data.get('userpic')

    curr = User.query.filter(User.username == username).first()
    if curr != None:
        return {
            "errno": 1,
            "errmsg": '用户名已存在!'
        }
    else:
        curr = User.query.filter(User.mailbox == mailbox).first()
        if curr !=None:
            return {
                "errno": 1,
                "errmsg": '邮箱已存在!'
            }
    user = User(username=username, password=password, state=state, name=name, sex=sex, telephone=telephone, mailbox=mailbox, userpic=userpic, birth=birth)
    datebase.session.add(user)
    datebase.session.commit()

    return {
        "errno": 0,
        "errmsg":''
    }

