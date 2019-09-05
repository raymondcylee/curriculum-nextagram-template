import re
import os
from models.base_model import BaseModel
import peewee as pw
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property
from models.image import Image


class Donation(BaseModel, UserMixin):
    amount = pw.DecimalField(null=False, decimal_places=0)
    image = pw.ForeignKeyField(Image, backref='donations')
    user = pw.CharField(null=False)
