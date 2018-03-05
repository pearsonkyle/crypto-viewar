
from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc
from sqlalchemy.sql import text

from datetime import datetime
import json

Base = declarative_base() 

class Database():
    '''
        Simplification for creating connections to different db with sqlalchemy

        settings = json.load(open(settings,'r'))
        data type = column formats
    '''

    def __init__(self, settings=None, dtype=None):
        self.settings = settings
        self.dtype = dtype

        # connect to data base
        self.create_session()
    
    def create_session(self):
        # connect to data base
        self.engine = create_engine(self.engine_string)
        Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)
        self.sess = self.DBSession()

    @property
    def count(self):
        return self.session.query(self.dtype).count()
        
    @property
    def engine_string(self):
        mystring = "{}://{}:{}@{}:{}/{}".format(
                                    self.settings['dialect'],
                                    self.settings['username'],
                                    self.settings['password'],
                                    self.settings['endpoint'],
                                    self.settings['port'],
                                    self.settings['dbname'] )
        return mystring

    def _check_session(foo):
        def magic( self ) :
            try:
                return foo( self )
            except:
                self.create_session()
                print('creating session')
                return foo( self )
        return magic

    @property
    @_check_session
    def session(self):
        return self.sess

    def query_recent(self,KEY='eth',n=721,datetimes=False):
        # get most recent entry based on timestamp 
        recent = self.session.query(self.dtype).order_by(desc(self.dtype.timestamp)).limit(n).all()
        values = [recent[i][KEY] for i in range(len(recent))][::-1]
        dates = [recent[i].timestamp for i in range(len(recent))][::-1]

        if not datetimes:
            dates = date2num(dates)

        return dates,values

    def close(self):
        self.sess.close()
        self.engine.dispose()

            
class Cryptocurrency(Base):
    __tablename__ = "cryptocurrency" # TODO change to gdax?

    # define columns of table
    timestamp = Column(DateTime, default=datetime.now(), primary_key=True) # 'Jun 1 2005  1:33PM'
    btc = Column(Float)
    ltc = Column(Float)
    eth = Column(Float)
    #bch = Column(Float)

    def cols(self):
        return ['timestamp','btc','ltc','eth']

    def keys(self):
        return ['btc','ltc','eth']

    # convert below to different class     
    def get(self,key='None'):
        if hasattr(self, key):
            return getattr(self,key)
        else:
            raise Exception("no key: {}".format(key))

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, val):
        if hasattr(self, key):
            setattr(self,key,val)
        else:
            raise Exception("no key: {}".format(key))
            
    def __repr__(self):
        string = " <" + str(type(self).__name__) + "> " 
        for k in self.keys():
            string += "{}:{}, ".format(k,self[k])
        return string[:-2]
    
    def toDict(self):
        js = {}
        for k in self.cols():
            if isinstance(self[k],type(datetime.now()) ):
                js[k] = self[k].strftime('%Y-%m-%d %H:%M:%S')
            else:
                js[k] = self[k]
        return js
    
    def toJSON(self):
        return json.dumps(self.toDict())

if __name__ == "__main__":
    # set up database connection 
    db = Database( settings=json.load(open("readonly.json",'r')),
                   dtype=Cryptocurrency )
    
    data = db.session.query(db.dtype).limit(100).all()