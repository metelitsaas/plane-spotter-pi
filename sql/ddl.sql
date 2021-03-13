CREATE SEQUENCE message_id_seq;

CREATE TABLE message (
	message_id integer NOT NULL,
	message_type varchar(3) NOT NULL,
    transmission_type integer,
    session_id integer,
    aircraft_id integer,
    hex_id varchar(10),
    flight_id integer,
    call_sign_nm varchar(10),
    altitude_value integer,
    ground_speed_value numeric,
    track_value numeric,
    latitude_value numeric,
    longitude_value numeric,
    vertical_rate_value numeric,
    squawk_value integer,
    alert_flg boolean,
    emergency_flg boolean,
    spi_flg boolean,
    is_on_ground_flg boolean,
    generation_dttm timestamp,
    received_dttm timestamp,
    creation_dttm timestamp,
	CONSTRAINT message_pkey PRIMARY KEY (message_id)
);