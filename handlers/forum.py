from flask import render_template, redirect, url_for, request, abort, Blueprint
from models import db, Topic, Comment
from lib.auth import get_user
from redis import create_token, token_valid

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

    csrf_token = create_token(user.name)

    if request.method == 'GET':
        return render_template('forum/forum-new-topic.html', csrf_token=csrf_token)
    else:
        csrf_token = request.form.get('csrf_token')

        if token_valid(user.name, csrf_token):
            name = request.form.get('topic-name')
            body = request.form.get('topic-body')

            topic = Topic.create(title=name, text=body, author=user)
            return redirect(url_for('forum_handlers.forum'))
        else:
            abort(403)


@forum_handlers.route('/forum/<topic_id>', methods=['GET', 'POST'])
def forum_topic_detail(topic_id):
    user = get_user()
    try:
        topic_id = int(topic_id)
    except ValueError:
        abort(404)

    topic = db.query(Topic).filter_by(id=int(topic_id)).first()
    if request.method == 'GET':
        if not topic:
            abort(404)
        comments = db.query(Comment).filter_by(topic_id=topic_id).all()
        csrf_token = create_token(user.name)

        return render_template('forum/forum-topic.html', topic=topic, comments=comments, csrf_token=csrf_token)
    else:
        csrf_token = request.form.get('csrf_token')

        if token_valid(user.name, csrf_token):
            body = request.form.get('comment-body')

            Comment.create(text=body, author=user, topic=topic)
            return redirect(url_for('forum_handlers.forum_topic_detail', topic_id=topic_id))
        else:
            abort(403)

