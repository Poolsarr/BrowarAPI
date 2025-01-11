from pymongo import MongoClient
from flask import jsonify
from config import Config

client = MongoClient(Config.ATLAS_LOGIN)
db = client.Browar1
users = db.users

def get_all_users():
    try:
        all_users = users.find() 
        
        # Zamiana wyników na listę i konwersja do JSON
        users_list = []
        for user in all_users:
            user_data = {
                "_id": str(user["_id"]), 
                "login": user.get("login")
            }
            users_list.append(user_data)
        
        return jsonify(users_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500