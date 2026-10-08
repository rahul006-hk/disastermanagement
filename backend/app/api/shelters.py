from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.db_service import get_db
from app.models.db_models import ShelterDB
from app.schemas.schemas import ShelterBase

router = APIRouter()

@router.get("/shelters", response_model=list[ShelterBase])
def get_shelters(db: Session = Depends(get_db)):
    return db.query(ShelterDB).all()
