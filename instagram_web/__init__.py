from app import app
import os
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from instagram_web.blueprints.idol_fan_relationships.views import idol_fan_relationships_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from models.image import Image
from models.user import User
from models.donations import Donation
from models.idol_fan_relationships import IdolFanRelationships
from instagram_web.helpers.google_oauth import oauth
import config

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(idol_fan_relationships_blueprint, url_prefix="/idol_fan_relationships")

oauth.init_app(app)

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
def home():
    users = User.select().prefetch(Image)
    return render_template('home.html', users=users)
