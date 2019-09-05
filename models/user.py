import re
import os
from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property


class User(BaseModel, UserMixin):
    name = pw.CharField(unique=False, null=False)
    username = pw.CharField(unique=True, null=False)
    email = pw.TextField(unique=True, null=False)
    password = pw.CharField(null=False)
    profile_picture = pw.CharField(null=True)

    @hybrid_property
    def all_idols(self):
        return [idol_rs.idol for idol_rs in self.idols]

    @hybrid_property
    def all_fans(self):
        array_of_fans = []
        for fans_rs in self.fans:
            fan = fans_rs.fan
            array_of_fans.append(fan)
        return array_of_fans

    @hybrid_property
    def profile_image_url(self):
        if self.profile_picture:
            return f'https://{os.environ.get("bucket_name")}.s3.amazonaws.com/' + self.profile_picture
        else:
            return "https://www.biiainsurance.com/wp-content/uploads/2015/05/no-image.jpg"

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