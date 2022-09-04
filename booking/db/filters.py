from . import models as m


# def vehiclemake_by_vehicleyear(session, year):
#     query = session.query(m.VehicleMake)
#     query = query.join(m.VehicleMake.vehiclemodels).\
#         join(m.VehicleModel.vehicletrims).\
#         join(m.VehicleTrim.vehicleyears)
#     query = query.filter(m.VehicleYear.year == year)
#     return {row.name: row.id for row in query.all()}


# def vehiclemodel_by_vehiclemake(session, vehiclemake_id, year=None):
#     query = session.query(m.VehicleModel).filter(m.VehicleModel.vehiclemake_id == vehiclemake_id)
#     if year:
#         query = query.join(m.VehicleModel.vehicletrims).\
#             join(m.VehicleTrim.vehicleyears)
#         query = query.filter(m.VehicleYear.year == year)
#     return {row.name: row.id for row in query.all()}


def room_by_reserve(session, reserve_id, roomnumber=None):
    query = session.query(m.Room).filter(m.Room.id == reserve_id)
    if roomnumber:
        query = query.join(m.Room.id).\
                    join(m.Reserve.roomid)
        query = query.filter(m.Reserve.roomid == roomnumber)
    return {row.name: row.id for row in query.all()}
