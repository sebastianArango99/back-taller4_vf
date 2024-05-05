from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from api.models.model import Task


def create_task(db: Session, task: dict, user_id: int) -> Task:
    """Create a new task in the database."""
    db_task = Task(**task, user_id=user_id, time_stamp=datetime.now())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task_by_id(db: Session, task_id: int) -> Task:
    """Retrieve a task by its ID."""
    return db.query(Task).filter(Task.id == task_id).first()


def delete_task(db: Session, task_id: int, user_id: int) -> None:
    """Delete a task by its ID and user ID."""
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    db.delete(task)
    db.commit()


def get_all_tasks_by_user(db: Session, user_id: int) -> list[Task]:
    """Retrieve all tasks for a given user, ordered by the most recent."""
    return db.query(Task).filter(Task.user_id == user_id).order_by(desc(Task.id)).all()


def update_task_by_pubsub_message_id(db: Session, pubsub_message_id: str, status: str) -> Task:
    """Update task status using Pub/Sub message ID."""
    task = db.query(Task).filter(Task.pubsub_message_id == pubsub_message_id).first()
    if task:
        task.status = status
        db.commit()
        db.refresh(task)
    return task


def get_task_by_pubsub_message_id(db: Session, pubsub_message_id: str) -> Task:
    """Retrieve a task using the Pub/Sub message ID."""
    return db.query(Task).filter(Task.pubsub_message_id == pubsub_message_id).first()
