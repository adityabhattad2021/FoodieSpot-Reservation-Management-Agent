from datetime import time, date, timedelta
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Restaurant, Table, Customer, Reservation, CuisineType, PriceRange, Ambiance, TableStatus
import random
from enum import Enum


def seed_data():
    db = SessionLocal()
    try:
        # Seed Restaurants
        restaurant_data = [
            {
                "name": "Taj Mahal",
                "cuisine_type": CuisineType.NORTH_INDIAN,
                "area": "Indiranagar",
                "price_range": PriceRange.PREMIUM,
                "ambiance": Ambiance.FINE_DINING,
                "description": "Authentic North Indian cuisine in a luxurious setting with royal Mughal ambiance",
                "specialties": "Butter Chicken, Dal Makhani, Naan, Biryani",
                "dietary_options": "Vegetarian, Vegan, Gluten-free options",
                "features": "Live music, Private dining rooms, Valet parking, Wine cellar"
            },
            {
                "name": "Punjab Grill",
                "cuisine_type": CuisineType.PUNJABI,
                "area": "Koramangala",
                "price_range": PriceRange.MODERATE,
                "ambiance": Ambiance.FAMILY,
                "description": "Authentic Punjabi cuisine with traditional charm",
                "specialties": "Sarson da Saag, Makki di Roti, Butter Chicken",
                "dietary_options": "Vegetarian, Non-vegetarian",
                "features": "Outdoor seating, Live tandoor, Weekend buffet"
            },
            {
                "name": "Dakshin Flavors",
                "cuisine_type": CuisineType.SOUTH_INDIAN,
                "area": "JP Nagar",
                "price_range": PriceRange.BUDGET,
                "ambiance": Ambiance.CASUAL,
                "description": "Traditional South Indian cuisine served with authentic flavors",
                "specialties": "Masala Dosa, Idli, Filter Coffee, Thali",
                "dietary_options": "Pure Vegetarian",
                "features": "Quick service, Traditional banana leaf serving"
            },
            {
                "name": "Dragon House",
                "cuisine_type": CuisineType.CHINESE,
                "area": "Whitefield",
                "price_range": PriceRange.PREMIUM,
                "ambiance": Ambiance.FINE_DINING,
                "description": "Premium Chinese dining experience with modern Asian decor",
                "specialties": "Peking Duck, Dim Sum, Sichuan Specialties",
                "dietary_options": "Vegetarian options, Seafood",
                "features": "Private dining rooms, Tea ceremony, Live cooking stations"
            },
            {
                "name": "Bella Italia",
                "cuisine_type": CuisineType.ITALIAN,
                "area": "HSR Layout",
                "price_range": PriceRange.PREMIUM,
                "ambiance": Ambiance.FINE_DINING,
                "description": "Authentic Italian cuisine with imported ingredients",
                "specialties": "Wood-fired pizzas, Fresh pasta, Tiramisu",
                "dietary_options": "Vegetarian options, Gluten-free pasta available",
                "features": "Wine pairing, Outdoor seating, Live pizza counter"
            },
            {
                "name": "Kerala Kitchen",
                "cuisine_type": CuisineType.KERALA,
                "area": "Marathahalli",
                "price_range": PriceRange.MODERATE,
                "ambiance": Ambiance.FAMILY,
                "description": "Authentic Kerala cuisine with coastal flavors",
                "specialties": "Malabar Biryani, Appam, Kerala Fish Curry",
                "dietary_options": "Seafood, Vegetarian options",
                "features": "Traditional setup, Family style dining"
            },
            {
                "name": "Hyderabad House",
                "cuisine_type": CuisineType.HYDERABADI,
                "area": "Electronic City",
                "price_range": PriceRange.MODERATE,
                "ambiance": Ambiance.CASUAL,
                "description": "Famous for authentic Hyderabadi cuisine",
                "specialties": "Hyderabadi Biryani, Haleem, Double ka Meetha",
                "dietary_options": "Non-vegetarian, Vegetarian options",
                "features": "Take-away, Party orders"
            },
            {
                "name": "Bengal Bay",
                "cuisine_type": CuisineType.BENGALI,
                "area": "BTM Layout",
                "price_range": PriceRange.MODERATE,
                "ambiance": Ambiance.FAMILY,
                "description": "Traditional Bengali cuisine with home-style cooking",
                "specialties": "Fish Curry, Biryani, Bengali Sweets",
                "dietary_options": "Fish specialties, Vegetarian options",
                "features": "Cultural events, Festival specials"
            },
            {
                "name": "Gujarati Thali",
                "cuisine_type": CuisineType.GUJARATI,
                "area": "Jayanagar",
                "price_range": PriceRange.BUDGET,
                "ambiance": Ambiance.FAMILY,
                "description": "Unlimited Gujarati thali restaurant",
                "specialties": "Thali, Farsaan, Chaas",
                "dietary_options": "Pure Vegetarian, Jain options",
                "features": "Unlimited servings, Traditional seating"
            },
            {
                "name": "Thai Orchid",
                "cuisine_type": CuisineType.THAI,
                "area": "Indira Nagar",
                "price_range": PriceRange.PREMIUM,
                "ambiance": Ambiance.FINE_DINING,
                "description": "Authentic Thai cuisine in elegant setting",
                "specialties": "Tom Yum, Green Curry, Pad Thai",
                "dietary_options": "Vegetarian options, Seafood",
                "features": "Thai decor, Cooking classes"
            },
            {
                "name": "Sushi Square",
                "cuisine_type": CuisineType.JAPANESE,
                "area": "Koramangala",
                "price_range": PriceRange.LUXURY,
                "ambiance": Ambiance.FINE_DINING,
                "description": "Premium Japanese dining experience",
                "specialties": "Sushi, Sashimi, Ramen",
                "dietary_options": "Vegetarian sushi available",
                "features": "Sushi bar, Sake collection, Private rooms"
            },
            {
                "name": "Mediterranean Blue",
                "cuisine_type": CuisineType.MEDITERRANEAN,
                "area": "Richmond Town",
                "price_range": PriceRange.PREMIUM,
                "ambiance": Ambiance.BISTRO,
                "description": "Mediterranean cuisine with fresh ingredients",
                "specialties": "Hummus, Falafel, Shawarma",
                "dietary_options": "Vegan options, Halal",
                "features": "Open kitchen, Herb garden"
            },
            {
                "name": "Mughlai Darbar",
                "cuisine_type": CuisineType.MUGHLAI,
                "area": "Fraser Town",
                "price_range": PriceRange.MODERATE,
                "ambiance": Ambiance.FAMILY,
                "description": "Royal Mughlai cuisine experience",
                "specialties": "Biryanis, Kebabs, Curries",
                "dietary_options": "Non-vegetarian, Vegetarian options",
                "features": "Live music on weekends, Outdoor seating"
            },
            {
                "name": "Continental Corner",
                "cuisine_type": CuisineType.CONTINENTAL,
                "area": "MG Road",
                "price_range": PriceRange.PREMIUM,
                "ambiance": Ambiance.FINE_DINING,
                "description": "Classic Continental cuisine with modern twist",
                "specialties": "Steaks, Pasta, Continental grills",
                "dietary_options": "Gluten-free options available",
                "features": "Wine pairing, Live music, Cigar room"
            },
            {
                "name": "Mexican Cantina",
                "cuisine_type": CuisineType.MEXICAN,
                "area": "Indiranagar",
                "price_range": PriceRange.MODERATE,
                "ambiance": Ambiance.CASUAL,
                "description": "Vibrant Mexican restaurant with authentic flavors",
                "specialties": "Tacos, Burritos, Enchiladas",
                "dietary_options": "Vegetarian options, Vegan available",
                "features": "Tequila bar, Live music, Outdoor seating"
            }
        ]

        restaurants = [
            Restaurant(
                name=restaurant["name"],
                address=f"{random.randint(100, 999)} {restaurant['area']} Road, {restaurant['area']}",
                phone=f"98723{random.randint(100000, 999999)}",
                email=f"info@{restaurant['name'].lower().replace(' ', '')}.com",
                opening_time=time(11, 0),  # 11:00 AM
                closing_time=time(23, 0),  # 11:00 PM
                seating_capacity=random.randint(50, 200),
                special_event_space=random.choice([True, False]),
                cuisine_type=restaurant["cuisine_type"],
                price_range=restaurant["price_range"],
                ambiance=restaurant["ambiance"],
                description=restaurant["description"],
                specialties=restaurant["specialties"],
                dietary_options=restaurant["dietary_options"],
                features=restaurant["features"]
            )
            for restaurant in restaurant_data
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
                    status=TableStatus.AVAILABLE
                )
                tables.append(table)
        
        for table in tables:
            db.add(table)
        db.commit()

        # Seed Customers
        customer = Customer(
            name="Aditya Bhattad",
            phone=f"555-{random.randint(1000, 9999)}",
            email="aditya.bhattad@example.com"
        )
        db.add(customer)
        db.commit()


    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()