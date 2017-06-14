from pyramid.security import Allow, Everyone

from sqlalchemy import Column, Integer, VARCHAR

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session, sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension(), expire_on_commit=False))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    First_Name = Column(VARCHAR(255))
    Last_Name = Column(VARCHAR(255))
    Age = Column(Integer)
    Address = Column(VARCHAR(255))


class Root(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:editors', 'edit')]

    def __init__(self, request):
        pass
