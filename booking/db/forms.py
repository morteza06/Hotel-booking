from sqlalchemy import inspect, delete, update
from . import models as m 
"""" Gol of this desing
    difine meta data ; model, fields, field_class   define some query
"""
from tkinter import  messagebox
class Field:
    def __init__(self,  label=None, value=None ):
        self.label = label
        self.value = value
       

class Form:
    def __new__(cls, *args, **kwargs):
        cls._fields = {}
        for k, v in vars(cls).items():
            if isinstance(v, Field):
                cls._fields[k] = v
        return super().__new__(cls)
    
    
    @property
    def fields(self)->dict:
        f = {}
        for key, field in self._fields.items():
            f[key] = vars(field)
        return f


class RoomForm(Form):
    id = Field(label='id')
    roomnumber = Field(label='roomnumber')
    countbedroom = Field(label='countbedroom')
    price = Field(label='price')
    description = Field(label='description')
    searchtext = Field(label='searchtext')
    searchby = Field(label='searchby')
     
    def __init__(self, session, data=None):
        self.data = data
        self.session = session

    def add_room(self,data):
        print('Save in RoomAddFrom===========')
        query =  m.Room( roomnumber= data['roomnumber'], countbedroom = data['countbedroom'], \
                            price= data['price'], description= data['description'] )
        try:
            self.session.add(query)
            self.session.commit()
            idd=query.id # find id after insert committed to database ,because id value is incrimental.
        except Exception as e:
            messagebox.showinfo('warning','Room Add Form caought an error! {}'.format(e))
            self.session.rollback()
            raise
        finally:
            self.session.close()
        return idd
            
    def delete_room(self,id):
        try:
            x=self.session.query(m.Room).get(id)
            self.session.delete(x)
            self.session.commit()
            messagebox.showinfo(title='Information',message='Commplete Delete the row with id')
        except Exception as e:
            self.session.rollback()
            messagebox.showinfo(title='error',message='Delete from Room table caought an error!\n {}'.format(e))
            raise
        finally:
            self.session.close()
            
    def update_room(self,data):
        try:
            self.data=data
            self.session.query(m.Room).filter(m.Room.id == self.data['id'].get()).\
                updata(
                        {m.Room.roomnumber: self.data['roomnumber'].get() ,
                        m.Room.countbedroom: self.data['countbedroom'].get(),
                        m.Room.price: self.data['price'].get(),
                        m.Room.description: self.data['description'].get() 
                        }
                    )
            self.session.commit()
            messagebox.showinfo(title='Information',message='Commplete Update the row with id')
        except Exception as e:
            self.session.rollback()
            messagebox.showinfo(title='error',message='Delete from Room table caought an error!\n {}'.format(e))
            raise
        finally:
            self.session.close()
       
class SearchRoomForm(Form):
         
    from tkinter import messagebox
    def search(self, data, session)->dict:
        try:
            self.data=data
            Qsearch=""
            print('search by===',self.data['searchby'])
            print('search text===',self.data['searchtext'])
            # if self.data['id'] !='':
                # Qsearch = session.query(m.Room).filter(m.Room.id==data['id']).first()
            if self.data['searchby'] == '':
                self.messagebox.showinfo('Information','Please Select type of search search ')
            elif self.data['searchby'] == 'RoomNumber':
                Qsearch = session.query(m.Room).filter(m.Room.roomnumber == self.data['searchtext'])
                # print(searchby)
            elif self.data['searchby'] == 'CountBedroom':
                Qsearch = session.query(m.Room).filter(m.Room.countbedroom == self.data['searchtext'])
                # print(searchby)
            elif self.data['searchby'] == 'Price[>=]YourEnter':
                Qsearch = session.query(m.Room).filter(m.Room.price >= self.data['searchtext'])
                # print(searchby)
            elif self.data['searchby'] == 'Price[<=]YourEnter':
                Qsearch = session.query(m.Room).filter(m.Room.price <= self.data['searchtext'])
                # print(data['searchtext']['values'])
                # print(data.items())
            print('**********',Qsearch)
            self.data={}
            self.data = {
                row.id:
                        {'id':row.id ,
                        'roomnumber':row.roomnumber ,
                        'countbedroom':row.countbedroom,
                        'price': row.price,
                        'description': row.description ,
                        } for row in Qsearch.all()
                }
        except Exception as e: 
            messagebox.showerror(title='Error',message='Error in search data:\n{}',\
                                detail=str(e))
        else:
          
            # data = object_as_dict(Qsearch)
            print('==**==',self.data.items())
            return self.data
        finally:
            print('finally search data complete. ')
    
