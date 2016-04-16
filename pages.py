from bottle import view, redirect, Bottle

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Page, Relation
from sqlalchemy.engine.url import URL

import config

pages_app = Bottle()

engine = create_engine(URL(**config.DATABASE))
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@pages_app.route('/pages')
@view('pages')
def pages():
    pages = session.query(Page).all()
    return locals()


@pages_app.route('/pages/remove')
@view('pages')
def page_remove_all():
    session.query(Relation).delete()
    session.query(Page).delete()
    session.commit()
    redirect("/pages")
    return locals()
