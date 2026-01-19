from fastapi import APIRouter,Depends,HTTPException,Path
from pydantic import BaseModel, Field
from ..models import Todos
from ..database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from .auth import get_current_user
router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str =Field(min_length=3)
    description:str =Field(min_length=3,max_length=100)
    priority:int =Field(gt=0,lt=6)
    complete:bool

@router.get("/")
async def read_all(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    return db.query(Todos).filter(Todos.owner_id==user.get('id').all())

@router.get("/todo/{todo_id}")
async def read_todo(user:user_dependency,db:db_dependency,todo_id:int=Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id==user.get('id').first())
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404,detail="Not found")

@router.post("/todo/")
async def create_todo(db:db_dependency,user:user_dependency,todo_request:TodoRequest):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    todo_model=Todos(**todo_request.model_dump(),owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()

@router.put("/todo/{todo_id}")
async def update_todo(user:user_dependency,db:db_dependency,todo_request:TodoRequest,todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail='To do Not found')

    todo_model.title=todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

@router.delete("/todo/{todo_id}")
async def delete_todo(user:user_dependency,db:db_dependency,todo_id: int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is  None:
        raise HTTPException(status_code=404,detail="Not found")
    db.query(Todos).filter(Todos.id==todo_id).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).delete()

    db.commit()