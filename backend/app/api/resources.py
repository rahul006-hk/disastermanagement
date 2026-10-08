from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.db_service import get_db
from app.models.db_models import WarehouseDB
from app.schemas.schemas import WarehouseBase

router = APIRouter()

@router.get("/resources", response_model=list[WarehouseBase])
def get_resources(db: Session = Depends(get_db)):
    return db.query(WarehouseDB).all()
