from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Login = Column(String(100), nullable=False)
    Password_hash = Column(String(64), nullable=False)


engine = create_engine(
    "mssql+pyodbc://@LENOVO\\SQLEXPRESS/test_db?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

Session = sessionmaker(bind=engine)

try:
    with Session() as session:
        with session.begin():
            user = UserModel(
                Login="commit_user",
                Password_hash="123"
            )
            session.add(user)

    print("Користувача збережено (COMMIT)")

except Exception as e:
    pass


try:
    with Session() as session:
        with session.begin():
            user = UserModel(
                Login="rollback_user",
                Password_hash="123"
            )
            session.add(user)

            print("Це помилковий користувач віклікаємо (ROLLBACK)")

            raise Exception("Викликаємо rollback")


except Exception as e:

    print(f"ROLLBACK спрацював: {e}")


with Session() as session:
    users = session.query(UserModel).order_by(UserModel.Id).all()

    print("\nТаблиця users:")

    for user in users:
        print(f"Id: {user.Id}, Login: {user.Login}, Password_hash: {user.Password_hash}")