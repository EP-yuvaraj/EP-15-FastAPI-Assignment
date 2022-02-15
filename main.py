import datetime
from datetime import date
from hashlib import new
from os import stat
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import null , func
from database import sessionLocal
import models

import psycopg2.extras

conn = psycopg2.connect('postgresql://postgres:yuviboxer@localhost/school1_db')

app = FastAPI()


class School(BaseModel):
    id:int
    designation:str
    name:str
    phone_number:int
    
    class Config:
        orm_mode=True

class Classes(BaseModel):
    id:int
    techers_id:int
    name_of_student:str
    datetime: Optional[datetime.datetime]


    class Config:
        orm_mode=True


db=sessionLocal()

@app.get('/schools',response_model=List[School],status_code=200)
def get_all_data():
    data = db.query(models.School).all()
    
    return data


@app.post('/schools',response_model=School,status_code=status.HTTP_201_CREATED)
def create_data(school1:School):
    db_data=db.query(models.School).filter(models.School.name==school1.name).first()

    if db_data is not None:
        raise HTTPException(status_code=400,detail="Item already exists")

    new_data={}
    new_data=models.School(
        id=school1.id,
        designation=school1.designation,
        name=school1.name,
        phone_number=school1.phone_number
        
    )
    db.add(new_data)
    db.commit()
    
    return new_data


@app.put('/school/{school_id}',response_model=School,status_code=status.HTTP_200_OK)
def update_data(school_id:int,school1:School):
    item_to_update=db.query(models.School).filter(models.School.id==school_id).first()
    item_to_update.designation=school1.designation
    item_to_update.name=school1.name
    item_to_update.phone_number=school1.phone_number

    db.commit()

    return item_to_update


@app.delete('/school/{school_id}')
def delete_item(school_id:int):
    item_to_delete=db.query(models.School).filter(models.School.id==school_id).first()

    if item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    
    db.delete(item_to_delete)
    db.commit()
    return item_to_delete




@app.post('/class',response_model=Classes,status_code=status.HTTP_201_CREATED)
async def create_data(classes1:Classes):


    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''select designation from school2
                    WHERE id = %s''' ,[classes1.techers_id,])
    des_teacher = cursor.fetchone()

    if(des_teacher[0]!="teacher"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not a valid teacher")

    cursor.execute('''select designation from school2
                    WHERE name = %s''' ,[classes1.name_of_student,])
    des_student = cursor.fetchone()

    if(des_student[0]!= "student"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Only student can Enter in class")

    cursor.execute('''select techers_id from classes2
                    ''' )
    id_teacher = cursor.fetchone()


    if(id_teacher[0]!=None and id_teacher[0]!=classes1.techers_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Only one teacher will be there {id_teacher}")

    data = db.query(models.Classes).all()
    if(len(data)==5):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Can't Take any student")

    # print(des_teacher[0])

    new_data=models.Classes(
        id=classes1.id,
        techers_id=classes1.techers_id,
        name_of_student=classes1.name_of_student,
        datetime=classes1.datetime

    )


    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

@app.delete('/class/delete/{delete_id}')
def delete_item(delete_id:int):
    item_to_delete=db.query(models.Classes).filter(models.Classes.id==delete_id).first()

    if item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    
    db.delete(item_to_delete)
    db.commit()
    return item_to_delete

@app.get('/class',response_model=List[Classes],status_code=200)
def get_all_data():
    data = db.query(models.Classes).all()
    if(len(data)==5):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Can't Take any student")
    return data
