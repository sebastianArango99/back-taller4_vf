import re
from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

# Repositories
from api.repositories import user_repository
from api.repositories.user_repository import get_user_by_email

# Constants
from api.constants.auth_constants import ACCESS_TOKEN_EXPIRE_WEEKS

# Models
from api.schemas.auth_schema import Auth
from api.schemas.user_schema import User, UserCreate

# Utils
from api.utils.auth_utils import (
    authenticate_user,
    create_access_token,
)
from api.core.db import get_db


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=User)
def create_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    db_user = user_repository.get_user_by_email(db, email=form_data.username)
    if re.fullmatch(regex, form_data.username) is None:
        raise HTTPException(status_code=409, detail="Invalid Email Address")
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    user = UserCreate(email=form_data.username, password=form_data.password)
    return user_repository.create_user(db=db, user=user)

@router.post("/signin", response_model=Auth)
def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user =  get_user_by_email(db, form_data.username)
    authenticated_user = authenticate_user(user, form_data.password)

    if not authenticated_user:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token_expires = timedelta(weeks=ACCESS_TOKEN_EXPIRE_WEEKS)
    access_token = create_access_token(
        data={"email": authenticated_user.email}, expires_delta=access_token_expires
    )

    # Crea una instancia de User a partir del diccionario
    auth_user = User(id=authenticated_user.id, email=authenticated_user.email)

    return Auth(access_token=access_token, token_type="Bearer", user=auth_user)