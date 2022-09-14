from . import models as m
# sample


def qry_room_view(session):
    query = session.query(
        m.Room.id.label('id'),
        m.Room.roomnumber.label('roomnumber'),
        m.Room.countbedroom.label('countbedroom'),
        m.Room.price.label('price'),
        m.Room.description.label('description'),
        m.Reserve.personid.label('personid'),
        m.Reserve.startdate.label('startdate'),
        m.Reserve.enddate.label('enddate'),
        m.Reserve.pricesum.label('pricesum'),
        )
    # query = query.select_from(m.Room)
    query = query.select_from(m.Room).join(m.Reserve)
    result = {
         row.id:
                {'id':row.id ,
                'roomnumber':row.roomnumber ,
                'countbedroom':row.countbedroom,
                'price': row.price,
                'description': row.description ,
                'personid': row.personid ,
                'startdate': row.startdate ,
                'enddate': row.enddate ,
                'pricesum': row.pricesum ,
                } for row in query.all()
        }
    print('output view=====',result)
    return result

def qry_room_showall(session):
    query=None
    result={}
    query = session.query(
        m.Room.id.label('id'),
        m.Room.roomnumber.label('roomnumber'),
        m.Room.countbedroom.label('countbedroom'),
        m.Room.price.label('price'),
        m.Room.description.label('description'),
        )
    # query = query.select_from(m.Room)
    result = {
         row.id:
                {'id':row.id ,
                'roomnumber':row.roomnumber ,
                'countbedroom':row.countbedroom,
                'price': row.price,
                'description': row.description ,
                } for row in query.all()
        }
    print('out put query==== ',result.items())
    return result

def qry_reserve_showall(session):
    query=None
    result={}
    query = session.query(
        m.Reserve.id.label('id'),
        m.Reserve.roomid.label('roomid'),
        m.Room.roomnumber.label('roomnumber'),
        m.Reserve.personid.label('personid'),
        m.UserType.title.label('title'),
        m.Person.name.label('name'),
        m.Person.family.label('family'),
        m.Reserve.startdate.label('startdate'),
        m.Reserve.enddate.label('enddate'),
        m.Reserve.pricesum.label('pricesum'),
        )
    query = query.select_from(m.Room).join(m.Reserve).join(m.Person).join(m.UserType)
    result = {
         row.roomid:
                {'id':row.id ,
                'roomid':row.roomid ,
                'roomnumber':row.roomnumber ,
                'personid':row.personid ,
                'title':row.title ,
                'name':row.name ,
                'family':row.family ,
                'startdate':row.startdate,
                'enddate': row.enddate,
                'pricesum': row.pricesum
                } for row in query.all()
        }
    return result

def qry_user_showall(session):
    query=None
    result={}
    query = session.query(
        m.Person.id.label('id'),
        m.UserType.title.label('title'),
        m.Person.name.label('name'),
        m.Person.family.label('family'),
        m.Person.email.label('email'),
        m.Person.tel.label('tel'),
        m.Person.address.label('address'),
        )
    query = query.select_from(m.Person).join(m.UserType)
    result = {
         row.id:
                {'id':row.id ,
                'title':row.title,
                'name':row.name,
                'family':row.family,
                'email':row.email,
                'tel':row.tel,
                'address':row.address
                } for row in query.all()
        }
    return result

def qry_usertype_showall(session):
    query=None
    result={}
    query = session.query(
        m.UserType.id.label('id'),
        m.UserType.title.label('title'),
        )
    query = query.select_from(m.UserType)
    result = {
         row.id:
                {'id':row.id ,
                'title':row.title,
                } for row in query.all()
        }
    return result


