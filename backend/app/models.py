from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class ReservationStatus(enum.Enum):
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    PENDING = "Pending"

class Restaurant(Base):
    __tablename__ = "restaurants"
    restaurant_id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_name = Column(String(100), nullable=False)
    restaurant_description = Column(String(1000), nullable=True)
    total_tables = Column(Integer, default=0)
    booked_tables = Column(Integer, default=0)  # This will be used for quick reference but not for actual availability checks

    reservations = relationship("Reservation", back_populates="restaurant")

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)  # Will store hashed password
    
    reservations = relationship("Reservation", back_populates="user")

class Reservation(Base):
    __tablename__ = "reservations"
    reservation_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.restaurant_id'), nullable=False)
    reservation_date = Column(Date, nullable=False)
    reservation_time = Column(Time, nullable=False)
    number_of_guests = Column(Integer, nullable=False)
    special_requests = Column(String(255), nullable=True)
    status = Column(Enum(ReservationStatus, name='reservation_status'), nullable=False)
    
    user = relationship("User", back_populates="reservations")
    restaurant = relationship("Restaurant", back_populates="reservations")