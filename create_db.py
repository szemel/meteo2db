import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, text, Boolean
from sqlalchemy.dialects.mysql import INTEGER, FLOAT, VARCHAR
from sqlalchemy.orm import Session

Base = declarative_base()


class MeteoData(Base):
    __tablename__ = 'meteo_data'

    id = Column(Integer, primary_key=True)
    value = Column(FLOAT(nullable=False))
    when = Column(DateTime)
    type = Column(INTEGER(unsigned=True))


class CreateDatabase(object):

    def __init__(self):
        self.engine = None
        self.session = None
        self.db_engine = "mysql"
        self.db_user = "location_root"
        self.db_password = "test"
        self.db_name = 'meteo'

    def connect(self):
        if not self.engine:
            self.engine = sqlalchemy.create_engine(
                self.db_engine + '://' + self.db_user + ':' + self.db_password + '@localhost')
        self.engine.execute("USE " + self.db_name)  # select new db
        self.session = Session(self.engine)
        return self.session

    def create_database(self):
        self.engine = sqlalchemy.create_engine(self.db_engine+'://'+self.db_user+':'+self.db_password+'@localhost')  # connect to server
        # self.engine.execute("DROP DATABASE IF EXISTS "+self.db_name)  # create db
        self.engine.execute("CREATE DATABASE "+self.db_name)  # create db
        # self.engine.execute("SET @@global.time_zone = '+00:00'")  # create db

    def create_tables(self):
        Base.metadata.create_all(self.engine)


if __name__ == "__main__":
    test=CreateDatabase()
    # test.create_database()
    test.connect()
    test.create_tables()
