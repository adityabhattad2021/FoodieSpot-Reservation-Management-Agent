from pydantic import BaseModel, EmailStr
from datetime import datetime, time, date
from typing import Optional, List
from .models import TableStatus, ReservationStatus, CuisineType, PriceRange, Ambiance

class RestaurantBase(BaseModel):
    name: str
    address: str
    phone: str
    email: EmailStr
    opening_time: time
    closing_time: time
    seating_capacity: int
    special_event_space: bool = False
    cuisine_type: CuisineType
    price_range: PriceRange
    ambiance: Ambiance
    features: Optional[str] = None
    description: Optional[str] = None
    specialties: Optional[str] = None
    dietary_options: Optional[str] = None
    average_rating: Optional[float] = 0.0

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

class SupportTicketBase(BaseModel):
    customer_id: int
    ticket_date: date
    ticket_time: time
    ticket_description: str
    status: bool

class SupportTicketCreate(SupportTicketBase):
    pass

class SupportTicket(SupportTicketBase):
    ticket_id: int

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

class SimpleReservationCreate(BaseModel):
    """
    Schema for creating a reservation with minimal information
    """
    restaurant_name: str
    date: str  # Format: YYYY-MM-DD
    time: str  # Format: HH:MM
    party_size: int
    user_id: str = "1"
    special_requests: Optional[str] = None
    has_user_confirmed: bool = True  # Assuming user confirmed if they submit

    class Config:
        from_attributes = True

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

class ReservationResponseSimple(BaseModel):
    """
    Schema for reservation response
    """
    reservation_id: int
    restaurant_name: str
    date: str
    time: str
    party_size: int
    message: str

    class Config:
        from_attributes = True