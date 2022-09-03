from cgi import print_exception
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
        for key, field in self._fields.items()
            f[key] = vars(field)
        return f

class RoomAddForm(Form):
    roomNumber = Field(label='Room Number')
    countbedroom = Field(label='Room Number')
    print_exception = Field(label='Room Number')
    description = Field(label='Room Number')
    def __init__(self, session, data=None):
        self.data = data
        self.session = session
    # have bug
        q_add = session.query(m.Room.add())