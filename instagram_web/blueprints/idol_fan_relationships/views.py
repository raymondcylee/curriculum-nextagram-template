import re
from flask import Blueprint, render_template, url_for, request, redirect, flash, abort, jsonify
from models.user import User
from models.image import Image
from models.idol_fan_relationships import IdolFanRelationships
from flask_login import logout_user, login_required, current_user

idol_fan_relationships_blueprint = Blueprint('idol_fan_relationships',
                            __name__,
                            template_folder='templates')


@idol_fan_relationships_blueprint.route('/<id>/follow', methods=["POST"])
def create(id):
    user = User.get_or_none(User.id == id)
    follow = IdolFanRelationships(idol_id=user.id, fan_id=current_user.id, user=user)
    follow.save()
    response = {
        "status": "success",
    }
    return jsonify(response)

@idol_fan_relationships_blueprint.route('/<id>/unfollow', methods=["POST"])
def destroy(id):
    user = User.get_by_id(id)
    IdolFanRelationships.delete().where(IdolFanRelationships.idol_id == user.id, IdolFanRelationships.fan_id == current_user.id).execute()
    response = {
        "status": "success"
    }
    return jsonify(response)