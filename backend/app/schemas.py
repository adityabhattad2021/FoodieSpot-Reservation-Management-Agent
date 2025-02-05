from pydantic import BaseModel, EmailStr
from datetime import datetime, time, date
from typing import Optional, List
from enum import Enum

class TableStatus(str, Enum):
    AVAILABLE = "Available"
    RESERVED = "Reserved"
    MAINTENANCE = "Maintenance"

class ReservationStatus(str, Enum):
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    PENDING = "Pending"

class RestaurantBase(BaseModel):
    name: str
    address: str
    phone: str
    email: EmailStr
    opening_time: time
    closing_time: time
    seating_capacity: int
    special_event_space: bool = False

class RestaurantCreate(RestaurantBase):
    pass
    

class Restaurant(RestaurantBase):
    restaurant_id: int
    
    class Config:
        from_attributes = True

class TableBase(BaseModel):
    restaurant_id: int
    table_number: int
    seating_capacity: int
    table_type: str
    status: TableStatus

class TableCreate(TableBase):
    pass

class Table(TableBase):
    table_id: int

    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    customer_id: int

    class Config:
        from_attributes = True

class ReservationBase(BaseModel):
    customer_id: int
    restaurant_id: int
    table_id: int
    reservation_date: date
    reservation_time: time
    number_of_guests: int
    special_requests: Optional[str] = None
    status: ReservationStatus

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    reservation_id: int
    
    class Config:
        from_attributes = True

class RestaurantWithTables(Restaurant):
    tables: List[Table] = []

class ReservationResponse(Reservation):
    customer: Customer
    table: Table
    restaurant: Restaurant