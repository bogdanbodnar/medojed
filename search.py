from bottle import view, redirect, Bottle, request
from wtforms import Form, StringField, IntegerField, BooleanField, validators

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_searchable import make_searchable
from sqlalchemy_searchable import search

from model import Page, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc
from sqlalchemy.engine.url import URL

import config
import sqlalchemy as sa
import sqlalchemy_searchable as ss

search_app = Bottle()

engine = create_engine(URL(**config.DATABASE))
Base.metadata.bind = engine
sa.orm.configure_mappers()
DBSession = sessionmaker(bind=engine)
session = DBSession()
import time


# Base = declarative_base()

pages_limit = 20

class SearchFormProcessor(Form):
    request = StringField('Request:', [validators.length(min=3)], render_kw={"autofocus": "autofocus"})

@search_app.get('/search/<s_req>/<num>')
@search_app.post('/search/<s_req>/<num')
@search_app.get('/search/<s_req>')
@search_app.post('/search/<s_req>')
@view('search_req')
def search(s_req, num = 1):
    print("Beep")
    form = SearchFormProcessor(request.forms.decode())
    if request.method == 'POST' and form.validate():
        req = form.request.data
        redirect("/search/" + req)

    start_time = time.time()

    query = session.query(Page)
    sssearch = ss.search(query, s_req).order_by(desc(Page.rank))

    global pages_limit
    pages_to_display = pages_limit
    pages = sssearch.limit(50)
    total_pages = sssearch.count()
    current_page = int(num)

    total_time = time.time() - start_time

    return locals()


@search_app.get('/search')
@search_app.post('/search')
@view('search')
def search():
    print("Boop")
    form = SearchFormProcessor(request.forms.decode())
    if request.method == 'POST' and form.validate():
        req = form.request.data
        redirect("/search/" + req)
    return locals()
