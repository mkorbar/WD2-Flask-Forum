from flask import request, render_template, make_response, redirect, url_for, Blueprint
import hashlib
import uuid
from models import db, User
import random
from settings import MAX_SECRET

auth_handlers = Blueprint("auth_handlers", __name__)


@auth_handlers.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        response = render_template('auth/login.html')
    else:
        email = request.form.get('user-email')
        password = hashlib.sha256(request.form.get('user-pass').encode()).hexdigest()

        user = db.query(User).filter_by(email=email, passwd=password).first()
        if not user:
            alert = {
                'message': 'Napačno geslo ali email naslov. Poskusi še enkrat ali ustvari '
                           '<a href="/user/sign-up/">nov račun</a>',
                'type': 'warning'
            }
            return render_template('auth/login.html', alert=alert)

        token = str(uuid.uuid4())
        user.session_token = token
        db.add(user)
        db.commit()

        response = make_response(redirect(url_for('game_handlers.index')))
        response.set_cookie('token', token, httponly=True, samesite='strict')

    return response


@auth_handlers.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        response = render_template('auth/sign-up.html')
    else:
        name = request.form.get('user-name')
        email = request.form.get('user-email')
        password = str(request.form.get('user-pass'))
        password = hashlib.sha256(password.encode()).hexdigest()

        user = db.query(User).filter_by(email=email).first()
        if user:
            alert = {'message': 'Uporabnik s tem elektronskim naslovom že obstaja.', 'type': 'warning'}
            return render_template('sign-up.html', alert=alert)

        secret = random.randint(1, MAX_SECRET)
        token = str(uuid.uuid4())
        user = User(name=name, email=email, secret_number=secret, passwd=password, session_token=token)
        db.add(user)
        db.commit()

        response = make_response(redirect(url_for('game_handlers.index')))
        response.set_cookie('token', token, httponly=True, samesite='strict')

    return response
