from . import models as m


def filter_room_by_reserve(session, reserve_id, roomnumber=None):
    print('filter_room_by_reserve')
    query = session.query(m.Room).filter(m.Room.id == reserve_id)
    if roomnumber:
        query = query.join(m.Room.id).\
                    join(m.Reserve.id)
        query = query.filter(m.Reserve.id == roomnumber)
    return {row.name: row.id for row in query.all()}

