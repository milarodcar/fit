import os
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from db.models import Base, Client

# TODO: Add height to the clients
# TODO: Separate objectives into a separate table and link with a many-many relationship
def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Sample client data
        sample_clients = [
            {
                "name": "Alex Johnson",
                "weight": 78.5,
                "age": 32,
                "objectives": "weight_loss,muscle_gain",
                "phone_number": "+15551234567",
                "training_type": "personal_training",
                "service": "monthly_subscription",
                "observations": "Prefers morning sessions",
                "is_active": True
            },
            {
                "name": "Maria Garcia",
                "weight": 65.2,
                "age": 28,
                "objectives": "flexibility,endurance",
                "phone_number": "+15559876543",
                "training_type": "group_classes",
                "service": "package_10",
                "observations": "Vegetarian diet",
                "is_active": True
            },
            {
                "name": "David Chen",
                "weight": 82.0,
                "age": 41,
                "objectives": "rehabilitation",
                "phone_number": "+15555555555",
                "training_type": "online_coaching",
                "service": "single_session",
                "observations": "Recovering from knee surgery",
                "is_active": True
            },
            {
                "name": "Sarah Williams",
                "weight": 70.8,
                "age": 25,
                "objectives": "general_fitness",
                "phone_number": "+15556667777",
                "training_type": "combined",
                "service": "premium",
                "observations": "Training for marathon",
                "is_active": True
            },
            {
                "name": "James Wilson",
                "weight": 90.3,
                "age": 38,
                "objectives": "muscle_gain",
                "phone_number": "+15558889999",
                "training_type": "personal_training",
                "service": "package_20",
                "observations": "Focus on strength training",
                "is_active": True
            }
        ]

        # Check if clients already exist
        if db.query(Client).count() == 0:
            for client_data in sample_clients:
                db_client = Client(**client_data)
                db.add(db_client)
            db.commit()
            print("✅ Database initialized with sample data")
        else:
            print("ℹ️ Database already contains data - no new records added")
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Delete existing database file if it exists
    if os.path.exists("trainer.db"):
        os.remove("trainer.db")
        print("🗑️ Removed existing database file")
    
    init_db()