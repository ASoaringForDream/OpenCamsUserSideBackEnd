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

@db.route('/edituser', methods=['POST'])
def editUser():
    data = request.get_json(silent=True)
    id = data.get('id')
    name = data.get('name')
    sex = data.get('sex')
    birth = data.get('birth')
    telephone = data.get('telephone')
    mailbox = data.get('mailbox')
    userpic = data.get('userpic')

    user = User.query.filter(User.id == id).first()
    if name != None:
        user.name = name
    if sex != None:
        user.sex = sex
    if birth != None:
        user.birth = birth
    if telephone != None:
        user.telephone = telephone
    if mailbox != None:
        curr = User.query.filter(User.mailbox == mailbox).first()
        if curr != None and curr.id != id:
            return {
                "errno": 1,
                "errmsg": '邮箱已存在!'
            }
        user.mailbox = mailbox
    if userpic != None:
        user.userpic = userpic
    datebase.session.commit()

    return {
        "errno": 0,
        "errmsg":''
    }

@db.route('/repassword', methods=['POST'])
def rePassWord():
    data = request.get_json(silent=True)
    id = data.get('id')
    password = data.get('password')
    rePassword = data.get('rePassword')
    user = User.query.filter(User.id == id).first()
    if(user.password != password):
        return {
            "errno": 1,
            "errmsg": "原密码输入错误"
        }
    user.password = rePassword
    datebase.session.commit()
    return {
        "errno": 0,
        "errmsg": ''
    }