from fastapi import APIRouter
from api.schemas import OBJECTIVE_OPTIONS, TRAINING_TYPE_OPTIONS, SERVICE_OPTIONS

router = APIRouter(prefix="/options", tags=["options"])

@router.get("/")
async def get_options():
    return {
        "objectives": list(OBJECTIVE_OPTIONS),
        "training_types": list(TRAINING_TYPE_OPTIONS),
        "services": list(SERVICE_OPTIONS)
    }