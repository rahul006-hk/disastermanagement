from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.db_service import get_db
from app.models.db_models import HospitalDB
from app.schemas.schemas import HospitalBase

router = APIRouter()

@router.get("/hospitals", response_model=list[HospitalBase])
def get_hospitals(db: Session = Depends(get_db)):
    return db.query(HospitalDB).all()
