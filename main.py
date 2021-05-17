from fastapi import FastAPI, Depends, HTTPException

from others.views import router as northwind_api_router

from typing import Lis

from sqlalchemy.orm import Session

from others import crud, schemas
from others.database import get_db
app = FastAPI()

app.include_router(northwind_api_router, tags=["northwind"])


@app.get("/suppliers")
async def get_suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)