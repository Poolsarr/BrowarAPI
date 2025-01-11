import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    ATLAS_LOGIN = os.getenv("atlas_login")
    JWT_SECRET_KEY = os.getenv("jwt_key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)