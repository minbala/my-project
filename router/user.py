from fastapi import APIRouter, Depends,HTTPException,status

from infrastructure import  models
from schemas.schemas import UserIn,UserOut
from typing import List
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from utils.utils import hash_password

router =APIRouter(prefix="/users",tags=["Users"])

@router.get("/",response_model=List[UserOut])
def get_users(db:Session =Depends(get_db)):
    return db.query(models.User).all()

@router.get("/{id}",response_model=UserOut)
def get_user(id:int,db :Session =Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with {id} was not found')
    return user_query.first()

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserOut)
def create_user(user:UserIn,db:Session =Depends(get_db)):
    user.password =hash_password(user.password)
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/{id}",response_model=UserOut)
def update_user(id:int,user:UserIn,db:Session =Depends(get_db)):
    user_query =db.query(models.User).filter(models.User.id == id)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user_query.update(user.dict(),synchronize_session=False)
    db.commit()
    return user_query.first()

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int,db:Session=Depends(get_db)):
    user_query =db.query(models.User).filter(models.User.id == id)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "sucessfully deleted"}