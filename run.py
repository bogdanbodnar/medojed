from bottle import route, view, run,  request, get, post, debug, template , static_file, error , redirect
from wtforms import Form, StringField, IntegerField, BooleanField, validators

import urllib.request
from bs4 import BeautifulSoup

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_dec import Base, Page, Relation


@route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')


class CrawlerFormProcessor(Form):
    url = StringField('URL', [validators.URL(require_tld=False, message="Must be valid URL")], render_kw={"placeholder": "https://example.com"})
    depth = IntegerField('Depth', [validators.NumberRange(min=1, message="Must be > 0")] , default=1)
    max_pages = IntegerField('Maximum pages', [validators.NumberRange(min=1, message="Must be > 0")], default=1000)
    uel = BooleanField('Uninclude external links')


def getOutlinks (website, removeExternalLinks):

    results = set()

    #add 'http' to the link if needed
    if website.find("http://")!= 0 and website.find("https://") != 0 :
        website = "http://" + website

    #remove / in the end
    while website[-1:] == '/':
        website = website[:-1]

    print('website', website)
    #domain base
    base = website[7:]
    slpos = base.find('/')
    if slpos != -1:
        base = base[:slpos]
    if base.find("www.") == 0:
        base = base[4:]
    print("BASE = ", base)

    #get header and content
    try:
        with urllib.request.urlopen(website) as url:
            info = url.info()
            page = url.read()
    except IOError:
        print("Couldn't open url",website)
        return

    #discard non-html
    if info['Content-Type'].find("html") == -1:
        print("Error : It's not an html page!")
        return
    #prepare soup
    soup = BeautifulSoup(page, "html.parser")

    for link in soup.find_all('a'):
        temp = link.get('href')

        #skip empty
        if temp is None:
            continue

        if len(temp) == 0:
            continue

        #print ("got", temp)
        #fix relative links
        if temp[0] == '/':
            temp = website + temp
        elif temp[0]!='h':
            temp = website + '/' + temp

        #throw away anchors
        if temp[0] == '#':
            continue

        #cut anchors from urls at the end
        if temp.rfind('#') != -1:
            temp = temp[:temp.rfind('#')]

        #throw away 'http' part
        httppos = temp.rfind("://")
        if httppos != -1:
            temp = temp[httppos+3 :]

        #throw away the 'www' part
        if temp.find("www.") == 0:
            temp = temp[4:]

        #throw away slash at the end
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

        results.add(temp)

    return results


@route('/')
@view('index')
def index():
    return locals()


@get('/crawler', name='crawler')
@post('/crawler')
@view('crawler')
def crawler():
    form = CrawlerFormProcessor(request.forms.decode())
    if request.method == 'POST' and form.validate():
        results = getOutlinks(form.url.data, form.uel.data)

        engine = create_engine('sqlite:///medojed.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        for link in results:
            new_page = Page(url=link)
            session.add(new_page)
        session.commit()
        redirect("/pages")

    return locals()

@route('/pages')
@view('pages')
def pages():

    engine = create_engine('sqlite:///medojed.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    pages = session.query(Page).all()
    return locals()

@route('/pages/remove')
@view('pages')
def page_remove_all():
    engine = create_engine('sqlite:///medojed.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    session.query(Page).delete();

    session.commit()

    pages = session.query(Page).all()

    return locals()

run(host='localhost', port=8080, debug=True,reloader=True)