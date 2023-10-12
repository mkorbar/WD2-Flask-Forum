from flask import request, render_template, url_for, make_response, redirect, Blueprint
import random
from lib.auth import get_user
from models import db
from settings import MAX_SECRET

game_handlers = Blueprint("game_handlers", __name__)


@game_handlers.route('/', methods=['GET'])
def index():
    user = get_user()
    return render_template('game/index.html', user=user, max_secret=MAX_SECRET)


@game_handlers.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))
    user = get_user()
    if not user:
        return redirect(url_for('auth_handlers.login'))

    if guess == user.secret_number:
        message = "Pravilno! Skrito število je {0}".format(str(user.secret_number))
        response = make_response(render_template("game/result.html", finished=True, message=message))
        user.secret_number = random.randint(1, MAX_SECRET)
        db.add(user)
        db.commit()
        return response
    elif guess > user.secret_number:
        message = "Ta poizkus ni pravilen. Poizkusi z manjšo številko."
        return render_template("game/result.html", finished=False, message=message)
    elif guess < user.secret_number:
        message = "Ta poizkus ni pravilen. Poizkusi z večjo številko."
        return render_template("game/result.html", finished=False,  message=message)
