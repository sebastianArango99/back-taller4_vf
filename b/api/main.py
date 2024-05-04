from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.core.db import engine, Base
from api.controllers.root_controller import router as root_router
from api.controllers.auth_controller import router as auth_router
from api.controllers.task_controller import router as task_router
from api.controllers.file_controller import router as file_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router)
app.include_router(auth_router)
app.include_router(task_router, prefix="/api")
app.include_router(file_router, prefix="/api")
