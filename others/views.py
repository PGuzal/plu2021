from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db

router = APIRouter()


@router.get("/shippers/{shipper_id}", response_model=schemas.Shipper)
async def get_shipper(shipper_id: PositiveInt, db: Session = Depends(get_db)):
    db_shipper = crud.get_shipper(db, shipper_id)
    if db_shipper is None:
        raise HTTPException(status_code=404, detail="Shipper not found")
    return db_shipper


@router.get("/shippers", response_model=List[schemas.Shipper])
async def get_shippers(db: Session = Depends(get_db)):
    return crud.get_shippers(db)

@router.get("/suppliers",response_model=List[schemas.Supplier])
async def get_suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)

@router.get("/suppliers/{id}",response_model=List[schemas.Supplier2])
async def get_suppliers(id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_shipper(db, id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Shipper not found")
    return db_supplier