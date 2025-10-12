from .. import models, schemas, oauth2
from fastapi import APIRouter, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import session
from ..database import get_db
from typing import Optional
from fastapi import Response
from sqlalchemy import func

router = APIRouter(

    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=list[schemas.PostOut])
#@router.get("/", response_model=list[schemas.PostResponse])

def get_posts(db: session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
 
    return results
    
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    #new_post = cursor.fetchone()   
    #conn.commit()

    
    post.dict()
    new_post = models.Post(owner_id=get_current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    #post_dict = post.dict()
    #post_dict['id'] = randrange(0, 1000000)
    #my_posts.routerend(post_dict)
   
   
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)): # response: Response ):  
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    #post = cursor.fetchone()   
    #post = find_post(id)
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):

    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    #deleted_post = find_post_index(id)
    #if index is None:
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    post_delete = deleted_post.first()
    
    if post_delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    #my_posts.pop(deleted_post)
    if post_delete.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate,  db: session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()    
    #conn.commit()
    #index = find_post_index(id)
    update_post = db.query(models.Post).filter(models.Post.id == id)
    post_update = update_post.first()

    if post_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    #post_dict = post.dict()
    #post_dict['id'] = id
    #my_posts[index] = post_dict
    if post_update.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    update_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return update_post.first()