from flask import request, Response
from flask.views import MethodView
from .models import *
from flask import jsonify, g
from .. import app
import os, time


class Index(MethodView):

    def __init__(self):
        pass

    @auth.login_required
    def get(self):
        return 'hello world!!!'


class Register(MethodView):

    def __init__(self):
        self.user_id = request.form.get('user_id')
        self.pwd = request.form.get('pwd')

    def post(self):
        try:
            user = User(password=self.pwd, user_id=self.user_id)
            db.session.add(user)
            db.session.commit()
            return jsonify({'code': '200', 'message': 'success'})
        except Exception as e:
            raise e


class Login(MethodView):

    def __init__(self):
        self.user_id = request.form.get('user_id')
        self.pwd = request.form.get('pwd')

    def post(self):
        result = User.query.filter_by(user_id=self.user_id).first()
        if result is not None and result.verify_password(self.pwd):
            return jsonify({"code": "200", "message": "success"})
        return jsonify({"code": "500", "message": "fail"})


# 获取token
class Token(MethodView):

    def __init__(self):
        pass

    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token(600)
        return jsonify({'token': token.decode('ascii'), 'duration': 600})


class Logout(MethodView):

    def __init__(self):
        pass

    @auth.login_required
    def get(self):
        g.user.generate_auth_token(1)
        return jsonify({"code": "200", "message": "success"})


class ChangePassword(MethodView):

    def __init__(self):
        self.user_id = request.form.get('user_id')
        self.pwd = request.form.get('pwd')

    def post(self):
        str_result = User.query.filter_by(user_id=self.user_id).first()
        str_result.pwd = self.pwd
        db.session.add(str_result)
        db.session.commit()
        return jsonify({"code": "200", "message": "success"})


class LoginChangePassword(MethodView):

    def __init__(self):
        self.user_id = request.form.get('user_id')
        self.old_pwd = request.form.get('old_pwd')
        self.new_pwd = request.form.get('new_pwd')

    def post(self):
        result = User.query.filter_by(user_id=self.user_id).first()
        if result is not None and result.verify_pwd(self.old_pwd):
            result.pwd = self.new_pwd
            db.session.add(result)
            db.session.commit()
            return jsonify({"code": "200", "message": "success"})
