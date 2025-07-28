from fastapi import FastAPI
from api.main import app as api_app
from db.database import engine
from db.models import Base

app = FastAPI(title="Trainer Management System")

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to Trainer Management System"}
