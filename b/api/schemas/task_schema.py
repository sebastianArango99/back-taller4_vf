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
    pubsub_message_id: str