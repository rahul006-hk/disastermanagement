from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.db_service import get_db
from app.models.db_models import RoadDB
from app.schemas.schemas import RoadBase, RoadUpdate

router = APIRouter()

@router.get("/roads", response_model=list[RoadBase])
def get_roads(db: Session = Depends(get_db)):
    return db.query(RoadDB).all()

@router.patch("/roads/{road_id}", response_model=RoadBase)
def update_road_status(road_id: str, update: RoadUpdate, db: Session = Depends(get_db)):
    road = db.query(RoadDB).filter(RoadDB.id == road_id).first()
    if not road:
        raise HTTPException(status_code=404, detail="Road not found")
    road.is_blocked = update.is_blocked
    db.commit()
    db.refresh(road)
    return road
