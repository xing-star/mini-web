from .. import app
from .views import *
"""
Issue:经测试，首次新号码发送验证码，在注册和修改密码时都会“卡”一段时间
经排查，在为到达post方法之前属于卡顿时间，说明不是代码的问题，具体问题待
处理。
Issue:经测试，添加数据的时候同一请求添加的datetime.now()的时间都是一致不会变化的。
"""


def usersrouter():
    app.add_url_rule('/', view_func=Index.as_view('/'), methods=['GET'])

    # 用户注册路由
    app.add_url_rule('/users/register', view_func=Register.as_view('/users/register'),
                     methods=['POST'])
    # 用户登录路由
    app.add_url_rule('/users/login', view_func=Login.as_view('/users/login'),
                     methods=['POST'])
    # 获取token
    app.add_url_rule('/users/token', view_func=Token.as_view('/users/token'),
                     methods=['GET'])
    # 注销登录（此处采用直接设置token过期来注销登录）Issue：此处设置过期时间无效
    app.add_url_rule('/users/logout', view_func=Logout.as_view('/users/logout'),
                     methods=['GET'])
    # 用户未登录修改密码的路由（忘记密码）
    app.add_url_rule('/users/changepassword', view_func=ChangePassword.as_view('/users/changepassword'),
                     methods=['POST'])
    # 用户登录修改密码
    app.add_url_rule('/users/loginchangepassword', view_func=LoginChangePassword
                     .as_view('/users/loginchangepassword'), methods=['POST'])
