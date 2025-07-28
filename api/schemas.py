from pydantic import BaseModel, Field, validator
from typing import List, Optional

OBJECTIVE_OPTIONS = [
    "weight_loss", "muscle_gain", "endurance",
    "flexibility", "rehabilitation", "general_fitness"
]

TRAINING_TYPE_OPTIONS = [
    "personal_training", "group_classes",
    "online_coaching", "nutrition_plan", "combined"
]

SERVICE_OPTIONS = [
    "monthly_subscription", "single_session",
    "package_10", "package_20", "premium"
]

class ClientBase(BaseModel):
    name: str = Field(..., example="John Doe")
    weight: float = Field(..., example=75.5)
    age: int = Field(..., example=30)
    objectives: List[str] = Field(..., example=["weight_loss"])
    phone_number: str = Field(..., example="+1234567890")
    training_type: str = Field(..., example="personal_training")
    service: str = Field(..., example="monthly_subscription")
    observations: Optional[str] = Field(None)

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True