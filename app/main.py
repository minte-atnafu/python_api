from random import randrange
from typing import Optional, List
import time

from fastapi import Body, FastAPI,Response, status, HTTPException, Depends
#pydantic is a library used to define schema for validation the incoming post requests will be verified by the the schmma deifined on the class.
from pydantic import BaseModel

#psycopg is a postgresql database adapter for python
import psycopg2

from . import models, schemas
from psycopg2.extras import RealDictCursor
from .databse import engine, get_db
from sqlalchemy.orm import Session
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

 
@app.get("/posts", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    # this belwo two lines where use to find the posts from the database suing direct query qithout using any ORM
    # cursor.execute("""select * from posts""")
    # posts=cursor.fetchall()

    # using SQLALCHEMY ORM fetch the posts from the database also using sessions 

    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/latest")
def get_latest_post():
    post=my_post[len(my_post)-1]
    return {"detail": post}

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    #the two line below used direct sql qury with psycopg adapter to find indivula posts form the database
    # cursor.execute("""select * from posts where id = %s""", (id,))
    # post = cursor.fetchone()
    
    #get invidual post using the id 

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} was not found")
    return post



@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post : schemas.CreatePost, db: Session = Depends(get_db)):
    #this three line below where used to insert data to databse using direct sql query
    # cursor.execute("""insert into posts(title, content, published) VALUES(%s, %s, %s) returning *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    #inserting data to posts using sqlalchemy
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    #these three lines used to sql query for delteing from database
    # cursor.execute("""delete from posts where id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    #delete data from the database using SQLALCHEMY
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, updated_post :schemas.CreatePost, db: Session = Depends(get_db)):
    # updating posts from databse using direct sql query by psycopg adapter
    # cursor.execute(""" update posts Set title=%s, content=%s, published=%s where id=%s returning *""", (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone() 
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post==None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()




            