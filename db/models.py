from sqlalchemy import create_engine, Column, Integer, String, DateTime, \
     ForeignKey, DECIMAL, Numeric
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relation

from sqlalchemy.ext.declarative import declarative_base 

# postgresql+psycopg2://user:password@host:port/dbname[?key=value&key=value...]
engine = create_engine("postgresql://postgres:admin@localhost:5432/Booking", client_encoding="utf8")
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Model = declarative_base(name='Model')
Model.query = db_session.query_property()

def init_db():
    Model.metadata.create_all(bind=engine)


class UserType(Model):
    __tablename__ = 'UserType'
    id = Column('UserTypeID', Integer, primary_key=True)
    title = Column(String(200))
    
class Access(Model):
    __tablename__= 'Access'
    id = Column('AccessID', Integer, primary_key=True)
    type = Column('UserType_ID', Integer, ForeignKey('UserType.UserTypeID'))
    id2 = Column('Page_ID', Integer, ForeignKey('Page.PageID'))
    
class Page(Model):
    __tablename__='Page'
    id = Column('PageID', Integer, primary_key=True)
    name = Column('PageName', String(100))
    

class Person(Model):
    __tablename__ = 'Person'
    id = Column('PersonID', Integer, primary_key=True)
    user = Column ('UserType_ID',Integer, ForeignKey('UserType.UserTypeID'))
    name = Column('UserName', String(200))
    family = Column('Family', String(200))
    email = Column('Email', String(100))
    tel = Column('Telephone', String(10))
    address = Column('Address', String(200))


class Reserve(Model):
    __tablename__ = 'Reserve'
    id = Column('ReserveID', Integer, primary_key=True)
    roomid = Column('Room_ID', Integer, ForeignKey('Room.RoomID'))
    personid = Column('Person_ID', Integer, ForeignKey('Person.PersonID'))
    startdate = Column('StartDate', DateTime)
    enddate = Column('EndDate', DateTime)
    pricesum = Column('PriceSum', DECIMAL)
    
class Room(Model):
    __tablename__ = 'Room'
    id = Column('RoomID', Integer, primary_key = True)
    roomnumber = Column('RoomNumber', Numeric)
    countbedroom = Column('CountBedroom', Numeric)
    price = Column('Price', DECIMAL)
    description = Column('Description', String(350))

