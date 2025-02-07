from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List, Set
from datetime import date, time
from .auth import add_auth_routes, get_auth

from . import schemas, crud
from .dependencies import get_db
from .init_db import init_database

app = FastAPI(
    title="FoodieSpot API",
    description="API for restaurant management system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_database()

add_auth_routes(app)

# Restaurant endpoints
@app.post("/restaurants/", response_model=schemas.Restaurant, tags=["Restaurants"])
async def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db),auth: str = Depends(get_auth)):
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
async def list_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),auth: str = Depends(get_auth)):
    """
    Retrieve a list of all restaurants with pagination support.
    """
    try:
        restaurants = crud.get_restaurants(db, skip=skip, limit=limit)
        print(f"Found {len(restaurants)} restaurants")  # Debug log
        if not restaurants:
            # Return 404 if no restaurants are found
            raise HTTPException(
                status_code=404,
                detail="No restaurants found in the database"
            )
        return restaurants
    except Exception as e:
        print(f"Error fetching restaurants: {str(e)}")  # Debug log
        raise HTTPException(
            status_code=500,
            detail="Internal server error while fetching restaurants"
        )

@app.get("/restaurants/{restaurant_id}", response_model=schemas.RestaurantWithTables, tags=["Restaurants"])
async def get_restaurant_detail(restaurant_id: int, db: Session = Depends(get_db),auth: str = Depends(get_auth)):
    """
    Get detailed information about a specific restaurant, including its tables.
    """
    restaurant = crud.get_restaurant_with_tables(db, restaurant_id=restaurant_id)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@app.get("/restaurants/search/", response_model=List[schemas.Restaurant], tags=["Restaurants"])
async def search_restaurants(
    cuisine_type: Optional[schemas.CuisineType] = None,
    price_range: Optional[schemas.PriceRange] = None,
    ambiance: Optional[schemas.Ambiance] = None,
    min_seating: Optional[int] = None,
    special_event_space: Optional[bool] = None,
    dietary_options: Optional[str] = None,
    area: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    auth: str = Depends(get_auth)
):
    """
    Search restaurants with multiple filters:
    - cuisine_type: Type of cuisine (e.g., North Indian, Chinese)
    - price_range: Price category ($, $$, $$$, $$$$)
    - ambiance: Restaurant atmosphere
    - min_seating: Minimum seating capacity required
    - special_event_space: Whether special events can be hosted
    - dietary_options: Specific dietary requirements
    - area: Location/area of the restaurant
    """
    return crud.search_restaurants(
        db=db,
        cuisine_type=cuisine_type,
        price_range=price_range,
        ambiance=ambiance,
        min_seating=min_seating,
        special_event_space=special_event_space,
        dietary_options=dietary_options,
        area=area,
        skip=skip,
        limit=limit
    )

@app.get("/restaurants/available/", response_model=List[schemas.Restaurant], tags=["Restaurants"])
async def get_available_restaurants(
    reservation_date: date,
    reservation_time: time,
    party_size: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    auth: str = Depends(get_auth)
):
    """
    Get restaurants that have available tables for the specified date, time and party size.
    """
    return crud.get_available_restaurants(
        db=db,
        reservation_date=reservation_date,
        reservation_time=reservation_time,
        party_size=party_size,
        skip=skip,
        limit=limit
    )

@app.get("/restaurants/recommendations/", response_model=List[schemas.Restaurant], tags=["Restaurants"])
async def get_restaurant_recommendations(
    cuisine_preferences: Optional[Set[schemas.CuisineType]] = Query(None),
    price_range: Optional[schemas.PriceRange] = None,
    party_size: Optional[int] = None,
    area: Optional[str] = None,
    special_occasion: bool = False,
    limit: int = 5,
    db: Session = Depends(get_db),
    auth: str = Depends(get_auth)
):
    """
    Get personalized restaurant recommendations based on:
    - cuisine_preferences: List of preferred cuisine types
    - price_range: Preferred price category
    - party_size: Number of people
    - area: Preferred location/area
    - special_occasion: Whether it's a special occasion
    - limit: Number of recommendations to return
    """
    return crud.get_restaurant_recommendations(
        db=db,
        cuisine_preferences=list(cuisine_preferences) if cuisine_preferences else None,
        price_range=price_range,
        party_size=party_size,
        area=area,
        special_occasion=special_occasion,
        limit=limit
    )

# Table endpoints
@app.post("/tables/", response_model=schemas.Table, tags=["Tables"])
async def create_table(table: schemas.TableCreate, db: Session = Depends(get_db),auth: str = Depends(get_auth)):
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
async def get_restaurant_tables(restaurant_id: int, db: Session = Depends(get_db),auth: str = Depends(get_auth)):
    """
    Get all tables for a specific restaurant.
    """
    return crud.get_restaurant_tables(db, restaurant_id=restaurant_id)

@app.put("/tables/{table_id}/status/", response_model=schemas.Table, tags=["Tables"])
async def update_table_status(table_id: int, status: schemas.TableStatus, db: Session = Depends(get_db),auth: str = Depends(get_auth)):
    """
    Update the status of a specific table (Available, Reserved, or Maintenance).
    """
    table = crud.update_table_status(db, table_id=table_id, status=status)
    if table is None:
        raise HTTPException(status_code=404, detail="Table not found")
    return table

# Customer endpoints
@app.post("/customers/", response_model=schemas.Customer, tags=["Customers"])
async def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db),auth: str = Depends(get_auth)):
    """
    Register a new customer with the following information:
    - name: Customer's full name
    - phone: Contact number
    - email: Email address (optional)
    """
    return crud.create_customer(db=db, customer=customer)

