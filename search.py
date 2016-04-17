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


# Base = declarative_base()


class SearchFormProcessor(Form):
    request = StringField('Request:', [validators.length(min=3)], render_kw={"autofocus": "autofocus"})


@search_app.get('/search/<s_req>')
@search_app.post('/search/<s_req>')
@view('search_req')
def search(s_req):
    form = SearchFormProcessor(request.forms.decode())
    if request.method == 'POST' and form.validate():
        req = form.request.data
        redirect("/search/" + req)

    query = session.query(Page)
    pages = ss.search(query, s_req).order_by(desc(Page.rank)).limit(50)

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
