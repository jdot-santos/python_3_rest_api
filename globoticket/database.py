# see PS course and https://chatgpt.com/c/260e8a56-b9ca-4dc0-a0a5-7423406a9d52
# for more info
import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# assuming logging isn't configured externally. Once it does, then remove
# logging.basicConfig().
# see https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#notice-logging
# for more info
logging.basicConfig()  # log messages to stdout
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


# for more connect options, see
# https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
