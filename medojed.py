from bottle import Bottle, static_file, view

from crawler import crawler_app
from pages import pages_app
from search import search_app

root_app = Bottle()


@root_app.route('/')
@view('index')
def index():
    return locals()


@root_app.route('/css/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static/css')


@root_app.route('/js/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static/js')


@root_app.route('/img/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static/img')


@root_app.route('/fonts/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static/fonts')


if __name__ == '__main__':
    root_app.merge(crawler_app)
    root_app.merge(pages_app)
    root_app.merge(search_app)
    root_app.run(server='cherrypy', host='localhost', port=8080, debug=True, reloader=True)
