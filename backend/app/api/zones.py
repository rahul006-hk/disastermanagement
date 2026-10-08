from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.db_service import get_db
from app.models.db_models import ZoneDB
from app.schemas.schemas import ZoneBase

router = APIRouter()

@router.get("/zones", response_model=list[ZoneBase])
def get_zones(db: Session = Depends(get_db)):
    return db.query(ZoneDB).all()
