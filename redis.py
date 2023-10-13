import os
import smartninja_redis
import uuid


redis = smartninja_redis.from_url(os.environ.get('REDIS_URL'))


def create_token(username):
    csrf_token = str(uuid.uuid4())
    redis.set(name=csrf_token, value=username)
    return csrf_token


def token_valid(username, csrf_token):
    if csrf_token:
        redis_csrf_uname = redis.get(name=csrf_token)
        if not redis_csrf_uname:
            return False
        return redis_csrf_uname.decode() == username
    else:
        return False
