from sqlalchemy import Column, Integer, String, DECIMAL, Time, Date, Boolean, Enum, ForeignKey, ARRAY
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

class CuisineType(enum.Enum):
    NORTH_INDIAN = "North Indian"
    SOUTH_INDIAN = "South Indian"
    CHINESE = "Chinese"
    ITALIAN = "Italian"
    CONTINENTAL = "Continental"
    MUGHLAI = "Mughlai"
    THAI = "Thai"
    JAPANESE = "Japanese"
    MEXICAN = "Mexican"
    MEDITERRANEAN = "Mediterranean"
    BENGALI = "Bengali"
    GUJARATI = "Gujarati"
    PUNJABI = "Punjabi"
    KERALA = "Kerala"
    HYDERABADI = "Hyderabadi"
    KOREAN = "Korean"
    VIETNAMESE = "Vietnamese"
    RAJASTHANI = "Rajasthani"
    GRILL = "Grill"

class PriceRange(enum.Enum):
    BUDGET = "$"
    MODERATE = "$$"
    PREMIUM = "$$$"
    LUXURY = "$$$$"

class Ambiance(enum.Enum):
    CASUAL = "Casual"
    FINE_DINING = "Fine Dining"
    FAMILY = "Family"
    CAFE = "Cafe"
    BISTRO = "Bistro"
    LOUNGE = "Lounge"
    OUTDOOR = "Outdoor"

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
    cuisine_type = Column(Enum(CuisineType, name='cuisine_type'), nullable=False)
    price_range = Column(Enum(PriceRange, name='price_range'), nullable=False)
    ambiance = Column(Enum(Ambiance, name='ambiance'), nullable=False)
    average_rating = Column(DECIMAL(3,2), default=0.0)
    features = Column(String(500), nullable=True)  
    description = Column(String(1000), nullable=True)
    specialties = Column(String(500), nullable=True)
    dietary_options = Column(String(255), nullable=True)  
    
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

class SupportTicket(Base):
    __tablename__ = "support_tickets"
    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    ticket_date = Column(Date, nullable=False)
    ticket_time = Column(Time, nullable=False)
    ticket_description = Column(String(255), nullable=False)

    # False = Open, True = Closed
    status = Column(Boolean, nullable=False,default=False)

    customer = relationship("Customer")

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