import os
from models.base_model import BaseModel
import peewee as pw
from flask_login import UserMixin
from models.user import User
from playhouse.hybrid import hybrid_property

class Image(BaseModel, UserMixin):
    image = pw.CharField()
    user = pw.ForeignKeyField(User, backref='images')

    @hybrid_property
    def upload_image_url(self):
        if self.image:
            return f'https://{os.environ.get("bucket_name")}.s3.amazonaws.com/' + self.image