from bottle import view, redirect, Bottle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Page, Relation
from sqlalchemy.engine.url import URL
import config
import numpy as np
import time

pages_app = Bottle()

engine = create_engine(URL(**config.DATABASE))
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

pages_limit = 20

@pages_app.route('/pages/<num>')
@pages_app.route('/pages')
@view('pages')
def pages_(num = 1):
    global pages_limit
    pages_to_display = pages_limit
    current_page = int(num)
    pages = session.query(Page).order_by(Page.rank.desc(), Page.url).offset(pages_to_display*(current_page-1)).limit(pages_to_display).all()
    total_pages = session.query(Page).count()
    return locals()

@pages_app.route('/pages/rank')
@view('pages')
def pagerank():

    start_time = time.time()

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

    print(time.time()-start_time, ": Copying")

    # init pagerank to 1/n
    pr = np.zeros(size)
    pr.fill(1 / size)

    stochastic_time = time.time()
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

    print(time.time() - stochastic_time, ": building stochastic matrix")

    # build E matrix
    e = np.zeros((size, size))
    e.fill(1 / size)
    #
    # set a parameter, Google uses 0.85, ČVUT uses 0.9
    a = 0.85


    g_time = time.time()
    # build Google matrix
    g = s * a + (1 - a) * e
    print(time.time() - g_time, ": building google matrix")

    iter_time = time.time()
    # iterate
    iter = 0
    while iter < 50:
        pr = np.dot(pr, g)
        iter += 1
    print(time.time() - iter_time, ": iterating")

    # print(pr)

    db_time = time.time()
    for i in session.query(Page).all():
        i.rank = pr[i.id - 1]
    session.commit()
    print(time.time() - db_time, ": writing back")

    end_time = time.time()
    print(end_time-start_time,": total time for processing",size,"x",size,"matrix")
    redirect("/pages")
    return locals()





