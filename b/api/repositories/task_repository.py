from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

from api.models.model import Task


def create_task(db: Session, task: dict, user_id: int) -> Task:
    db_task = Task(**task, user_id=user_id, time_stamp=datetime.now())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task_by_id(db: Session, task_id: int) -> Task:
    return db.query(Task).filter(Task.id == task_id).first()


def delete_task(db: Session, task_id: int, user_id: int) -> None:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    db.delete(task)
    db.commit()


def get_all_tasks_by_user(db: Session, user_id: int) -> list[Task]:
    return db.query(Task).filter(Task.user_id == user_id).order_by(desc(Task.id)).all()


def update_task_by_celery_task_id(db: Session, celery_task_id: str, status: str) -> Task:
    task = db.query(Task).filter(Task.celery_task_id == celery_task_id).first()
    task.status = status
    db.commit()
    return task


def get_task_by_celery_task_id(db: Session, celery_task_id: str) -> Task:
    return db.query(Task).filter(Task.celery_task_id == celery_task_id).first()