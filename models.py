from datetime import datetime



from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from todolist import db

class Todolist(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    status = db.Column(db.Integer)
    create_time = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',back_populates='todolists')


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24))
    password_hash = db.Column(db.String(128))
    todolists = db.relationship('Todolist',back_populates='user',lazy='dynamic')

    @property
    def password(self):
        """ 密码属性不可被访问
        """
        raise AttributeError('密码不可访问')

    @password.setter
    def password(self,password):
        """ 密码属性可写不可读
                :param password: 用户密码
                """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """ 密码验证
        :param password: 用户密码
        :return: 验证成功返回 True，反之返回 False
        """
        return check_password_hash(self.password_hash,password)






