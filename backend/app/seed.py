import random
from datetime import time, date, timedelta
from .database import SessionLocal
from .models import Restaurant, User, Reservation, ReservationStatus
from .crud import get_password_hash

def seed_data():
    db = SessionLocal()
    try:
        # Seed Restaurants
        restaurant_data = [
            {
                "name": "Taj Mahal",
                "description": "Authentic North Indian cuisine in a luxurious setting with royal Mughal ambiance",
            },
            {
                "name": "Punjab Grill",
                "description": "Authentic Punjabi cuisine with traditional charm",
            },
            {
                "name": "Dakshin Flavors",
                "description": "Traditional South Indian cuisine served with authentic flavors",
            },
            {
                "name": "Dragon House",
                "description": "Premium Chinese dining experience with modern Asian decor",
            },
            {
                "name": "Bella Italia",
                "description": "Authentic Italian cuisine with imported ingredients",
            }
        ]

        restaurants = []
        for data in restaurant_data:
            restaurant = Restaurant(
                restaurant_name=data["name"],
                restaurant_description=data["description"],
                total_tables=random.randint(10, 20),
                booked_tables=0
            )
            db.add(restaurant)
            restaurants.append(restaurant)
        
        db.commit()
        
        # Create a single user
        user = User(
            name="Aditya Bhattad",
            email="aditya.bhattad@example.com",
            password=get_password_hash("password123") ,
            ai_preferences="I prefer vegetarian options."
        )
        db.add(user)
        db.commit()
        
        print(f"Created user: {user.name} with ID: {user.user_id}")
        
        # Create reservations for the user
        today = date.today()
        
        # Make 5 reservations for different dates and restaurants
        for i in range(5):
            reservation_date = today + timedelta(days=i+1)
            restaurant = random.choice(restaurants)
            
            # Random time between 6 PM and 9 PM
            hour = random.randint(18, 21)
            minute = random.choice([0, 15, 30, 45])
            reservation_time = time(hour, minute)
            
            reservation = Reservation(
                user_id=user.user_id,
                restaurant_id=restaurant.restaurant_id,
                reservation_date=reservation_date,
                reservation_time=reservation_time,
                number_of_guests=random.randint(2, 6),
                status=ReservationStatus.CONFIRMED
            )
            
            db.add(reservation)
            
            # Update booked tables count
            restaurant.booked_tables += 1
            
            print(f"Created reservation at {restaurant.restaurant_name} on {reservation_date} at {reservation_time}")
        
        db.commit()
        print("Seed data created successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
