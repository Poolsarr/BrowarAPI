from flask import Blueprint, request, jsonify
from users.user_utils import get_all_users
from flask_jwt_extended import jwt_required

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route("", methods=["GET"])
@jwt_required()
def users_route():
    return get_all_users()