from . import models as m 

class Field:
    def __init__(self, default=None, disable=False, initial=None, label=None, required=True, values=None ):
        self.default = default
        self.disable = disable
        self.initial = initial
        self.label = label
        self.required = required
        self.values = values or {}

class Form:
    def __new__(cls, *args, **kwargs):
        cls._fields = {}
        for k, v in vars(cls).items():
            if isinstance(v, Field):
                cls._fields[k] = v
        return super().__new__(cls)
    
    
    @property
    def fields(self):
        f = {}
        for key, field in self._fields.items():
            f[key] = vars(field)
        return f



class RoomAddForm(Form):
    roomnumber = Field(label='roomnumber')
    countbedroom = Field(label='countbedroom')
    price = Field(label='price')
    description = Field(label='description')
        
    def save(self, session, data):
        print('Save in RoomAddFrom===========')
        new_room =  m.Room( roomnumber= data['roomnumber'], countbedroom= data['countbedroom'], \
                            price= data['price'], description= data['description'] )
        print(new_room)
        session.add(new_room)
        session.commit()
        return {'roomnumber': new_room.roomnumber, 'countbedroom': new_room.countbedroom, 'price': new_room.price, \
                'description': new_room.description }
       
class SearchForm(Form):
    searchtext = Field(label='searchtext')
    searchby = Field(label='searchby')
        
    def search(self, session, data, searchby):
        print('Save in SearchForm===========')
        # self.Search
        # qr = session.query(Room).\
        #         filter(Room.searchby == )
        # print(new_room)
        # session.add(new_room)
        # session.commit()
        # return {'roomnumber': new_room.roomnumber, 'countbedroom': new_room.countbedroom, 'price': new_room.price, 'description': new_room.description }
       
class ReserveInfoAddForm(Form):
    roomid = Field(label='roomid')
    personid = Field(label='personid')
    startdate = Field(label='startdate')
    enddate = Field(label='enddate')
    pricesum = Field(label='pricesum')
        
    def save(self, session, data):
        print('Save in ReserveInfoAddForm ====')
        new_reserve =  m.Reserve( roomid= data['roomid'], personid= data['personid'],\
                            startdate= data['startdate'], enddate= data['enddate'], pricesum= data['pricesum'] )
        # print(new_reserve)
        session.add(new_reserve)
        session.commit()
        return {'roomid': new_reserve.roomid, 'personid': new_reserve.personid, 'startdate': new_reserve.startdate, \
                'enddate': new_reserve.enddate, 'pricesum': new_reserve.pricesum }
          
class RoomSelectForm(Form):
    
    # id = Field(label='id')
    roomnumber = Field(label='roomnumber')
    # countbedroom = Field(label='countbedroom')
    # price = Field(label='price')
    # description = Field(label='description')
  
    def __init__(self, session, data, **kwargs):
        self.data = data
        print(self.data)
        self.session = session
        q_room = session.query(m.Room)
        self.values ={['id'][row.id]:['roomnumber'][row.roomnumber] for row in q_room.all()}
        print(self.values,"*/*/*/*")
        data = self.values 
        print('RoomAddForm ==> run query')
        print('db.forms ==> init  RoomAddForm')
        return None
        
