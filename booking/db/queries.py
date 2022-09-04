from . import models as m
# sample

def qry_room_view(session):
    query = session.query(
        m.Room.id.label('room_id'),
        m.Room.roomnumber.label('roomnumber'),
        m.Room.countbedroom.label('countbedroom'),
        m.Room.price.label('price'),
        m.Room.description.label('description'),
        m.Reserve.personid.label('personid'),
        m.Reserve.startdate.label('startdate'),
        m.Reserve.enddate.label('enddate'),
        m.Reserve.pricesum.label('pricesum'),
        )
    query = query.select_from(m.Room).join(m.Reserve)
    result = {
         row.room_id:
                {'roomnumber':row.roomnumber ,
                'countbedroom':row.countbedroom,
                'price': row.price,
                'description': row.description ,
                'personid': row.personid ,
                'startdate': row.startdate ,
                'enddate': row.enddate ,
                'pricesum': row.pricesum ,
                } for row in query.all()
        }
    return result


# def qry_filter_vehiclemodel(session, vehiclemake_id=None):
#     query = session.query(m.VehicleModel)
#     if vehiclemake_id:
#         query = query.filter(m.VehicleModel.vehiclemake_id == vehiclemake_id)
#     return {row.name: row.id for row in query.all()}


# def qry_vehicletrim_view(session):
#     query = session.query(
#         m.VehicleMake.name.label('make_name'),
#         m.VehicleModel.name.label('model_name'),
#         m.VehicleTrim.name.label('trim_name'),
#         m.VehicleTrim.id.label('trim_id')
#     )
#     query = query.select_from(m.VehicleTrim).\
#         join(m.VehicleTrim.vehiclemodel).\
#         join(m.VehicleModel.vehiclemake)
#     result = {
#         row.trim_id: {'make': row.make_name, 'model': row.model_name, 'trim': row.trim_name} for row in query.all()
#     }
#     return result
