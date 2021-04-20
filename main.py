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

@app.put("/method",status_code=status.HTTP_200_OK)
def putmethod():
    return {"method": "PUT"}


@app.get("/method",status_code=status.HTTP_200_OK)
def getmethod():
    return {"method": "GET"}

@app.post("/method", status_code=status.HTTP_201_CREATED)
def postmethod():
    return {"method": "POST"}


@app.delete("/method",status_code=status.HTTP_200_OK)
def deletemethod():
    return {"method": "DELETE"}

@app.options("/method",status_code=status.HTTP_200_OK)
def optionsmethod():
    return {"method": "OPTIONS"}

@app.get("/auth")
def auth(password: Optional[str] = None ,password_hash: Optional[str]= None):
    if password != None or password_hash !=None:
        password_encode = password.encode()
        password_sha512 = sha512(password_encode)
        if password_sha512.hexdigest() == password_hash:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


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
    patient.register_date = date.today().strftime('%Y-%m-%d')
    plus_data = len(check_string(patient.name))+len(check_string(patient.surname))
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