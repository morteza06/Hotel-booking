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
    print(result)
    return result


