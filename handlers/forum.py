from flask import render_template, redirect, url_for, request, abort, Blueprint
from models import db, Topic
import uuid
from lib.auth import get_user
from redis import redis

forum_handlers = Blueprint("forum_handlers", __name__)


@forum_handlers.route('/forum', methods=['GET'])
def forum():
    topics = db.query(Topic).all()
    return render_template('forum/forum.html', topics=topics)


@forum_handlers.route('/forum/new-topic', methods=['GET', 'POST'])
def forum_new_topic():
    user = get_user()
    if not user:
        return redirect(url_for('auth_handlers.login'))

    csrf_token = str(uuid.uuid4())
    redis.set(name=csrf_token, value=user.name)

    if request.method == 'GET':
        return render_template('forum/forum-new-topic.html', csrf_token=csrf_token)
    else:
        csrf_token = request.form.get('csrf_token')
        redis_csrf_uname = redis.get(name=csrf_token).decode()
        if redis_csrf_uname and redis_csrf_uname == user.name:
            name = request.form.get('topic-name')
            body = request.form.get('topic-body')

            topic = Topic.create(title=name, text=body, author=user)
            return redirect(url_for('forum_handlers.forum'))
        else:
            abort(403)


@forum_handlers.route('/forum/<topic_id>', methods=['GET'])
def forum_topic_detail(topic_id):
    try:
        topic_id = int(topic_id)
    except ValueError:
        abort(404)

    topic = db.query(Topic).filter_by(id=int(topic_id)).first()
    return render_template('forum/forum-topic.html', topic=topic)

