from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import config

engine = create_engine(config.SQL_DB_URI)
Base = declarative_base()

class CCTradeBotDB(object):
    _session = None

    @property
    def session(self):
        if not self._session:
            self.session = sessionmaker(bind=engine)()
        return self._session

    @session.setter
    def session(self, val):
        self._session = val


db = CCTradeBotDB()