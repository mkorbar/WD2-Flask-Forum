import random
from flask import Flask, render_template, request, make_response, redirect, url_for, abort
from models import User, Topic, db
import uuid
import hashlib
import os
import smartninja_redis

redis = smartninja_redis.from_url(os.environ.get('REDIS_URL'))

app = Flask(__name__)
app.url_map.strict_slashes = False
db.create_all()

MAX_SECRET = 30


def get_user(user_token=None):
    if not user_token:
        user_token = request.cookies.get('token')
    return db.query(User).filter_by(session_token=user_token).first()


@app.route('/', methods=['GET'])
def index():
    user = get_user()
    return render_template('index.html', user=user, max_secret=MAX_SECRET)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/forum', methods=['GET'])
def forum():
    topics = db.query(Topic).all()
    return render_template('forum.html', topics=topics)


@app.route('/forum/new-topic', methods=['GET', 'POST'])
def forum_new_topic():
    user = get_user()
    if not user:
        return redirect(url_for('login'))

    csrf_token = str(uuid.uuid4())
    redis.set(name=csrf_token, value=user.name)

    if request.method == 'GET':
        return render_template('forum-new-topic.html', csrf_token=csrf_token)
    else:
        csrf_token = request.form.get('csrf_token')
        redis_csrf_uname = redis.get(name=csrf_token).decode()
        print(redis_csrf_uname)
        if redis_csrf_uname and redis_csrf_uname == user.name:
            name = request.form.get('topic-name')
            body = request.form.get('topic-body')

            topic = Topic.create(title=name, text=body, author=user)
            return redirect(url_for('forum'))
        else:
            abort(403)


@app.route('/forum/<topic_id>', methods=['GET'])
def forum_topic_detail(topic_id):
    try:
        topic_id = int(topic_id)
    except ValueError:
        abort(404)

    topic = db.query(Topic).filter_by(id=int(topic_id)).first()
    return render_template('forum-topic.html', topic=topic)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        response = render_template('login.html')
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
            return render_template('login.html', alert=alert)

        token = str(uuid.uuid4())
        user.session_token = token
        db.add(user)
        db.commit()

        response = make_response(redirect(url_for('index')))
        response.set_cookie('token', token, httponly=True, samesite='strict')

    return response


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        response = render_template('sign-up.html')
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

        response = make_response(redirect(url_for('index')))
        response.set_cookie('token', token, httponly=True, samesite='strict')

    return response


@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))
    user = get_user()
    if not user:
        return redirect(url_for('login'))

    if guess == user.secret_number:
        message = "Pravilno! Skrito število je {0}".format(str(user.secret_number))
        response = make_response(render_template("result.html", finished=True, message=message))
        user.secret_number = random.randint(1, MAX_SECRET)
        db.add(user)
        db.commit()
        return response
    elif guess > user.secret_number:
        message = "Ta poizkus ni pravilen. Poizkusi z manjšo številko."
        return render_template("result.html", finished=False, message=message)
    elif guess < user.secret_number:
        message = "Ta poizkus ni pravilen. Poizkusi z večjo številko."
        return render_template("result.html", finished=False,  message=message)


@app.route("/profile", methods=["GET"])
def profile():
    token = request.cookies.get('token')
    user = db.query(User).filter_by(session_token=token).first()

    if user:
        return render_template("profile.html", user_data=user)
    else:
        return redirect(url_for('login'))


@app.route("/profile/edit", methods=["GET", "POST"])
def profile_edit():
    token = request.cookies.get('token')
    user = db.query(User).filter_by(session_token=token).first()

    if not user:
        return redirect(url_for('login'))
    else:
        if request.method == "GET":
            return render_template("profile_edit.html", user_data=user)
        else:
            user.email = request.form.get('email')
            db.add(user)
            db.commit()

            return redirect(url_for('profile'))


# todo: change method to POST
@app.route("/profile/delete", methods=["GET", "POST"])
def profile_delete():
    token = request.cookies.get('token')
    user = db.query(User).filter_by(session_token=token).first()

    if not user:
        return redirect(url_for('login'))
    else:
        if request.method == "GET":
            return render_template("profile_delete.html")
        else:
            db.delete(user)
            db.commit()

            return render_template("deleted.html")


@app.route("/users")
def all_users():
    users_list = db.query(User).all()

    return render_template("all_users.html", users=users_list)


# beremo vrednost parametra user_id iz URL naslova
@app.route("/user/<user_id>")
def user_detail(user_id):
    user = db.query(User).get(int(user_id))
    if not user:
        abort(404)

    return render_template("profile.html", user_data=user)


if __name__ == '__main__':
    app.run()
