from flask import request, render_template, redirect, url_for, abort, Blueprint
from models import db, User

user_handlers = Blueprint("user_handlers", __name__)


@user_handlers.route("/profile", methods=["GET"])
def profile():
    token = request.cookies.get('token')
    user = db.query(User).filter_by(session_token=token).first()

    if user:
        return render_template("user/profile.html", user_data=user)
    else:
        return redirect(url_for('auth_handlers.login'))


@user_handlers.route("/profile/edit", methods=["GET", "POST"])
def profile_edit():
    token = request.cookies.get('token')
    user = db.query(User).filter_by(session_token=token).first()

    if not user:
        return redirect(url_for('auth_handlers.login'))
    else:
        if request.method == "GET":
            return render_template("user/profile_edit.html", user_data=user)
        else:
            user.email = request.form.get('email')
            db.add(user)
            db.commit()

            return redirect(url_for('user_handlers.profile'))


@user_handlers.route("/profile/delete", methods=["GET", "POST"])
def profile_delete():
    token = request.cookies.get('token')
    user = db.query(User).filter_by(session_token=token).first()

    if not user:
        return redirect(url_for('auth_handlers.login'))
    else:
        if request.method == "GET":
            return render_template("user/profile_delete.html")
        else:
            db.delete(user)
            db.commit()

            return render_template("user/deleted.html")


@user_handlers.route("/users")
def all_users():
    users_list = db.query(User).all()

    return render_template("user/all_users.html", users=users_list)


# beremo vrednost parametra user_id iz URL naslova
@user_handlers.route("/user/<user_id>")
def user_detail(user_id):
    user = db.query(User).get(int(user_id))
    if not user:
        abort(404)

    return render_template("user/profile.html", user_data=user)

