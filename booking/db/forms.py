from sqlalchemy import inspect, delete, update,select
from . import models as m 
from tkinter import  messagebox

class RoomForm():

    def __init__(self, session, data=None):
        self.data = data
        self.session = session

    def add_room(self,data):
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
            x=self.session.query(m.Room).filter(m.Room.id==id).first()
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
       
class ReserveForm():
    
    def __init__(self, session, data=None):
        self.data = data
        self.session = session
        
    def add_reserve(self,room_id,data):
        query =  m.Reserve( roomid= room_id , personid = data['personid'], \
                            startdate = data['startdatetime'], enddate= data['enddatetime'], pricesum = data['pricesum'] )
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
            x = self.session.query(m.Reserve).filter(m.Reserve.id==id).first()
            self.session.delete(x)
            self.session.commit()
            messagebox.showinfo(title='Information',message='Commplete Delete the row with id')
        except Exception as e:
            self.session.rollback()
            messagebox.showinfo(title='error',message='Delete from Reserve table caought an error!\n {}'.format(e))
            raise
        finally:
            self.session.close()

    # disable to refactor
    def find_price_reserve(self, id):
        q = (self.session.query(m.Room.price).
             filter(m.Room.id == id))
        result = q.first()
        
        if not result: 
            self.session.close()
            raise
        else: 
            self.session.close()
            return result
    
    def list_person_info(self):
        pass

class UserForm():
  
    def __init__(self, session, data=None):
        self.data = data
        self.session = session
        
    def add_user(self,data,usertype_id):
        query =  m.Person( user= usertype_id, name = data['name'], \
                            family= data['family'], email= data['email'], tel = data['tel'] , \
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
            x=self.session.query(m.Person).filter(m.Person.id==id).first()
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
 
class UserTypeForm():
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
            x=self.session.query(m.UserType).filter(m.UserType.id==id).first()
            self.session.delete(x)
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
    
class SearchRoomForm():
    
    from tkinter import messagebox
    def search(self, data, session)->dict: 
        self.session = session
        result=[]
        query=None
        try:
            self.data = data
            searchby = self.data['searchby']
            searchtext = self.data['searchtext']
            if  searchby == '' and searchtext == '':
                self.messagebox.showinfo('Information','Please select type of search and enter text search. ')
            elif searchby == 'RoomNumber':
                query = self.session.query(m.Room.id,m.Room.roomnumber,m.Room.countbedroom,m.Room.price,m.Room.description).filter(m.Room.roomnumber == searchtext)
            elif  searchby == 'CountBedroom':
                query = self.session.query(m.Room.id,m.Room.roomnumber,m.Room.countbedroom,m.Room.price,m.Room.description).filter(m.Room.countbedroom == searchtext)
            elif  searchby == 'Price[>]YourEnter':
                query = self.session.query(m.Room.id,m.Room.roomnumber,m.Room.countbedroom,m.Room.price,m.Room.description).filter(m.Room.price >searchtext)
            elif searchby == 'Price[<]YourEnter':
                query = self.session.query(m.Room.id,m.Room.roomnumber,m.Room.countbedroom,m.Room.price,m.Room.description).filter(m.Room.price < searchtext)
            if query != None:
                # result = query
                # print(type(result))
                    result={
                        row.id:
                            {'id':row.id ,
                            'roomnumber':row.roomnumber ,
                            'countbedroom':row.countbedroom ,
                            'price':row.price ,
                            'description':row.description ,
                            } for row in query.all()
                    }
            else: 
                result={}
            
        except Exception as e: 
            messagebox.showerror(title='Error' ,message='Error in search data:\n',\
                                detail=str(e))
        else:
            messagebox.showinfo(title='Information',message='          Search complete.        ')
            print('==Search Done ==',result.items())
            return result
        finally:
            return result
            print('finally search data complete. ')