@app.get("/customers/{customer_id}", response_model=schemas.Customer, tags=["Customers"])
async def get_customer(customer_id: int, db: Session = Depends(get_db),auth:str = Depends(get_auth)):
    """
    Retrieve customer information by ID.
    """
    customer = crud.get_customer(db, customer_id=customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.get("/customers/phone/{phone}", response_model=schemas.Customer, tags=["Customers"])
async def get_customer_by_phone(phone: str, db: Session = Depends(get_db),auth:str = Depends(get_auth)):
    """
    Retrieve customer information by phone number.
    """
    customer = crud.get_customer_by_phone(db, phone=phone)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.get("/customers/email/{email}", response_model=schemas.Customer, tags=["Customers"])
async def get_customer_by_email(email: str, db: Session = Depends(get_db),auth:str = Depends(get_auth)):
    """
    Retrieve customer information by email address.
    """
    customer = crud.get_customer_by_email(db, email=email)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.get("/customers/", response_model=List[schemas.Customer], tags=["Customers"])
async def list_customers(db: Session = Depends(get_db),auth:str = Depends(get_auth)):
    """
    Retrieve a list of all customers with pagination support.
    """
    return crud.get_customers(db)


# Reservation endpoints
@app.post("/reservations/", response_model=schemas.Reservation, tags=["Reservations"])
async def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db),auth: str = Depends(get_auth)):
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
    
@app.get('/reservations/', response_model=List[schemas.Reservation], tags=["Reservations"])
async def get_reservations(db: Session = Depends(get_db),auth: str = Depends(get_auth)):
    """
    Retrieve a list of all reservations with pagination support.
    """
    return crud.get_reservations(db)

@app.get("/reservations/{reservation_id}", response_model=schemas.ReservationResponse, tags=["Reservations"])
async def get_reservation(reservation_id: int, db: Session = Depends(get_db),auth: str = Depends(get_auth)):
    """
    Get detailed information about a specific reservation.
    """
    reservation = crud.get_reservation(db, reservation_id=reservation_id)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@app.get("/customers/{customer_id}/reservations/", response_model=List[schemas.Reservation], tags=["Reservations"])
async def get_customer_reservations(customer_id: int, db: Session = Depends(get_db),auth: str = Depends(get_auth)):
    """
    Get all reservations for a specific customer.
    """
    return crud.get_customer_reservations(db, customer_id=customer_id)

@app.get("/restaurants/{restaurant_id}/reservations/", response_model=List[schemas.Reservation], tags=["Reservations"])
async def get_restaurant_reservations(
    restaurant_id: int, 
    date: Optional[date] = None, 
    db: Session = Depends(get_db),
    auth: str = Depends(get_auth)
):
    """
    Get all reservations for a specific restaurant, optionally filtered by date.
    """
    return crud.get_restaurant_reservations(db, restaurant_id=restaurant_id, date=date)

@app.put("/reservations/{reservation_id}/status/", response_model=schemas.Reservation, tags=["Reservations"])
async def update_reservation_status(
    reservation_id: int, 
    status: schemas.ReservationStatus, 
    db: Session = Depends(get_db),
    auth: str = Depends(get_auth)
):
    """
    Update the status of a reservation (Confirmed, Cancelled, or Pending).
    """
    reservation = crud.update_reservation_status(db, reservation_id=reservation_id, status=status)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation



# Support ticket endpoints

@app.post("/support/", response_model=schemas.SupportTicket, tags=["Support"])
async def create_support_ticket(ticket: schemas.SupportTicketCreate, db: Session = Depends(get_db),auth: str = Depends(get_auth)):
    """
    Create a new support ticket with the following details:
    - customer_id: ID of the customer
    - ticket_date: Date of the ticket
    - ticket_time: Time of the ticket
    - ticket_description: Description of the issue
    - status: Ticket status (Open, Closed) (False = Open, True = Closed)
    """
    return crud.create_support_ticket(db=db, ticket=ticket)

@app.get("/support/{ticket_id}", response_model=schemas.SupportTicket, tags=["Support"])
async def get_support_ticket(ticket_id: int, db: Session = Depends(get_db),auth: str = Depends(get_auth)):
    """
    Get detailed information about a specific support ticket.
    """
    ticket = crud.get_support_ticket(db, ticket_id=ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Support ticket not found")
    return ticket

@app.get("/customers/{customer_id}/support/", response_model=List[schemas.SupportTicket], tags=["Support"])
async def get_customer_support_tickets(customer_id: int, db: Session = Depends(get_db),auth: str = Depends(get_auth)):
    """
    Get all support tickets for a specific customer.
    """
    return crud.get_customer_support_tickets(db, customer_id=customer_id)

@app.put("/support/{ticket_id}/close/", response_model=schemas.SupportTicket, tags=["Support"])
async def close_support_ticket(ticket_id: int, db: Session = Depends(get_db),auth: str = Depends(get_auth)):
    """
    Close a specific support ticket.
    """
    ticket = crud.close_support_ticket(db, ticket_id=ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Support ticket not found")
    return ticket

@app.get("/support/", response_model=List[schemas.SupportTicket], tags=["Support"])
async def get_all_support_tickets(db: Session = Depends(get_db),auth: str = Depends(get_auth)):
    """
    Get a list of all support tickets.
    """
    return crud.get_all_support_tickets(db)
