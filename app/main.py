from random import randrange
from typing import Optional, List
import time
from passlib.context import CryptContext
from fastapi import Body, FastAPI,Response, status, HTTPException, Depends
#pydantic is a library used to define schema for validation the incoming post requests will be verified by the the schmma deifined on the class.
from pydantic import BaseModel

#psycopg is a postgresql database adapter for python
import psycopg2

from . import models, schemas, utils
from psycopg2.extras import RealDictCursor
from .databse import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine) #create tabels from the models

app=FastAPI()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password'
#                     , cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")    
#         print("Error: ", error)
#         time.sleep(3)




my_post = [{"title": "first post 1", "content": "content one", "id":1}, {"title": "second post 2", "content": "content two", "id":2}, 
           {"title":"thrid post 3", "content":"content three", "id":3}]



#routing different endpoints

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")  #decorater for the root endpoint
def root(): 
    return {"message": "Hello World"}


def find_post(id):
    for p in my_post:
        if p["id"]==id:
            return p

def find_post_index(id):
    for i, p in enumerate(my_post):
        if p["id"]==id:
            return i   
    return None         

 



