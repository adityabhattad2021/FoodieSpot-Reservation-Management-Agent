from datetime import time, date, timedelta
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Restaurant, Table, Customer, Reservation
import random

def seed_data():
    db = SessionLocal()
    try:
        # Seed Restaurants
        restaurants = [
            Restaurant(
                name=name,
                address=f"{random.randint(100, 999)} {street} Road, {area}",
                phone=f"555-{random.randint(1000, 9999)}",
                email=f"info@{name.lower().replace(' ', '')}.com",
                opening_time=time(11, 0),  # 11:00 AM
                closing_time=time(23, 0),  # 11:00 PM
                seating_capacity=random.randint(50, 200),
                special_event_space=random.choice([True, False])
            )
            for name, street, area in [
                ("Taj Mahal", "MG", "Indiranagar"),
                ("Punjab Grill", "Brigade", "Koramangala"),
                ("Dakshin Flavors", "Commercial", "JP Nagar"),
                ("Spice Garden", "Church", "Whitefield"),
                ("Royal Biryani", "Richmond", "HSR Layout"),
                ("Curry Leaf", "Victoria", "Malleshwaram"),
                ("Mumbai Masala", "Infantry", "Jayanagar"),
                ("Chennai Express", "Residency", "BTM Layout"),
                ("Delhi Darbar", "Palace", "Electronic City"),
                ("Tandoor Tales", "CMH", "Bellandur"),
                ("Hyderabad House", "Airport", "Marathahalli"),
                ("Kerala Kitchen", "Outer Ring", "Sarjapur"),
                ("Rajasthani Rasoi", "Inner Ring", "Hebbal"),
                ("Bengal Bay", "Old Madras", "RT Nagar"),
                ("Andhra Bhavan", "Hosur", "Silk Board"),
                ("Goan Paradise", "Double", "Yelahanka"),
                ("Lucknow Legacy", "Bannerghatta", "JP Nagar"),
                ("Chettinad Corner", "Old Airport", "Domlur"),
                ("Gujarati Ghee", "Cunningham", "Vasanth Nagar"),
                ("Kashmiri Kitchen", "St Johns", "Cox Town"),
                ("Awadhi Avenue", "Cambridge", "Fraser Town"),
                ("Mangalorean Magic", "Miller", "Richards Town"),
                ("Kolkata Kitchen", "Dickenson", "Shivaji Nagar"),
                ("Bombay Bistro", "Infantry", "Commercial Street"),
                ("Madras Meals", "Lavelle", "MG Road")
            ]
        ]

        # Add restaurants to session
        for restaurant in restaurants:
            db.add(restaurant)
        db.commit()

        # Seed Tables for each restaurant
        tables = []
        table_types = ['Regular', 'Booth', 'Private']
        status_options = ['Available', 'Reserved', 'Maintenance']

        for restaurant in restaurants:
            # Create 8-12 tables per restaurant
            for i in range(random.randint(8, 12)):
                table = Table(
                    restaurant_id=restaurant.restaurant_id,
                    table_number=i + 1,
                    seating_capacity=random.choice([2, 2, 4, 4, 4, 6, 6, 8, 8, 10]),
                    table_type=random.choice(table_types),
                    status='Available'
                )
                tables.append(table)
        
        for table in tables:
            db.add(table)
        db.commit()

        # Seed Customers
        indian_first_names = ['Aarav', 'Arjun', 'Advait', 'Kabir', 'Reyansh', 
                            'Vihaan', 'Aanya', 'Aadhya', 'Ishaan', 'Veer',
                            'Riya', 'Zara', 'Anaya', 'Aisha', 'Prisha']
        indian_last_names = ['Patel', 'Sharma', 'Kumar', 'Singh', 'Shah',
                           'Verma', 'Rao', 'Reddy', 'Malhotra', 'Kapoor']

        customers = []
        for _ in range(50):  # Create 50 customers
            customer = Customer(
                name=f"{random.choice(indian_first_names)} {random.choice(indian_last_names)}",
                phone=f"555-{random.randint(1000, 9999)}",
                email=f"customer{_}@example.com"
            )
            customers.append(customer)

        for customer in customers:
            db.add(customer)
        db.commit()

        # Seed Reservations
        today = date.today()
        status_options = ['Confirmed', 'Cancelled', 'Pending']

        for _ in range(100):  # Create 100 reservations
            reservation_date = today + timedelta(days=random.randint(0, 30))
            reservation_time = time(random.randint(11, 22), random.choice([0, 30]))
            
            random_customer = random.choice(customers)
            random_restaurant = random.choice(restaurants)
            random_table = random.choice([t for t in tables if t.restaurant_id == random_restaurant.restaurant_id])

            reservation = Reservation(
                customer_id=random_customer.customer_id,
                restaurant_id=random_restaurant.restaurant_id,
                table_id=random_table.table_id,
                reservation_date=reservation_date,
                reservation_time=reservation_time,
                number_of_guests=random.randint(1, random_table.seating_capacity),
                special_requests=random.choice([None, "Window seat", "Birthday celebration", "Anniversary", "Business meeting"]),
                status=random.choice(status_options)
            )
            db.add(reservation)
        
        db.commit()

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()