from sqlalchemy import Column, Integer, String, Float, Boolean
from db.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    weight = Column(Float)
    age = Column(Integer)
    objectives = Column(String)
    phone_number = Column(String)
    training_type = Column(String)
    service = Column(String)
    observations = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)