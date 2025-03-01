from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import date, time, datetime, timedelta
from . import models, schemas
from typing import Optional
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Restaurant CRUD operations
def create_restaurant(db: Session, restaurant: schemas.RestaurantCreate):
    db_restaurant = models.Restaurant(**restaurant.model_dump())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

def get_restaurant(db: Session, restaurant_id: int):
    return db.query(models.Restaurant).filter(models.Restaurant.restaurant_id == restaurant_id).first()

def get_restaurant_by_name(db: Session, restaurant_name: str):
    return db.query(models.Restaurant).filter(models.Restaurant.restaurant_name.ilike(f"%{restaurant_name}%")).first()

def get_restaurants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Restaurant).offset(skip).limit(limit).all()

def update_restaurant(db: Session, restaurant_id: int, restaurant: schemas.RestaurantCreate):
    db_restaurant = get_restaurant(db, restaurant_id)
    if db_restaurant:
        for key, value in restaurant.model_dump().items():
            setattr(db_restaurant, key, value)
        db.commit()
        db.refresh(db_restaurant)
    return db_restaurant

def delete_restaurant(db: Session, restaurant_id: int):
    db_restaurant = get_restaurant(db, restaurant_id)
    if db_restaurant:
        db.delete(db_restaurant)
        db.commit()
        return True
    return False

def get_available_tables_count(db: Session, restaurant_id: int, reservation_date: date, reservation_time: time):
    """
    Calculate the number of available tables at a specific date and time
    by checking existing reservations.
    """
    # Get the restaurant
    restaurant = get_restaurant(db, restaurant_id)
    if not restaurant:
        return 0
    
    # Define the time window for the reservation (typically 1.5 hours)
    time_obj = datetime.combine(date.today(), reservation_time)
    end_time = (time_obj + timedelta(hours=1, minutes=30)).time()
    
    # Count reservations that overlap with the requested time
    overlapping_reservations = db.query(func.count(models.Reservation.reservation_id)).filter(
        and_(
            models.Reservation.restaurant_id == restaurant_id,
            models.Reservation.reservation_date == reservation_date,
            models.Reservation.status != models.ReservationStatus.CANCELLED,
            or_(
                # Reservation starts during our time window
                and_(
                    models.Reservation.reservation_time >= reservation_time,
                    models.Reservation.reservation_time < end_time
                ),
                # Reservation ends during our time window
                and_(
                    models.Reservation.reservation_time < reservation_time,
                    # Use a simpler approach without time_add
                    # Assuming all reservations are 1.5 hours long
                    # We'll consider any reservation that starts up to 1.5 hours before our time
                    models.Reservation.reservation_time >= (datetime.combine(date.today(), reservation_time) - timedelta(hours=1, minutes=30)).time()
                )
            )
        )
    ).scalar()
    
    # If there was an error with the query, fall back to a simpler approach
    if overlapping_reservations is None:
        # Simplified approach: just count reservations at the exact same time
        overlapping_reservations = db.query(func.count(models.Reservation.reservation_id)).filter(
            and_(
                models.Reservation.restaurant_id == restaurant_id,
                models.Reservation.reservation_date == reservation_date,
                models.Reservation.reservation_time == reservation_time,
                models.Reservation.status != models.ReservationStatus.CANCELLED
            )
        ).scalar() or 0
    
    # Calculate available tables
    available_tables = max(0, restaurant.total_tables - overlapping_reservations)
    return available_tables


def is_table_available(db: Session, restaurant_id: int, reservation_date: date, reservation_time: time):
    """Check if there are any tables available at the given time."""
    return get_available_tables_count(db, restaurant_id, reservation_date, reservation_time) > 0

# User CRUD operations
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        if 'password' in update_data and update_data['password']:
            update_data['password'] = get_password_hash(update_data['password'])
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

