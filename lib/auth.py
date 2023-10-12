from flask import request
from models import db, User


def get_user(user_token=None):
    if not user_token:
        user_token = request.cookies.get('token')
    return db.query(User).filter_by(session_token=user_token).first()
