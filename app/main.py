from random import randrange
from typing import Optional
import time

from fastapi import Body, FastAPI,Response, status, HTTPException
#pydantic is a library used to define schema for validation the incoming post requests will be verified by the the schmma deifined on the class.
from pydantic import BaseModel

#psycopg is a postgresql database adapter for python
import psycopg2

from psycopg2.extras import RealDictCursor

app=FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    #we can also decalte optional porperties for post request
    # rating: Optional[int] = None
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password'
                    , cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")    
        print("Error: ", error)
        time.sleep(3)




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

 
@app.get("/posts")
def get_post():
    cursor.execute("""select * from posts""")
    posts=cursor.fetchall()
    return {"data":posts}


@app.get("/posts/latest")
def get_latest_post():
    post=my_post[len(my_post)-1]
    return {"detail": post}

@app.get("/posts/{id}", status_code=status.HTTP_403_FORBIDDEN)
def get_post(id: int):
    cursor.execute("""select * from posts where id = %s""", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} was not found")
    return {"Post detail": post}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post : Post):
    cursor.execute("""insert into posts(title, content, published) VALUES(%s, %s, %s) returning *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"Data": new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):

    cursor.execute("""delete from posts where id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post :Post):
    cursor.execute(""" update posts Set title=%s, content=%s, published=%s where id=%s returning *""", (post.title, post.content, post.published, str(id),))
    updated_post = cursor.fetchone() 
    conn.commit()
    if update_post==None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    return {"data": updated_post}




            