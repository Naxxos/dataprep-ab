from sqlmodel import SQLModel
from sqlmodel import create_engine
import os


db_password = "vGXGLqTY4EF7DCiozYoKlqRRUaC7ECd"

DATABASE_URL = "postgresql://postgres:{}@localhost/actes_budgetaire".format(db_password)

engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)

def drop_and_create_db_and_tables():
    drop_db_and_tables()
    create_db_and_tables()



if __name__ == "__main__":
    create_db_and_tables()
