from fastapi import FastAPI, Response, status, Request
from pydantic import BaseModel
from hashlib import sha512
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime, time, timedelta, date
from fastapi.encoders import jsonable_encoder
app = FastAPI()
app.counter = 0
app.id_reg = 1
app.patient_list = []

class HelloResp(BaseModel):
    msg: str


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.get("/counter")
def counter():
    app.counter += 1
    return app.counter


@app.get("/hello/{name}", response_model=HelloResp)
def hello_name_view(name: str):
    return HelloResp(msg=f"Hello {name}")


@app.get("/method")
def method():
    return {"method": "GET"}

@app.get("/auth")
def auth(password:str,password_hash:str, response:Response):
    password_sha512 = sha512(password.encode())
    if password_sha512.hexdigest() == password_hash:
        response.status_code = status.HTTP_204_NO_CONTENT
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED

class Patient(BaseModel):
    id: Optional[int]
    name:str
    surname:str
    register_date: Optional[date]
    vaccination_date: Optional[date]

@app.post("/register")
async def register(patient: Patient, response: Response):
    patient.id = app.id_reg
    patient.register_date = date.today()
    plus_data = len(patient.name)+len(patient.surname)
    patient.vaccination_date = date.today()+timedelta(days=plus_data)
    app.patient_list.append(patient) 
    app.id_reg +=1
    response.status_code = status.HTTP_201_CREATED
    return jsonable_encoder(patient)

@app.get("/patient/{id}")
def patient_reg(id: int, response: Response):
    if id<1:
        response.status_code = status.HTTP_400_BAD_REQUEST
    else:
        if len(app.patient_list)!=0:
            for patient in app.patient_list:
                if patient.id == id:
                    response.status_code = status.HTTP_200_OK
                    return jsonable_encoder(patient)
                else:
                    response.status_code = status.HTTP_404_NOT_FOUND
        else:
            response.status_code = status.HTTP_404_NOT_FOUND