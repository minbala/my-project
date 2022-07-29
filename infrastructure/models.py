from sqlalchemy import Column
from .database import Base
from sqlalchemy import Column,Integer,String,ForeignKey,TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ ="users"
    
    email =Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    id = Column(Integer,primary_key=True,nullable=False)
    created_at =Column(TIMESTAMP(timezone=True),nullable=False,server_default =text("now()"))
    
class Page(Base):
    __tablename__= "pages"
    
    title=Column(String,nullable=False)
    id=Column(Integer,primary_key=True,nullable=False)
    content=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner=relationship("User")