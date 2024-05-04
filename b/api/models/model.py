from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from api.core.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    
    tasks = relationship('Task', backref='user')

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    original_extension = Column(String)
    new_extension = Column(String)
    status = Column (Enum("uploaded", "processed", name="task_status"))
    time_stamp = Column(DateTime)
    celery_task_id = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))