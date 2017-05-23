# coding:utf-8

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
url = 'mysql+pymysql://root:root@52.163.48.238:10101/m1905_db?charset=utf8'
engine = create_engine(url, echo=False)


class DB_Util(object):
    @staticmethod
    def get_session(url=None):
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    @staticmethod
    def init_db():
        Base.metadata.create_all(engine)


class m1905_movies(Base):
    __tablename__ = 'movie'
    info_id = Column(String(100),primary_key=True, nullable=False)
    name = Column(String(100), nullable=True)
    director = Column(String(100), nullable=True)
    actor = Column(String(100), nullable=True)
    type = Column(String(100), nullable=True)
    country = Column(String(100),nullable=True)
    date = Column(String(100),nullable=True)
    gernic = Column(String(100), nullable=True)
    score = Column(String(100), nullable=True)
    time = Column(String(100), nullable=True)




