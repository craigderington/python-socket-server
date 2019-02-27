from db import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Float
from sqlalchemy.orm import relationship


class RadioType(Base):
    __tablename__ = 'radio_types'

    id = Column(Integer, primary_key=True)
    radio_type_name = Column(String(255), nullable=False)
    radio_type_descr = Column(String(255), nullable=False)

    def __repr__(self):
        if self.id and self.radio_type_name:
            return '{} {}'.format(
                self.id, self.radio_type_name
            )


class Radio(Base):
    __tablename__ = 'radios'

    id = Column(Integer, primary_key=True)
    radio_type = Column(Integer, ForeignKey('radio_types.id'), nullable=False)
    serial_number = Column(String(255), nullable=False)
    imei = Column(String(24), nullable=False)

    def __repr__(self):
        if self.id and self.radio_type:
            return '{} {} {}'.format(
                self.id, self.radio_type, self.imei
            )


class Tx(Base):
    __tablename__ = 'radio_txs'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, onupdate=datetime.now)
    raw_data = Column(String(1024), nullable=False)

    def __repr__(self):
        if self.id and self.timestamp:
            return '{} {} {}'.format(
                self.id, self.timestamp, self.raw_data
            )


class TxHeader(Base):
    __tablename__ = 'radio_tx_headers'

    id = Column(Integer, primary_key=True)
    tx_id = Column(Integer, ForeignKey('radio_txs.id'), nullable=False)
    tx = relationship('Tx')
    timestamp = Column(DateTime, nullable=False, onupdate=datetime.now)
    product_type = Column(Integer, nullable=False)
    hardware_rev = Column(Float, nullable=False)
    firmware_rev = Column(String(10), nullable=False)
    contact_reason = Column(String(8), nullable=False)
    alarm_status = Column(String(8), nullable=False)
    gsm_rssi = Column(Integer, nullable=False)
    battery_status = Column(String(10), nullable=False)
    imei = Column(String(16), nullable=False)
    message_type = Column(Integer, nullable=False)
    payload_len = Column(Integer, nullable=False)

    def __repr__(self):
        if self.id:
            return '{} {} {}'.format(
                self.id, self.imei, self.message_type
            )


class TxReading(Base):
    __tablename__ = 'radio_tx_readings'

    id = Column(Integer, primary_key=True)
    tx_id = Column(Integer, ForeignKey('radio_txs.id'), nullable=False)
    tx_header_id = Column(Integer, ForeignKey('radio_tx_headers.id'), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    distance = Column(Float, nullable=False, default=0.00)
    src = Column(String(255), nullable=False)
    rssi = Column(Integer, nullable=False)
    temperature = Column(Float, nullable=False)

    def __repr__(self):
        if self.id:
            return '{} {} on {}'.format(
                self.tx_id, self.distance, self.timestamp
            )
