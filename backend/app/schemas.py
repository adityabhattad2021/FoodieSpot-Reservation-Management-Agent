from pydantic import BaseModel, EmailStr
from datetime import date, time
from typing import Optional, List
from .models import ReservationStatus

# Restaurant schemas
class RestaurantBase(BaseModel):
    restaurant_name: str
    restaurant_description: Optional[str] = None
    total_tables: Optional[int] = 0
    booked_tables: Optional[int] = 0

class RestaurantCreate(RestaurantBase):
    pass

class Restaurant(RestaurantBase):
    restaurant_id: int
    
    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    ai_preferences: Optional[str] = None

class User(UserBase):
    user_id: int
    ai_preferences: Optional[str] = None
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None

# Simplified Reservation schemas
class ReservationBase(BaseModel):
    restaurant_id: int
    reservation_date: date
    reservation_time: time
    number_of_guests: int

class ReservationCreate(ReservationBase):
    user_id: Optional[int] = None

class SimpleReservationCreate(BaseModel):
    user_id: Optional[int] = None
    restaurant_name: str
    date: str  # Format: YYYY-MM-DD
    time: str  # Format: HH:MM
    guests: int

class ReservationUpdate(BaseModel):
    user_id: Optional[int] = None
    reservation_date: Optional[date] = None
    reservation_time: Optional[time] = None
    number_of_guests: Optional[int] = None
    status: Optional[ReservationStatus] = None

class Reservation(ReservationBase):
    reservation_id: int
    user_id: int
    status: ReservationStatus
    reservation_code: str
    
    class Config:
        from_attributes = True

class ReservationWithRestaurant(Reservation):
    restaurant: Restaurant
    
    class Config:
        from_attributes = True

class ReservationResponse(BaseModel):
    reservation_id: int
    restaurant_name: str
    date: str
    time: str
    guests: int
    status: str
    reservation_code: str
    message: str = "Reservation confirmed"
    
    class Config:
        from_attributes = True