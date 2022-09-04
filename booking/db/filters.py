from . import models as m


def room_by_reserve(session, reserve_id, roomnumber=None):
    query = session.query(m.Room).filter(m.Room.id == reserve_id)
    if roomnumber:
        query = query.join(m.Room.id).\
                    join(m.Reserve.roomid)
        query = query.filter(m.Reserve.roomid == roomnumber)
    return {row.name: row.id for row in query.all()}
