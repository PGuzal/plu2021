# -*- coding: utf-8 -*-
from fastapi import FastAPI, Response, status, Request, HTTPException
from pydantic import BaseModel
from hashlib import sha512
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime, time, timedelta, date
from fastapi.encoders import jsonable_encoder
import re
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


@app.put("/method")
def method():
    return {"method": "PUT"}


@app.get("/method")
def method():
    return {"method": "GET"}

@app.post("/method", status_code=status.HTTP_201_CREATED)
def method():
    return {"method": "POST"}


@app.delete("/method")
def method():
    return {"method": "DELETE"}

@app.options("/method")
def method():
    return {"method": "OPTIONS"}

@app.get("/auth")
def auth(password: Optional[str] = None ,password_hash: Optional[str]= None):
    password_sha512 = sha512(password.encode())
    if password_sha512.hexdigest() == password_hash:
        raise HTTPException(status_code=204)
    else:
        raise HTTPException(status_code=401)


class Patient(BaseModel):
    id: Optional[int]
    name:str
    surname:str
    register_date: Optional[date]
    vaccination_date: Optional[date]

def check_string(data):
    new_data = data
    for c in data:
        print(c.isdigit())
        if c.isalpha() == False:
            new_data = new_data.replace(c,'')
    new_data = new_data.translate(new_data.maketrans({'ó': 'o', 'ż': 'z','ź': 'z','ń':'n','ą':'a','ę':'e','ł':'l','ć':'c','ś':'s','Ó': 'O', 'Ż': 'Z','Ź': 'Z','Ń':'N','Ą':'A','Ę':'E','Ł':'L','Ć':'C','Ś':'S'}))
    return new_data

            
@app.post("/register")
async def register(patient: Patient, response: Response):
    patient.id = app.id_reg
    patient.name = check_string(patient.name)
    patient.surname = check_string(patient.surname)
    patient.register_date = date.today().strftime('%Y-%m-%d')
    plus_data = len(patient.name)+len(patient.surname)
    vaccination = date.today()+timedelta(days=plus_data)
    patient.vaccination_date = vaccination.strftime('%Y-%m-%d')
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