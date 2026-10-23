
from fastapi import Body, Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from ..databse import engine, get_db
from .. import models, schemas, oauth2

router=APIRouter(
     prefix="/posts",
     tags=['Posts']
)

@router.get("/", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    # this belwo two lines where use to find the posts from the database suing direct query qithout using any ORM
    # cursor.execute("""select * from posts""")
    # posts=cursor.fetchall()

    # using SQLALCHEMY ORM fetch the posts from the database also using sessions 

    posts = db.query(models.Post).all()
    return posts




@router.get("/{id}", response_model=schemas.Post)
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



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post : schemas.CreatePost, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
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

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
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