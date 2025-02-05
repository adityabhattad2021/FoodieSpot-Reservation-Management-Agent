from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date, time
from . import models, schemas
from typing import List, Optional

# Restaurant CRUD operations
def create_restaurant(db: Session, restaurant: schemas.RestaurantCreate):
    db_restaurant = models.Restaurant(**restaurant.model_dump())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

def get_restaurant(db: Session, restaurant_id: int):
    return db.query(models.Restaurant).filter(models.Restaurant.restaurant_id == restaurant_id).first()

def get_restaurants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Restaurant).offset(skip).limit(limit).all()

def get_restaurant_with_tables(db: Session, restaurant_id: int):
    return db.query(models.Restaurant).filter(models.Restaurant.restaurant_id == restaurant_id).first()

# Table CRUD operations
def create_table(db: Session, table: schemas.TableCreate):
    db_table = models.Table(**table.model_dump())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

def get_table(db: Session, table_id: int):
    return db.query(models.Table).filter(models.Table.table_id == table_id).first()

def get_restaurant_tables(db: Session, restaurant_id: int):
    return db.query(models.Table).filter(models.Table.restaurant_id == restaurant_id).all()

def update_table_status(db: Session, table_id: int, status: schemas.TableStatus):
    db_table = db.query(models.Table).filter(models.Table.table_id == table_id).first()
    if db_table:
        db_table.status = status
        db.commit()
        db.refresh(db_table)
    return db_table

# Customer CRUD operations
def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()

def get_customer_by_email(db: Session, email: str):
    return db.query(models.Customer).filter(models.Customer.email == email).first()

def get_customer_by_phone(db: Session, phone: str):
    return db.query(models.Customer).filter(models.Customer.phone == phone).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()


# Reservation CRUD operations
def create_reservation(db: Session, reservation: schemas.ReservationCreate):
    # First check if table is available
    existing_reservations = check_table_availability(
        db,
        reservation.table_id,
        reservation.reservation_date,
        reservation.reservation_time
    )
    
    if existing_reservations:
        raise ValueError("Table is already reserved for this time slot")
    
    db_reservation = models.Reservation(**reservation.model_dump())
    db.add(db_reservation)
    
    # Update table status to Reserved
    update_table_status(db, reservation.table_id, schemas.TableStatus.RESERVED)
    
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def get_reservation(db: Session, reservation_id: int):
    return db.query(models.Reservation).filter(
        models.Reservation.reservation_id == reservation_id
    ).first()

def get_customer_reservations(db: Session, customer_id: int):
    return db.query(models.Reservation).filter(
        models.Reservation.customer_id == customer_id
    ).all()

def get_restaurant_reservations(db: Session, restaurant_id: int, date: Optional[date] = None):
    query = db.query(models.Reservation).filter(models.Reservation.restaurant_id == restaurant_id)
    if date:
        query = query.filter(models.Reservation.reservation_date == date)
    return query.all()

def update_reservation_status(db: Session, reservation_id: int, status: schemas.ReservationStatus):
    db_reservation = db.query(models.Reservation).filter(
        models.Reservation.reservation_id == reservation_id
    ).first()
    if db_reservation:
        db_reservation.status = status
        if status == schemas.ReservationStatus.CANCELLED:
            # Make table available again if reservation is cancelled
            update_table_status(db, db_reservation.table_id, schemas.TableStatus.AVAILABLE)
        db.commit()
        db.refresh(db_reservation)
    return db_reservation

def check_table_availability(db: Session, table_id: int, date: date, time: time):
    return db.query(models.Reservation).filter(
        and_(
            models.Reservation.table_id == table_id,
            models.Reservation.reservation_date == date,
            models.Reservation.reservation_time == time,
            models.Reservation.status != schemas.ReservationStatus.CANCELLED
        )
    ).first()

def cancel_reservation(db: Session, reservation_id: int):
    return update_reservation_status(db, reservation_id, schemas.ReservationStatus.CANCELLED)