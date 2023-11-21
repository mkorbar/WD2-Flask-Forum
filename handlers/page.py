from flask import render_template, Blueprint, make_response

page_handlers = Blueprint("page_handlers", __name__)


@page_handlers.route('/about', methods=['GET'])
def about():
    page = make_response(render_template('page/about.html'))
    page.set_cookie('token', 'tokencookieValue')

    return page
