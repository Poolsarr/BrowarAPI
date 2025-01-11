from flask import Blueprint, request, jsonify
from auth.auth_utils import register_user, login_user
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth', __name__, url_prefix='/')

@auth_bp.route("/register", methods=["POST"])
def register():
    return register_user(request)

@auth_bp.route("/login", methods=["POST"])
def login():
    return login_user(request)
