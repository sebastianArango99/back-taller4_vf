from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from api.core.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    tasks = relationship('Task', backref='user')


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_extension = Column(String, nullable=False)
    new_extension = Column(String, nullable=False)
    status = Column(Enum("uploaded", "processed", "failed", name="task_status"), nullable=False)
    time_stamp = Column(DateTime, nullable=False)
    pubsub_message_id = Column(String, unique=True, nullable=True)  # Replaced celery_task_id

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
