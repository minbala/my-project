from fastapi import APIRouter, Depends,status,HTTPException
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from infrastructure import models
from wikipedia import summary
from schemas.schemas import PageCreate,PageOut
from typing import List, Optional
from  oauth2.oauth2 import get_current_user

router=APIRouter(prefix="/view_page",tags=["view_page"])

@router.get("sample/{page_name}")
def view_page(page_name:str,current_user:int=Depends(get_current_user)):
    try:
        return summary(page_name)
    except Exception as e:
        return {"message": e}

@router.post("/{page_name}/{save}",status_code=status.HTTP_201_CREATED,response_model=PageOut)
def create_page(page_name:str,save:bool,db:Session =Depends(get_db),current_user:int=Depends(get_current_user)):
    if save:
        page={"title":page_name,"content":view_page(page_name=page_name)}
        new_page=models.Page(owner_id=current_user.id,**page)
        db.add(new_page)
        db.commit()
        db.refresh(new_page)
        return new_page
    
@router.get("/",response_model=List[PageOut])
def get_pages(db:Session =Depends(get_db),current_user:int=Depends(get_current_user),limit:int =5,
              skip:int=0,search:Optional[str]=""):
    return db.query(models.Page).filter(models.Page.title.contains(search)).limit(limit).offset(skip).all()

@router.get("/{id}",response_model=PageOut)
def get_page(id:int,db:Session =Depends(get_db),current_user:int =Depends(get_current_user)):
    page =db.query(models.Page).filter(id ==models.Page.id).first()
    if not page:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'page with {id} was not found')
    return page

@router.put("/{id}",response_model=PageOut)
def update_page(page:PageCreate,id:int,db:Session =Depends(get_db),current_user:int =Depends(get_current_user)):
    page_query=db.query(models.Page).filter(id == models.Page.id)
    if not page_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"page with {id} was not found")
    if page_query.first().id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Not authorized to perform requested action')
    page_query.update(page.dict(),synchronize_session=False)
    db.commit()
    return page_query.first()

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_page(id:int,db:Session =Depends(get_db),current_user:int =Depends(get_current_user)):
    page_query=db.query(models.Page).filter(id == models.Page.id)
    if not page_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"page with {id} was not found")
    if page_query.first().id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Not authorized to perform requested action')
    page_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "successfully deleted"}
    