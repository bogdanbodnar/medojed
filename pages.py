from bottle import view, redirect, Bottle, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, load_only
from model import Base, Page, Relation
from sqlalchemy.engine.url import URL
import config
import numpy as np
import time
from wtforms import Form, RadioField, IntegerField, FloatField, validators

pages_app = Bottle()

# engine = create_engine(URL(**config.DATABASE))
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

from model import session

pages_limit = 20

class CrawlerFormProcessor(Form):
    alpha = FloatField('α', [validators.NumberRange(min=0.001, max = 0.999, message="0 < α < 1")], default=0.85)
    iterations = IntegerField('Iterations', [validators.NumberRange(min=0, message="Should be positive")], default=50)
    choice_switcher = RadioField(
        'Choice?',
        [validators.DataRequired()],
        choices=[('choice1', 'Calculate G then apply it to PageRank vector'), ('choice2', 'Use matrix-free power method')], default='choice1'
    )

@pages_app.route('/pages/<num>')
@pages_app.route('/pages')
@view('pages')
def pages_(num = 1):
    form = CrawlerFormProcessor(request.forms.decode())
    global pages_limit
    pages_to_display = pages_limit
    current_page = int(num)
    pages = session.query(Page).order_by(Page.rank.desc(), Page.url).offset(pages_to_display*(current_page-1)).limit(pages_to_display).all()
    total_pages = session.query(Page).count()

    return locals()

@pages_app.post('/pages/rank')
@pages_app.route('/pages/rank')
@view('pages')
def pagerank():
    form = CrawlerFormProcessor(request.forms.decode())
    print(form.alpha.data, form.iterations.data, form.choice_switcher.data)

    alpha = form.alpha.data
    iterations = form.iterations.data
    power = False
    if form.choice_switcher.data == "choice2":
        power = True
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

    # ---------------------------------------------------------------------------------------------------------
    if power:
        pr = pagerank_power(size, graph, alpha, iterations)
    else:
        pr = pagerank_computation(size, graph, alpha, iterations)

    # ---------------------------------------------------------------------------------------------------------

    db_time = time.time()
    for i in session.query(Page).options(load_only("id", "text")).all():
        i.rank = pr[i.id - 1]
    session.commit()
    print(time.time() - db_time, ": writing back")
    end_time = time.time()
    print(end_time-start_time,": total time for processing",size,"x",size,"matrix")



    redirect("/pages")
    return locals()


def pagerank_computation (size, graph, alpha, iterations):
    # init pagerank to 1/n
    pr = np.full(size, 1 / size)

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



    g_time = time.time()
    # build Google matrix
    g = s * alpha + (1 - alpha) * e
    print(time.time() - g_time, ": building google matrix")

    iter_time = time.time()
    # iterate
    iter = 0
    while iter < iterations:
        diff = 0
        oldl = [x for (y, x) in sorted(zip(pr, range(0, size)))]
        pr = np.dot(pr, g)
        l = [x for (y, x) in sorted(zip(pr, range(0, size)))]
        for i in range(0,size):
            if oldl[i] != l[i]:
                diff += 1
        print("Iter", iter, "diff:", diff)
        iter += 1
    print(time.time() - iter_time, ": iterating")

    return pr

def pagerank_power (size, graph, alpha, iterations):
    # build a stochastic matrix
    H = np.zeros((size, size))
    sumOnRow = 0
    row = 0
    a = np.zeros(size)

    mark = time.time()
    for link in graph:
        H[link[0]][link[1]] = 1
        if link[0] == row:
            sumOnRow += 1
        elif link[0] > row:
            H[row] /= sumOnRow
            sumOnRow = 1
            row += 1
            while row != link[0]:
                a[row] = 1
                row += 1

    # final row edit
    H[row] /= sumOnRow
    row += 1
    while row < size:
        a[row] = 1
        row += 1

    print(time.time() - mark, "Building H")

    e = np.ones(size)
    pr = np.full(size, 1 / size)

    mark = time.time()
    iter = 0
    while iter < iterations:
        diff = 0
        oldl = [x for (y, x) in sorted(zip(pr, range(0, size)))]
        # mark = time.time()
        # pr = alpha * pr * H + (alpha * pr * a + 1 - alpha) * e / size
        pr = alpha * pr.dot(H) + (alpha * pr.dot(a) + 1 - alpha) * e / size
        l = [x for (y, x) in sorted(zip(pr, range(0, size)))]
        for i in range(0, size):
            if oldl[i] != l[i]:
                diff += 1
        print("Iter", iter, "diff:", diff)
        iter += 1
    print(time.time() - mark, "Iterating")

    return pr

