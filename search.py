from bottle import view, redirect, Bottle, request
from wtforms import Form, StringField, IntegerField, BooleanField, validators

from model import Page, Base,session
from sqlalchemy import create_engine, desc

import sqlalchemy_searchable as ss
import time

search_app = Bottle()
pages_limit = 10


class SearchFormProcessor(Form):
    request = StringField('Request:', [validators.length(min=3)], render_kw={"autofocus": "autofocus"})

@search_app.post('/search/<s_req>')
@search_app.get('/search/<s_req>')
@search_app.post('/search/<s_req>/<num>')
@search_app.get('/search/<s_req>/<num>')
@view('search_req')
def search(s_req, num = 1):
    print("Processing search request", s_req)
    form = SearchFormProcessor(request.forms.decode())
    if request.method == 'POST' and form.validate():
        req = form.request.data
        redirect("/search/" + req)

    start_time = time.time()

    query = session.query(Page)
    sssearch = ss.search(query, s_req).order_by(desc(Page.rank))

    global pages_limit
    pages_to_display = pages_limit
    current_page = int(num)
    pages = sssearch.offset(pages_to_display*(current_page-1)).limit(pages_limit)
    total_pages = sssearch.count()


    total_time = time.time() - start_time

    return locals()


@search_app.get('/search')
@search_app.post('/search')
@view('search')
def search():
    form = SearchFormProcessor(request.forms.decode())
    if request.method == 'POST' and form.validate():
        req = form.request.data
        redirect("/search/" + req)
    return locals()
