from flask import Flask
from models import db

from handlers import auth, forum, game, page, user, api

app = Flask(__name__)
app.url_map.strict_slashes = False

db.create_all()

app.register_blueprint(auth.auth_handlers)
app.register_blueprint(forum.forum_handlers)
app.register_blueprint(game.game_handlers)
app.register_blueprint(page.page_handlers)
app.register_blueprint(user.user_handlers)

app.register_blueprint(api.api_handlers)

if __name__ == '__main__':
    app.run(debug=True)