# Reservation CRUD operations
def create_reservation(db: Session, reservation: schemas.ReservationCreate, user_id: int):
    # Check if tables are available at the requested time
    if not is_table_available(db, reservation.restaurant_id, reservation.reservation_date, reservation.reservation_time):
        return None
    
    db_reservation = models.Reservation(
        **reservation.model_dump(),
        user_id=user_id,
        status=models.ReservationStatus.CONFIRMED
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def create_reservation_by_restaurant_name(db: Session, reservation: schemas.SimpleReservationCreate, user_id: int):
    # Find restaurant by name
    restaurant = get_restaurant_by_name(db, reservation.restaurant_name)
    if not restaurant:
        return None
    
    # Parse date and time
    try:
        reservation_date = datetime.strptime(reservation.date, "%Y-%m-%d").date()
        reservation_time = datetime.strptime(reservation.time, "%H:%M").time()
    except ValueError:
        return None
    
    # Check if tables are available at the requested time
    if not is_table_available(db, restaurant.restaurant_id, reservation_date, reservation_time):
        return None
    
    # Create reservation
    db_reservation = models.Reservation(
        restaurant_id=restaurant.restaurant_id,
        user_id=user_id,
        reservation_date=reservation_date,
        reservation_time=reservation_time,
        number_of_guests=reservation.guests,
        special_requests=reservation.special_requests,
        status=models.ReservationStatus.CONFIRMED
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation, restaurant

def get_reservation(db: Session, reservation_id: int):
    return db.query(models.Reservation).filter(models.Reservation.reservation_id == reservation_id).first()

def get_user_reservations(db: Session, user_id: int):
    return db.query(models.Reservation).filter(models.Reservation.user_id == user_id).all()

def get_restaurant_reservations(db: Session, restaurant_id: int, reservation_date: Optional[date] = None):
    query = db.query(models.Reservation).filter(models.Reservation.restaurant_id == restaurant_id)
    if reservation_date:
        query = query.filter(models.Reservation.reservation_date == reservation_date)
    return query.all()

def update_reservation(db: Session, reservation_id: int, reservation_update: schemas.ReservationUpdate, user_id: int):
    db_reservation = db.query(models.Reservation).filter(
        and_(
            models.Reservation.reservation_id == reservation_id,
            models.Reservation.user_id == user_id
        )
    ).first()
    
    if db_reservation:
        update_data = reservation_update.model_dump(exclude_unset=True)
        
        # If changing date or time, check availability
        if ('reservation_date' in update_data or 'reservation_time' in update_data):
            new_date = update_data.get('reservation_date', db_reservation.reservation_date)
            new_time = update_data.get('reservation_time', db_reservation.reservation_time)
            
            # Check if the new time slot is available
            if not is_table_available(db, db_reservation.restaurant_id, new_date, new_time):
                return None
        
        for key, value in update_data.items():
            setattr(db_reservation, key, value)
        
        db.commit()
        db.refresh(db_reservation)
    return db_reservation

def cancel_reservation(db: Session, reservation_id: int, user_id: int):
    db_reservation = db.query(models.Reservation).filter(
        and_(
            models.Reservation.reservation_id == reservation_id,
            models.Reservation.user_id == user_id
        )
    ).first()
    
    if db_reservation:
        db_reservation.status = models.ReservationStatus.CANCELLED
        db.commit()
        db.refresh(db_reservation)
    return db_reservation

def get_restaurant_availability(db: Session, restaurant_id: int, date: date):
    """
    Get the availability of a restaurant for all hours in a day.
    Returns a dictionary with hour -> available tables.
    """
    restaurant = get_restaurant(db, restaurant_id)
    if not restaurant:
        return {}
    
    # Create a dictionary for all hours of operation (assuming 9 AM to 10 PM)
    availability = {}
    for hour in range(9, 23):  # 9 AM to 10 PM
        for minute in [0, 30]:  # Every 30 minutes
            time_slot = time(hour, minute)
            available_tables = get_available_tables_count(db, restaurant_id, date, time_slot)
            availability[f"{hour:02d}:{minute:02d}"] = available_tables
    
    return availability