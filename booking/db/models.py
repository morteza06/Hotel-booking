from tkinter import CASCADE
from sqlalchemy import Column, Integer, String, DATE, \
     ForeignKey, DECIMAL, Numeric,Table
from sqlalchemy.orm import  relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref

# TODO
# 1-Validates data at each model. 
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


class UserType(Base): # Not delte 
    __tablename__ = 'UserType'
    id = Column('UserTypeID', Integer, primary_key=True) 
    title = Column(String(200))
    
    def __repr__(self):
        return 'UserType({})'.format(self.title)
    
class Access(Base):
    __tablename__ = 'Access'
    id = Column('AccessID', Integer, primary_key=True)
    type = Column('UserType_ID', Integer, ForeignKey('UserType.UserTypeID', ondelete='CASCADE')) 
    id2 = Column('Page_ID', Integer, ForeignKey('Page.PageID'))
    
    #help that is => https://stackoverflow.com/questions/5033547/sqlalchemy-cascade-delete
    UserType = relationship(UserType, backref= backref('Access', passive_deletes=True))
    
class Page(Base):
    __tablename__= 'Page'
    id = Column('PageID', Integer, primary_key=True)
    name = Column('PageName', String(100))
    
    def __repr__(self) -> str:
        return 'Page({})'.format(self.name)

class Person(Base): #User table
    __tablename__ = 'Person'
    id = Column('PersonID', Integer, primary_key=True)
    user = Column ('UserType_ID',Integer, ForeignKey('UserType.UserTypeID', ondelete='ISNULL'))
    name = Column('UserName', String(200))
    family = Column('Family', String(200))
    email = Column('Email', String(100))
    tel = Column('Telephone', String(10))
    address = Column('Address', String(200))
    
    UserType = relationship(UserType, backref = backref('Person', passive_deletes=True)) 
    
    def __repr__(self) -> str:
        return 'Person({}{})'.format(self.name, self.family)

class Room(Base):
    __tablename__ = 'Room'
    id = Column('RoomID', Integer, primary_key = True)
    roomnumber = Column('RoomNumber', Integer)
    countbedroom = Column('CountBedroom', Numeric)
    price = Column('Price', DECIMAL)
    description = Column('Description', String(350))

    def __repr__(self) -> str:
        return 'Room({}{}{})'.format(self.roomnumber, self.countbedroom, self.price)
    
class Reserve(Base):
    __tablename__ = 'Reserve'
    id = Column('ReserveID', Integer, primary_key=True)
    roomid = Column('Room_ID', Integer, ForeignKey('Room.RoomID', ondelete='ISNULL',))
    personid = Column('Person_ID', Integer, ForeignKey('Person.PersonID', ondelete='ISNULL'))
    startdate = Column('StartDate', DATE)
    enddate = Column('EndDate', DATE)
    pricesum = Column('PriceSum', DECIMAL)
    
    room = relationship(Room, backref = backref('Reserve', passive_deletes=False))
    person = relationship(Person, backref = backref('Reserve', passive_deletes=False))
    
    def __repr__(self) -> str:
        return 'Reserve({}{})'.format(self.roomid,self.pricesum)

