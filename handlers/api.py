import json
from flask import Blueprint, jsonify, request


api_handlers = Blueprint("api_handlers", __name__, url_prefix='/api')


@api_handlers.route("/user", methods=["GET"])
def user_get():
    with open('users.json') as f:
        users = json.loads(f.read())
    # return json.dumps(users)
    return jsonify(users)


@api_handlers.route("/user", methods=["POST"])
def user_post():
    data = json.loads(request.data)
    print(data['field_name_1'])

    return jsonify({'status': 'ok'})
