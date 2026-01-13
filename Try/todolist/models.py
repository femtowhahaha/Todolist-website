
from todolist import db
from datetime import datetime
from todolist import bcrypt
from todolist import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    

class User(db.Model, UserMixin):

    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    username = db.Column(db.String(length=30), nullable=False, unique=True )
    password_hash = db.Column(db.String(), nullable=False)

    user_todos = db.relationship('List', backref='owner', lazy=True)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_hash(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class List(db.Model):
    

    list_id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    todo = db.Column(db.String(length=400), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    num = db.Column(db.Integer(), nullable=False)

    __table_args__ = (db.UniqueConstraint('user_id', 'num', name='unique_num_per_user'),)

    def __repr__(self):
        return f"To do {self.num}"


