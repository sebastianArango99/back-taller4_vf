from pydantic import BaseModel
from datetime import datetime

class TaskBase(BaseModel):
    filename: str
    original_extension: str
    new_extension: str

class Task(TaskBase):
    id: int
    time_stamp: datetime
    status: str
    celery_task_id: str