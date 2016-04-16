import os

from sqlalchemy import Column, ForeignKey, Integer, UnicodeText, String, Unicode, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType

import config

Base = declarative_base()
make_searchable()


class Page(Base):
    __tablename__ = 'page'
    id = Column(Integer, primary_key=True)
    url = Column(Unicode(255), unique=True)
    text = Column(UnicodeText())
    rank = Column(Float)
    search_vector = Column(TSVectorType('text', 'url'))


class Relation(Base):
    __tablename__ = 'relation'
    id = Column(Integer, primary_key=True)
    page_id = Column(Integer, ForeignKey('page.id'))
    destination_id = Column(Integer)
    page = relationship(Page)

engine = create_engine(URL(**config.DATABASE))
Base.metadata.create_all(engine)
