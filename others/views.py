from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy.orm import Session
import logging

from . import crud, schemas
from .database import get_db

router = APIRouter()
logger = logging.getLogger("api")

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

@router.get("/suppliers/{id}",response_model=schemas.Supplier2)
async def get_supplier(id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

@router.get("/suppliers/{id}/products")
async def get_product(id: PositiveInt, db: Session = Depends(get_db)):
    data = crud.get_product(db, id)
    if data is None or bool(data)==False:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return [{"ProductID": x['ProductID'], 'ProductName':f"{x['ProductName']}",'Category':{'CategoryID':x['CategoryID'],'CategoryName':f"{x['CategoryName']}"},'Discontinued':x['Discontinued'] } for x in data]

@router.post("/suppliers",status_code=status.HTTP_201_CREATED)
async def get_suppliers(data:schemas.Supp_post,db: Session = Depends(get_db)):
    return crud.make_supplier(db,data)

@router.put("/suppliers/{id}")
async def put_suppliers(id:PositiveInt,data:schemas.Supplier2, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, id)
    if db_supplier is None or bool(db_supplier)==False:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return crud.update_supplier(db,data,id)

@router.delete("/suppliers/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_suppliers(id: PositiveInt, db: Session = Depends(get_db)):
    db_supp= crud.get_supplier(db, id)
    if db_supp is None or bool(db_supp)==False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Supplier not found")
    crud.delete_supp(db, id)