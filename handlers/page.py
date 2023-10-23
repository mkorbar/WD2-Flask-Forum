from flask import render_template, Blueprint

page_handlers = Blueprint("page_handlers", __name__)


@page_handlers.route('/about', methods=['GET'])
def about():
    from tasks import get_random_num
    get_random_num()
    return render_template('page/about.html')
