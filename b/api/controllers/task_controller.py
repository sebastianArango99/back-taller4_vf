from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
import os

# Repositories
from api.repositories.task_repository import (
    get_all_tasks_by_user,
    create_task,
    get_task_by_id,
    delete_task,
    update_task_by_pubsub_message_id,
    get_task_by_pubsub_message_id,
)
from api.repositories.user_repository import get_user_by_email

# Services
from api.services.storage_services import storage_instance
from api.services.pubsub_services import publish_message, get_task_status_from_pubsub

# Schemas
from api.schemas.task_schema import Task

# Utils
from api.utils.file_utils import create_temporal_file
from api.utils.auth_utils import verify_token

# Database
from api.core.db import get_db

# Constants
from api.constants.server_constants import ALLOWED_EXTENSIONS, ALLOWED_EXTENSIONS_TO_CONVERT

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=list[Task])
def get_all_tasks(user_email: str = Depends(verify_token), db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return get_all_tasks_by_user(db, user.id)


@router.post("/{extension}", response_model=Task)
async def create_task_for_user(
    extension: str,
    file: UploadFile = File(...),
    user_email: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    user = get_user_by_email(db, user_email)
    file_extension = file.filename.split(".")[-1]

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Extension not allowed")

    if file_extension not in ALLOWED_EXTENSIONS_TO_CONVERT:
        raise HTTPException(status_code=400, detail="File extension not allowed")

    # Create the temporary file
    user_id = str(user.id)
    temp_file = await create_temporal_file(user_id, file)

    # Upload the file to GCP
    blob_name = os.path.join(user_id, file.filename)
    storage_instance.upload_file(temp_file, blob_name)

    new_task = {
        "filename": file.filename.rsplit(".", 1)[0],
        "original_extension": file_extension,
        "new_extension": extension,
        "status": "uploaded",
    }

    # Publish the task to Pub/Sub
    pubsub_message_id = publish_message(user_id, temp_file, new_task)
    new_task["pubsub_message_id"] = pubsub_message_id

    # Create the database record
    db_task = create_task(db=db, task=new_task, user_id=user.id)

    return db_task


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.get("/status/{pubsub_message_id}", response_model=Task)
def get_task_status(pubsub_message_id: str, db: Session = Depends(get_db)):
    task_status = get_task_status_from_pubsub(pubsub_message_id)

    if task_status == "processed":
        return update_task_by_pubsub_message_id(db, pubsub_message_id, "processed")
    else:
        return get_task_by_pubsub_message_id(db, pubsub_message_id)


def get_gcp_file_path(user_id: int, filename: str, extension: str) -> str:
    return os.path.join(str(user_id), filename + "." + extension)


@router.delete("/{task_id}")
def delete_task_for_user(
    task_id: int,
    user_email: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        storage_instance.delete_file(
            get_gcp_file_path(user.id, task.filename, task.original_extension)
        )
        storage_instance.delete_file(get_gcp_file_path(user.id, task.filename, task.new_extension))
    except Exception:
        print("Failed to delete files from storage")

    delete_task(db, task_id, user.id)
    return {"message": "Task deleted successfully"}
