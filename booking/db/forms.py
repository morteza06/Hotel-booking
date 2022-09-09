from . import models as m 
"""" Gol of this desing
    difine meta data ; model, fields, field_class   define some query
"""
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
    # roomnumber = Field(label='roomnumber')
    # countbedroom = Field(label='countbedroom')
    # price = Field(label='price')
    # description = Field(label='description')
        
    def save(self, session, data):
        print('Save in RoomAddFrom===========')
        new_room =  m.Room( roomnumber= data['roomnumber'], countbedroom = data['countbedroom'], \
                            price= data['price'], description= data['description'] )
        print(new_room)
        session.add(new_room)
        session.commit()
    # {'roomnumber': new_room.roomnumber, 'countbedroom': new_room.countbedroom, 'price': new_room.price, \
                # 'description': new_room.description }
       
class SearchForm(Form):
    
    searchtext = Field(label='searchtext')
    searchby = Field(label='searchby')
        
    from tkinter import messagebox

    def search(self,session,data):
        # print(data['searchtext']['values'])
        print(data.items())
        
        if self.fields.get('searchby') == '':
            self.messagebox.showinfo('Information','Please Insert text for search ')
        if self.fields.get('searchtext') == '':
            self.messagebox.showinfo('Information','Please Select  search type ')
            # print(data.items())
        else:
            print('===>',data.get('searchby'),'==>',data.get('searchtext'))
            Qsearch = session.query(m.Room).filter(m.Room.roomnumber == self.fields.get('searchby'))
        return  
        # return {'roomnumber': new_room.roomnumber, 'countbedroom': new_room.countbedroom, 'price': new_room.price, 'description': new_room.description }
       
class ReserveForm(Form):
    roomid = Field(label='roomid')
    personid = Field(label='personid')
    startdate = Field(label='startdate')
    enddate = Field(label='enddate')
    pricesum = Field(label='pricesum')
        
    def save(self, session, data):
        print('Save in ReserveForm ====')
        new_reserve =  m.Reserve( roomid= data['roomid'], personid= data['personid'],\
                            startdate= data['startdate'], enddate= data['enddate'], pricesum= data['pricesum'] )
        # print(new_reserve)
        session.add(new_reserve)
        session.commit()
          
class PersonForm(Form):
    pass
