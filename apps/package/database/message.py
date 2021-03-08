from sqlalchemy import Column, Numeric, Integer, String, DateTime, Boolean
from package.database.base import Base


class Message(Base):
    """
    Table message
    """
    __tablename__ = 'message'

    message_id = Column(Integer, primary_key=True, nullable=False)
    message_type = Column(String, nullable=False)
    transmission_type = Column(Integer)
    session_id = Column(Integer)
    aircraft_id = Column(Integer)
    hex_id = Column(String)
    flight_id = Column(Integer)
    call_sign_nm = Column(Integer)
    altitude_value = Column(Integer)
    ground_speed_value = Column(Numeric)
    track_value = Column(Numeric)
    latitude_value = Column(Numeric)
    longitude_value = Column(Numeric)
    vertical_rate_value = Column(Numeric)
    squawk_value = Column(Integer)
    alert_flg = Column(Boolean)
    emergency_flg = Column(Boolean)
    spi_flg = Column(Boolean)
    is_on_ground_flg = Column(Boolean)
    generation_dttm = Column(DateTime)
    received_dttm = Column(DateTime)
    creation_dttm = Column(DateTime)

    def __init__(self, message_id, message_type, transmission_type, session_id, aircraft_id,
                 hex_id, flight_id, call_sign_nm, altitude_value, ground_speed_value, track_value,
                 latitude_value, longitude_value, vertical_rate, squawk_value, alert_flg, emergency_flg,
                 spi_flg, is_on_ground_flg, generation_dttm, received_dttm, creation_dttm):
        self.message_id = message_id
        self.message_type = message_type
        self.transmission_type = transmission_type
        self.session_id = session_id
        self.aircraft_id = aircraft_id
        self.hex_id = hex_id
        self.flight_id = flight_id
        self.call_sign_nm = call_sign_nm
        self.altitude_value = altitude_value
        self.ground_speed_value = ground_speed_value
        self.track_value = track_value
        self.latitude_value = latitude_value
        self.longitude_value = longitude_value
        self.vertical_rate = vertical_rate
        self.squawk_value = squawk_value
        self.alert_flg = alert_flg
        self.emergency_flg = emergency_flg
        self.spi_flg = spi_flg
        self.is_on_ground_flg = is_on_ground_flg
        self.generation_dttm = generation_dttm
        self.received_dttm = received_dttm
        self.creation_dttm = creation_dttm
