from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="MYZSFGObsZxyNfbhHDtMCvovzWtWDzoS",
    host="monorail.proxy.rlwy.net",
    database="railway",
    port=20426
)
engine = create_engine(url)
session = sessionmaker(bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
        