from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.db_service import get_db
from app.models.db_models import VehicleDB
from app.schemas.schemas import VehicleBase

router = APIRouter()

@router.get("/vehicles", response_model=list[VehicleBase])
def get_vehicles(db: Session = Depends(get_db)):
    return db.query(VehicleDB).all()
