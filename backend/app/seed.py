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
                "description": "Authentic North Indian cuisine in a luxurious setting with royal Mughal ambiance"
            },
            {
                "name": "Punjab Grill",
                "description": "Authentic Punjabi cuisine with traditional charm"
            },
            {
                "name": "Dakshin Flavors",
                "description": "Traditional South Indian cuisine served with authentic flavors"
            },
            {
                "name": "Dragon House",
                "description": "Premium Chinese dining experience with modern Asian decor"
            },
            {
                "name": "Bella Italia",
                "description": "Authentic Italian cuisine with imported ingredients"
            },
            {
                "name": "Kerala Kitchen",
                "description": "Authentic Kerala cuisine with coastal flavors"
            },
            {
                "name": "Hyderabad House",
                "description": "Famous for authentic Hyderabadi cuisine"
            },
            {
                "name": "Bengal Bay",
                "description": "Traditional Bengali cuisine with home-style cooking"
            },
            {
                "name": "Gujarati Thali",
                "description": "Unlimited Gujarati thali restaurant"
            },
            {
                "name": "Thai Orchid",
                "description": "Authentic Thai cuisine in elegant setting"
            },
            {
                "name": "Sushi Square",
                "description": "Premium Japanese dining experience"
            },
            {
                "name": "Mediterranean Blue",
                "description": "Mediterranean cuisine with fresh ingredients"
            },
            {
                "name": "Mughlai Darbar",
                "description": "Royal Mughlai cuisine experience"
            },
            {
                "name": "Continental Corner",
                "description": "Classic Continental cuisine with modern twist"
            },
            {
                "name": "Mexican Cantina",
                "description": "Vibrant Mexican restaurant with authentic flavors"
            },
            {
                "name": "Seoul Kitchen",
                "description": "Authentic Korean BBQ and traditional dishes"
            },
            {
                "name": "Vietnam House",
                "description": "Fresh Vietnamese cuisine with authentic flavors"
            },
            {
                "name": "Maharaja Kitchen",
                "description": "Royal Rajasthani dining experience with desert ambiance"
            },
            {
                "name": "Dim Sum Dynasty",
                "description": "Specializing in handcrafted dim sum and Cantonese cuisine"
            },
            {
                "name": "BBQ Nation",
                "description": "Interactive BBQ dining experience"
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
        print("Seed data created successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
