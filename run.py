from bottle import route, view, run, request, get, post, debug, template, static_file, error, redirect
from wtforms import Form, StringField, IntegerField, BooleanField, validators

import urllib.request
from bs4 import BeautifulSoup

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_dec import Base, Page, Relation

#DB connection
engine = create_engine('sqlite:///medojed.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')


@route('/hello/<name>')
def hello(name="asdsd"):
    return template('<b>Hello {{name}}</b>!', name=name)


class CrawlerFormProcessor(Form):
    url = StringField('URL', [validators.URL(require_tld=False, message="Must be valid URL")],
                      render_kw={"placeholder": "https://example.com"})
    depth = IntegerField('Depth', [validators.NumberRange(min=1, message="Must be > 0")], default=1)
    max_pages = IntegerField('Maximum pages', [validators.NumberRange(min=1, message="Must be > 0")], default=1000)
    uel = BooleanField('Uninclude external links')


class SearchFormProcessor(Form):
    request = StringField('Request:', [validators.length(min=3)], render_kw={"placeholder": "Request example"})


def getOutlinks(website, removeExternalLinks):
    results = []

    # add 'http' to the link if needed
    if website.find("http://") != 0 and website.find("https://") != 0:
        website = "http://" + website

    # remove / in the end
    while website[-1:] == '/':
        website = website[:-1]

    print('website', website)
    # domain base
    base = website[7:]
    slpos = base.find('/')
    if slpos != -1:
        base = base[:slpos]
    if base.find("www.") == 0:
        base = base[4:]
    print("BASE = ", base)

    # get header and content
    try:
        with urllib.request.urlopen(website) as url:
            info = url.info()
            page = url.read()
    except IOError:
        print("Couldn't open url", website)
        return

    # discard non-html
    if info['Content-Type'].find("html") == -1:
        print("Error : It's not an html page!")
        return

    # prepare soup

    soup = BeautifulSoup(page, "html.parser")

    for link in soup.find_all('a'):
        temp = link.get('href')

        # skip empty
        if temp is None:
            continue

        if len(temp) == 0:
            continue

        # fix relative links
        if temp[0] == '/':
            temp = website + temp
        elif temp[0] != 'h':
            temp = website + '/' + temp

        # throw away anchors
        if temp[0] == '#':
            continue

        # cut anchors from urls at the end
        if temp.rfind('#') != -1:
            temp = temp[:temp.rfind('#')]

        # throw away 'http' part
        httppos = temp.rfind("://")
        if httppos != -1:
            temp = temp[httppos + 3:]

        # throw away the 'www' part
        if temp.find("www.") == 0:
            temp = temp[4:]

        # throw away slash at the end
        if temp[-1:] == '/':
            temp = temp[:-1]

        # throwaway javascript: or mailto:
        if temp.find(":") != -1:
            continue

        if removeExternalLinks == True:
            ws = temp.find(base)
            sl = temp.find("/")
            if ws == -1 or sl < ws:
                continue

        try:
            with urllib.request.urlopen("http://" + temp) as url:
                info = url.info()
                page = url.read()
        except IOError:
            print("Couldn't open url", website)

        soup = BeautifulSoup(page, "html.parser")

        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        results.append([temp, text.encode('utf-8')])

    return results


@route('/')
@view('index')
def index():
    return locals()


@get('/crawler')
@post('/crawler')
@view('crawler')
def crawler():
    form = CrawlerFormProcessor(request.forms.decode())
    if request.method == 'POST' and form.validate():
        results = getOutlinks(form.url.data, form.uel.data)
        for page in results:
            url = page[0]
            text = page[1]
            new_page = Page(url=url, text=text, rank=0)
            session.add(new_page)
        session.commit()
        redirect("/pages")

    return locals()


@get('/search')
@post('/search')
@view('search')
def search():
    form = SearchFormProcessor(request.forms.decode())
    if request.method == 'POST' and form.validate():
        req = form.request.data
        redirect("/search/" + req)
    return locals()


@route('/pages')
@view('pages')
def pages():
    pages = session.query(Page).all()
    return locals()


@route('/pages/remove')
@view('pages')
def page_remove_all():
    session.query(Page).delete()
    session.commit()
    redirect("/pages")
    return locals()


run(server='cherrypy', host='localhost', port=8080, debug=True, reloader=True)
