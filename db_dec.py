import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Page(Base):
    __tablename__ = 'page'
    id = Column(Integer, primary_key=True)
    url = Column(String(250))
    text = Column(String(250))
    rank = Column(Integer)

class Relation(Base):
    __tablename__ = 'relation'
    id = Column(Integer, primary_key=True)
    page_id = Column(Integer, ForeignKey('page.id'))
    destination_id = Column(Integer)
    page = relationship(Page)

engine = create_engine('sqlite:///medojed.db')

Base.metadata.create_all(engine)