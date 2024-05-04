import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse, JSONResponse

# Services
from api.services.storage_services import storage_instance

# Respositories
from api.repositories.user_repository import get_user_by_email

# Database
from api.core.db import get_db

# Utils
from api.utils.auth_utils import verify_token

# Constants
from api.constants.server_constants import TEMP_DIR

router = APIRouter(prefix="/files", tags=["Files"])


@router.get("/{filename}", response_model=None)
def get_file_by_name(
    filename: str, user_email: str = Depends(verify_token), db: Session = Depends(get_db)
):
    user = get_user_by_email(db, user_email)
    blob_name = os.path.join(str(user.id), filename)
    
    if not user:
        return JSONResponse(status_code=404, content={"detail": "User not found"})

    if not storage_instance.file_exists(blob_name):
        return JSONResponse(status_code=404, content={"detail": "File not found"})
        
    os.makedirs(TEMP_DIR, exist_ok=True)
    download_path = os.path.join(TEMP_DIR, blob_name.replace('/', '-'))
    storage_instance.download_file(blob_name, download_path)

    return FileResponse(download_path)

# LOCAL_DIR="/app/temp/"
# @router.get("/{filename}", response_model=None)
# def get_file_by_name(
#     filename: str, user_email: str = Depends(verify_token), db: Session = Depends(get_db)
# ):
#     user = get_user_by_email(db, user_email)
#     blob_name = os.path.join(str(user.id), filename)
    
#     if not user:
#         return JSONResponse(status_code=404, content={"detail": "User not found"})

#     if not storage_instance.file_exists(blob_name):
#         return JSONResponse(status_code=404, content={"detail": "File not found"})
        
#     os.makedirs(TEMP_DIR, exist_ok=True)
#     download_path = os.path.join(TEMP_DIR, blob_name.replace('/', '-'))
#     storage_instance.download_file(blob_name, download_path)
#     file_path = os.path.join(LOCAL_DIR, filename)
#     if not os.path.isfile(file_path):
#         raise HTTPException(status_code=404, detail="File not found")

#     return FileResponse(download_path)

# LOCAL_DIR="/app/temp2"
# @router.get("/{filename}", response_model=None)
# def get_file_by_name(
#     filename: str,
#     user_email: str = Depends(verify_token),
#     db: Session = Depends(get_db)
# ):
#     user = get_user_by_email(db, user_email)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     file_path = os.path.join(LOCAL_DIR, str(user.id), filename)
#     if not os.path.isfile(file_path):
#         raise HTTPException(status_code=404, detail="File not found")

#     return FileResponse(file_path, filename=filename)
    