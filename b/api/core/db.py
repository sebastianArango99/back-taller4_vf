from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="vmQymogtcaYpuYqYSQeLZoafBZJAWKNN",
    host="roundhouse.proxy.rlwy.net",
    database="railway",
    port=19049
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

