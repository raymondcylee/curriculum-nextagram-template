import re
from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
from flask_login import UserMixin


class User(BaseModel, UserMixin):
    name = pw.CharField(unique=False, null=False)
    username = pw.CharField(unique=True, null=False)
    email = pw.TextField(unique=True, null=False)
    password = pw.CharField(null=False)

    def validate(self):
        if not self.name or not self.username or not self.email or not self.password:
            self.errors.append("One of the fields is blank")

        duplicate_username = User.get_or_none(User.username == self.username)
        if duplicate_username and not(duplicate_username.id == self.id):
            self.errors.append('Username has been taken')
        
        
        duplicate_email = User.get_or_none(User.email == self.email)
        if duplicate_email and not(duplicate_email.id == self.id):
            self.errors.append('Email has been taken')
        
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.email):
            self.errors.append('Invalid Email')

        if not re.match(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}', self.password):
            self.errors.append('Invalid Password')
        else:
            self.password = generate_password_hash(self.password)

