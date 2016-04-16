from bottle import view, redirect, Bottle

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Page, Relation
from sqlalchemy.engine.url import URL

import config

import numpy as np

pages_app = Bottle()

engine = create_engine(URL(**config.DATABASE))
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@pages_app.route('/pages')
@view('pages')
def pages():
    pages = session.query(Page).order_by(Page.rank.desc(), Page.url).all()
    return locals()


@pages_app.route('/pages/rank')
@view('pages')
def pagerank():
    graph = []
    size = 0
    for i in session.query(Relation).order_by(Relation.page_id).all():
        ifrom = i.page_id
        ito = i.destination_id
        # print(ifrom, ito)
        graph.append((ifrom-1, ito-1))
        if ifrom > size:
            size = ifrom
        if ito > size:
            size = ito

    #print("Size =", size)

    # init pagerank to 1/n
    pr = np.zeros(size)
    pr.fill(1 / size)

    # build a stochastic matrix
    s = np.zeros((size, size))
    sumOnRow = 0
    row = 0

    for link in graph:
        s[link[0]][link[1]] = 1
        if link[0] == row:
            sumOnRow += 1
        elif link[0] > row:
            s[row] /= sumOnRow
            sumOnRow = 1
            row += 1
            while row != link[0]:
                s[row] = 1 / size
                row += 1

    # final row edit
    s[row] /= sumOnRow
    row += 1
    while row < size:
        s[row] = 1 / size
        row += 1

    # build E matrix
    e = np.zeros((size, size))
    e.fill(1 / size)
    #
    # set a parameter, Google uses 0.85, ČVUT uses 0.9
    a = 0.85

    # build Google matrix
    g = s * a + (1 - a) * e

    # print(g)
    # iterate
    iter = 0
    while iter < 50:
        pr = np.dot(pr, g)
        iter += 1

    # print(pr)

    for i in session.query(Page).all():
        i.rank = pr[i.id - 1]
    session.commit()


    redirect("/pages")
    return locals()


