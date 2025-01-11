from pymongo import MongoClient
from flask import jsonify
import bcrypt
from flask_jwt_extended import create_access_token
import os
from config import Config

client = MongoClient(Config.ATLAS_LOGIN)
db = client.Browar1
users = db.users

def register_user(request):
    data = request.json
    login = data.get("login")
    password = data.get("password")

    if not login or not password:
        return jsonify({"error": "Podaj login i hasło"}), 400

    # Sprawdź, czy użytkownik już istnieje w bazie
    existing_user = users.find_one({"login": login})
    if existing_user:
        return jsonify({"error": "Użytkownik o podanym loginie już istnieje"}), 400

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Dodaj użytkownika do bazy
    users.insert_one({
        "login": login,
        "password_hash": hashed_password
    })

    return jsonify({"message": f"Użytkownik {login} został zarejestrowany"}), 201

def login_user(request):
    data = request.json
    login = data.get("login")
    password = data.get("password")

    if not login or not password:
        return jsonify({"error": "Podaj login i hasło"}), 400

    user = users.find_one({"login": login})
    if not user:
        return jsonify({"error": "Nieprawidłowy login lub hasło"}), 401

    if bcrypt.checkpw(password.encode("utf-8"), user["password_hash"]):
        access_token = create_access_token(identity=login)
        return jsonify({"message": "Zalogowano pomyślnie!", "access_token": access_token}), 200
    else:
        return jsonify({"error": "Nieprawidłowy login lub hasło"}), 401