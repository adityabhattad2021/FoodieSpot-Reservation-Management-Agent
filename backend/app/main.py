from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date, time

from . import models, schemas, crud
from .database import SessionLocal, engine
from .dependencies import get_db

app = FastAPI(title="FoodieSpot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Restaurant endpoints
@app.post("/restaurants/", response_model=schemas.Restaurant, tags=["Restaurants"])
async def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    """
    Create a new restaurant with the following information:
    - name: Restaurant name
    - address: Physical location
    - phone: Contact number
    - email: Contact email
    - opening_time: Daily opening time
    - closing_time: Daily closing time
    - seating_capacity: Total capacity
    - special_event_space: Whether special events can be hosted
    """
    return crud.create_restaurant(db=db, restaurant=restaurant)

@app.get("/restaurants/", response_model=List[schemas.Restaurant], tags=["Restaurants"])
async def list_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of all restaurants with pagination support.
    """
    return crud.get_restaurants(db, skip=skip, limit=limit)

@app.get("/restaurants/{restaurant_id}", response_model=schemas.RestaurantWithTables, tags=["Restaurants"])
async def get_restaurant_detail(restaurant_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific restaurant, including its tables.
    """
    restaurant = crud.get_restaurant_with_tables(db, restaurant_id=restaurant_id)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

# Table endpoints
@app.post("/tables/", response_model=schemas.Table, tags=["Tables"])
async def create_table(table: schemas.TableCreate, db: Session = Depends(get_db)):
    """
    Create a new table in a restaurant with the following details:
    - restaurant_id: ID of the restaurant
    - table_number: Unique number within the restaurant
    - seating_capacity: Number of seats at the table
    - table_type: Type of table (Regular, Booth, Private)
    - status: Current status (Available, Reserved, Maintenance)
    """
    return crud.create_table(db=db, table=table)

@app.get("/restaurants/{restaurant_id}/tables/", response_model=List[schemas.Table], tags=["Tables"])
async def get_restaurant_tables(restaurant_id: int, db: Session = Depends(get_db)):
    """
    Get all tables for a specific restaurant.
    """
    return crud.get_restaurant_tables(db, restaurant_id=restaurant_id)

@app.put("/tables/{table_id}/status/", response_model=schemas.Table, tags=["Tables"])
async def update_table_status(table_id: int, status: schemas.TableStatus, db: Session = Depends(get_db)):
    """
    Update the status of a specific table (Available, Reserved, or Maintenance).
    """
    table = crud.update_table_status(db, table_id=table_id, status=status)
    if table is None:
        raise HTTPException(status_code=404, detail="Table not found")
    return table

# Customer endpoints
@app.post("/customers/", response_model=schemas.Customer, tags=["Customers"])
async def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """
    Register a new customer with the following information:
    - name: Customer's full name
    - phone: Contact number
    - email: Email address (optional)
    """
    return crud.create_customer(db=db, customer=customer)

@app.get("/customers/{customer_id}", response_model=schemas.Customer, tags=["Customers"])
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Retrieve customer information by ID.
    """
    customer = crud.get_customer(db, customer_id=customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.get("/customers/phone/{phone}", response_model=schemas.Customer, tags=["Customers"])
async def get_customer_by_phone(phone: str, db: Session = Depends(get_db)):
    """
    Retrieve customer information by phone number.
    """
    customer = crud.get_customer_by_phone(db, phone=phone)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.get("/customers/email/{email}", response_model=schemas.Customer, tags=["Customers"])
async def get_customer_by_email(email: str, db: Session = Depends(get_db)):
    """
    Retrieve customer information by email address.
    """
    customer = crud.get_customer_by_email(db, email=email)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.get("/customers/", response_model=List[schemas.Customer], tags=["Customers"])
async def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of all customers with pagination support.
    """
    return crud.get_customers(db, skip=skip, limit=limit)



# Reservation endpoints
@app.post("/reservations/", response_model=schemas.Reservation, tags=["Reservations"])
async def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    """
    Create a new reservation with the following details:
    - customer_id: ID of the customer making the reservation
    - restaurant_id: ID of the restaurant
    - table_id: ID of the table to reserve
    - reservation_date: Date of the reservation
    - reservation_time: Time of the reservation
    - number_of_guests: Number of people
    - special_requests: Any special requirements (optional)
    - status: Status of the reservation (Confirmed, Cancelled, Pending)
    """
    try:
        return crud.create_reservation(db=db, reservation=reservation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/reservations/{reservation_id}", response_model=schemas.ReservationResponse, tags=["Reservations"])
async def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific reservation.
    """
    reservation = crud.get_reservation(db, reservation_id=reservation_id)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@app.get("/customers/{customer_id}/reservations/", response_model=List[schemas.Reservation], tags=["Reservations"])
async def get_customer_reservations(customer_id: int, db: Session = Depends(get_db)):
    """
    Get all reservations for a specific customer.
    """
    return crud.get_customer_reservations(db, customer_id=customer_id)

@app.get("/restaurants/{restaurant_id}/reservations/", response_model=List[schemas.Reservation], tags=["Reservations"])
async def get_restaurant_reservations(
    restaurant_id: int, 
    date: Optional[date] = None, 
    db: Session = Depends(get_db)
):
    """
    Get all reservations for a specific restaurant, optionally filtered by date.
    """
    return crud.get_restaurant_reservations(db, restaurant_id=restaurant_id, date=date)

@app.put("/reservations/{reservation_id}/status/", response_model=schemas.Reservation, tags=["Reservations"])
async def update_reservation_status(
    reservation_id: int, 
    status: schemas.ReservationStatus, 
    db: Session = Depends(get_db)
):
    """
    Update the status of a reservation (Confirmed, Cancelled, or Pending).
    """
    reservation = crud.update_reservation_status(db, reservation_id=reservation_id, status=status)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@app.post("/reservations/{reservation_id}/cancel/", response_model=schemas.Reservation, tags=["Reservations"])
async def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    """
    Cancel a specific reservation.
    """
    reservation = crud.cancel_reservation(db, reservation_id=reservation_id)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

