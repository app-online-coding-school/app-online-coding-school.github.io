from fastapi import FastAPI,Depends, responses,status,Request, Response, HTTPException
from sqlalchemy.orm import Session
import schemas
import models
from database import SessionLocal, engine
from fastapi.templating import Jinja2Templates


app=FastAPI()
templates = Jinja2Templates(directory="templates/")

models.Base.metadata.create_all(bind=engine) #this is important to create table in the database

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


#creates a new entry in the table "blog"
@app.post("/blog",status_code=201)
#or
#app.post("/blog",status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog, db:Session = Depends(get_db)): #request:schemas--->as class Blog is defined in schemas.py
                                             #db:session ---> otherwise, db is treated as a query parameter
                                             #used to get the database instance
   new_blog=models.Blog(title=request.title,body=request.body)
   db.add(new_blog)
   db.commit()
   db.refresh(new_blog)
   return new_blog

#getting existing blogs from the database
@app.get("/blogs")
def all(request: Request, db:Session = Depends(get_db)):
    blogs=db.query(models.Blog).all() #gets all records.
                                    #this is converted as SQL query.
    return templates.TemplateResponse('blogs2.html', context={'request': request,'blogs': blogs})

#get a particular blog from the database
@app.get("/blogs/{id}",status_code=200)
def show(id,response:Response,db:Session = Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog: #if no blog of {id} available,
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return {'detail':f"Blog with the id {id} is not available"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
    return {"id": blog.id, 'title': blog.title, 'description': blog.body}


#delete a particular blog
@app.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db:Session = Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog with id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'deletion done'

#update a blog
@app.put("/blog/{id}",status_code=status.HTTP_202_ACCEPTED)
def update(id,request:schemas.Blog,db:Session = Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} is not available")
    blog.update()
    db.commit()
    return 'updated successfully'
