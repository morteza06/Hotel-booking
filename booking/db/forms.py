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



class RoomAddForm:
    # roomnumber = Field(label='Room Number')
    # countbedroom = Field(label='Room countbedroom')
    # price = Field(label='Room price')
    # description = Field(label='Room Description')
    
    # def __init__(self, session, data=None):
    #    pass
    
    fields = {
        'roomnumber': {'label': 'roomnumber', 'required': True},
        'countbedroom': {'label': 'countbedroom', 'required': True},
        'price': {'label': 'price', 'required': True},
        'description': {'label': 'description', 'required': True}
    }
        
    def save(self, session, data):
        new_room =  m.Room( roomnumber= data['roomnumber'], countbedroom= data['countbedroom'],\
                            price= data['price'], description= data['description'] )
        print(new_room)
        session.add(new_room)
        session.commit()
        
        
class RoomSelectForm(Form):
    pass
#     roomnumber = Field(label='RoomNumber')
#     countbedroom = Field(label='CountRoom')
#     price = Field(label='Price')
#     description = Field(label='Description')

#     def __init__(self, session, data=None):
#         self.data = data
#         self.session = session
#         if not self.data:
#             q_room = session.query(m.Room).distinct().order_by(m.Room.roomnumber)
#             self.roomnumber.values={str(row.roomnumber): row.roomnumber for row in q_room.all()}
#             print(self.roomnumber.values)
#             print('RoomAddForm ==> run query')
#         print('db.forms ==> init  RoomAddForm')
        
        
#     def save(self, session, data):
#         new_room = m.Room(roomnumber=data['roomnumber'], countbedroom=data['countbedroom'],\
#                         price=data['price'], description=data['description'])
#         session.add(new_room)
#         session.commit()
#         return {'name':new_room.roomnumber,'id':new_room.id}