from app.database import engine, Base
from app.models import Restaurant, Table, Customer, Reservation
from app.seed import seed_data

def init_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
    
    print("Starting to seed data...")
    seed_data()
    print("Data seeded successfully!")

if __name__ == "__main__":
    init_database()