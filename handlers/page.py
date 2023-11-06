from flask import render_template, Blueprint

page_handlers = Blueprint("page_handlers", __name__)


@page_handlers.route('/about', methods=['GET'])
def about():
    return render_template('page/about.html')
