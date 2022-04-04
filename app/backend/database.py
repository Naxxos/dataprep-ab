from sqlmodel import SQLModel
from sqlmodel import create_engine
import os

db_password = os.environ["PG_ROOT_PASSWORD"]

DATABASE_URL = "postgresql://postgres:{}@localhost/actes_budgetaire".format(db_password)

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
