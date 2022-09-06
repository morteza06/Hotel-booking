from sqlalchemy import Column, Integer, String, DATE, \
     ForeignKey, DECIMAL, Numeric,Table
from sqlalchemy.orm import  relationship
from sqlalchemy.ext.declarative import declarative_base

# TODO
# 1-Validates data at each model. difine __reper__, and any builtin method you need.
# 2-Exception handling with ORM complier with postgresql for ex. foreginkey , keyerror, type error
# init class Integer and string from sqlalchemy.types,TypeDecorator, @complier(sqlalchemy.types.TypeDecorator) metho copmile_string_postgresql



#Table
class Base(object):
    @classmethod
    def __table_cls__(cls, *args, **kwargs):
        t = Table(*args, **kwargs)
        t.decl_class = cls
        return t
    
    
class_registry ={}
Base = declarative_base(cls=Base, class_registry=class_registry)


class UserType(Base):
    __tablename__ = 'UserType'
    id = Column('UserTypeID', Integer, primary_key=True)
    title = Column(String(200))
    
class Access(Base):
    __tablename__ = 'Access'
    id = Column('AccessID', Integer, primary_key=True)
    type = Column('UserType_ID', Integer, ForeignKey('UserType.UserTypeID'))
    id2 = Column('Page_ID', Integer, ForeignKey('Page.PageID'))
    
class Page(Base):
    __tablename__= 'Page'
    id = Column('PageID', Integer, primary_key=True)
    name = Column('PageName', String(100))
    

class Person(Base):
    __tablename__ = 'Person'
    id = Column('PersonID', Integer, primary_key=True)
    user = Column ('UserType_ID',Integer, ForeignKey('UserType.UserTypeID'))
    name = Column('UserName', String(200))
    family = Column('Family', String(200))
    email = Column('Email', String(100))
    tel = Column('Telephone', String(10))
    address = Column('Address', String(200))


class Reserve(Base):
    __tablename__ = 'Reserve'
    id = Column('ReserveID', Integer, primary_key=True)
    roomid = Column('Room_ID', Integer, ForeignKey('Room.RoomID'))
    personid = Column('Person_ID', Integer, ForeignKey('Person.PersonID'))
    startdate = Column('StartDate', DATE)
    enddate = Column('EndDate', DATE)
    pricesum = Column('PriceSum', DECIMAL)
    

class Room(Base):
    __tablename__ = 'Room'
    id = Column('RoomID', Integer, primary_key = True)
    roomnumber = Column('RoomNumber', Numeric)
    countbedroom = Column('CountBedroom', Numeric)
    price = Column('Price', DECIMAL)
    description = Column('Description', String(350))

