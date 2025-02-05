from sqlalchemy import Column, Integer, String, DECIMAL, Time, Date, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import enum

class TableStatus(enum.Enum):
    AVAILABLE = "Available"
    RESERVED = "Reserved"
    MAINTENANCE = "Maintenance"

class ReservationStatus(enum.Enum):
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    PENDING = "Pending"

class Restaurant(Base):
    __tablename__ = "restaurants"
    restaurant_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=False)
    email = Column(String(100), nullable=False)
    opening_time = Column(Time, nullable=False)
    closing_time = Column(Time, nullable=False)
    seating_capacity = Column(Integer, nullable=False)
    special_event_space = Column(Boolean, default=False)
    tables = relationship("Table", back_populates="restaurant")

class Table(Base):
    __tablename__ = "tables"
    table_id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.restaurant_id'), nullable=False)
    table_number = Column(Integer, nullable=False)
    seating_capacity = Column(Integer, nullable=False)
    table_type = Column(String(50), nullable=False)
    status = Column(Enum(TableStatus, name='table_status'), nullable=False)

    restaurant = relationship("Restaurant", back_populates="tables")

class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    email = Column(String(100), nullable=True)

class Reservation(Base):
    __tablename__ = "reservations"
    reservation_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.restaurant_id'), nullable=False)
    table_id = Column(Integer, ForeignKey('tables.table_id'), nullable=False)
    reservation_date = Column(Date, nullable=False)
    reservation_time = Column(Time, nullable=False)
    number_of_guests = Column(Integer, nullable=False)
    special_requests = Column(String(255))
    status = Column(Enum(ReservationStatus, name='reservation_status'), nullable=False)

    customer = relationship("Customer")
    restaurant = relationship("Restaurant")
    table = relationship("Table")