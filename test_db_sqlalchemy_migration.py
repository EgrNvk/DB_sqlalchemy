from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mssql+pyodbc://@LENOVO\\SQLEXPRESS/test_db?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Login = Column(String(100), nullable=False)
    Password_hash = Column(String(64), nullable=False)


class ProductModel(Base):
    __tablename__ = "products"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100), nullable=False)
    Price = Column(Integer, nullable=False)


try:
    with engine.connect() as conn:
        print("Підключення до БД успішне")
except Exception as e:
    print(f"Помилка підключення: {e}")