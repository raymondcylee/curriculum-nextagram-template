from flask_wtf.csrf import CSRFProtect
import os
import config
from flask import Flask
from models.base_model import db
from flask_login import LoginManager
import boto3, botocore


web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)

S3_BUCKET = os.environ.get("bucket_name")
S3_KEY = os.environ.get("access_key_ID")
S3_SECRET = os.environ.get("secret_access_key")


if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)