from  fastapi import APIRouter, Depends,HTTPException,status
from utils.utils import verify_password
from schemas.schemas import Token
from fastapi.security import OAuth2PasswordRequestForm
from infrastructure.database import get_db
from sqlalchemy.orm import Session
from infrastructure import models
from oauth2.oauth2 import create_access_token

router =APIRouter(prefix="/login",tags=["login"])

@router.post("/",response_model=Token)
def login(user_credentials:OAuth2PasswordRequestForm =Depends(),db:Session =Depends(get_db)):
    user =db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not verify_password(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Wrong Password")
    access_token =create_access_token(data={"user_id": user.id})
    
    return {"access_token":access_token,"token_type":"bearer"}
    