class ReserveForm(Form):
    roomid = Field(label='roomid')
    personid = Field(label='personid')
    startdate = Field(label='startdate')
    enddate = Field(label='enddate')
    pricesum = Field(label='pricesum')
    
    def __init__(self, session, data=None):
        self.data = data
        self.session = session
        
    def add_reserve(self,data):
        query =  m.Reserve( roomid= data['roomid'], personid = data['personid'], \
                            startdate= data['startdate'], enddate= data['enddate'], pricesum = data['pricesum'] )
        try:
            self.session.add(query)
            self.session.commit()
            idd=query.id # find id after insert committed to database ,because id value is incrimental.
        except Exception as e:
            messagebox.showinfo('warning','Reserve Add Form caought an error! {}'.format(e))
            self.session.rollback()
            raise
        finally:
            self.session.close()
        return idd
    
    def delete_reserve(self,id):
        try:
            x=self.session.query(m.Reserve).get(id)
            self.session.delete(x)
            self.session.commit()
            messagebox.showinfo(title='Information',message='Commplete Delete the row with id')
        except Exception as e:
            self.session.rollback()
            messagebox.showinfo(title='error',message='Delete from Reserve table caought an error!\n {}'.format(e))
            raise
        finally:
            self.session.close()

class UserForm(Form):
    def __init__(self, session, data=None):
        self.data = data
        self.session = session
        
    def add_user(self,data):
        query =  m.Person( usertype= data['usertype'], personid = data['username'], \
                            family= data['family'], email= data['email'], telephone = data['tel'] , \
                                address = data['address'])
        try:
            self.session.add(query)
            self.session.commit()
            idd=query.id # find id after insert committed to database ,because id value is incrimental.
        except Exception as e:
            messagebox.showinfo('warning','User Add Form caought an error! {}'.format(e))
            self.session.rollback()
            raise
        finally:
            self.session.close()
        return idd
            
    def delete_user(self,id):
        try:
            x=self.session.query(m.Person).get(id)
            self.session.delete(x)
            self.session.commit()
            messagebox.showinfo(title='Information',message='Commplete Delete the row with id')
        except Exception as e:
            self.session.rollback()
            messagebox.showinfo(title='error',message='Delete from User table caought an error!\n {}'.format(e))
            raise
        finally:
            self.session.close()
  
    def update_user(self):
        pass
 
class UserTypeForm(Form):
    def __init__(self, session , data=None):
        self.data = data
        self.session = session
 
    def add_usertype(self,  data):
        query =  m.UserType( title= data['title'])
        try:
            self.session.add(query)
            self.session.commit()
            idd=query.id # find id after insert committed to database ,because id value is incrimental.
        except Exception as e:
            messagebox.showinfo('warning','User Type Add Form caought an error! {}'.format(e))
            self.session.rollback()
            raise
        finally:
            self.session.close()
        return idd
    
    def delete_usertype(self,id):
        try:
            x=self.session.query(m.UserType).get(id) 
            self.session.delete(x)
            self.session.commit()
            self.session.commit()
            messagebox.showinfo(title='Information',message='Commplete Delete the row with id')
        except Exception as e:
            self.session.rollback()
            messagebox.showinfo(title='error',message='Delete from UserType table caought an error!\n {}'.format(e))
            raise
        finally:
            self.session.close()   
        pass
    
    def update_usertype(self):
        pass
    
  
    