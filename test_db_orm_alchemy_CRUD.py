from sqlalchemy import create_engine, Column, String, Integer, select
from sqlalchemy.orm import declarative_base, sessionmaker
import hashlib


Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Login = Column(String(100), nullable=False, unique=True)
    Password_hash = Column(String(64), nullable=False)


class User:
    def __init__(self):
        self.engine = create_engine(
            "mssql+pyodbc://@LENOVO\\SQLEXPRESS/test_db?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
        )
        self.Session = sessionmaker(bind=self.engine)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def show_users(self):
        with self.Session() as session:
            users = session.execute(
                select(UserModel).order_by(UserModel.Id)
            ).scalars().all()

            if not users:
                print("\nСписок користувачів порожній.\n")
                return

            print("\nСписок користувачів:")
            for user in users:
                print(f"Id: {user.Id}, Login: {user.Login}, Password_hash: {user.Password_hash}")
            print()

    def add_user(self, login, password):
        if not login or not password:
            print("Login і пароль не можуть бути порожніми.\n")
            return

        password_hash = self.hash_password(password)

        try:
            with self.Session() as session:
                user = UserModel(Login=login, Password_hash=password_hash)
                session.add(user)
                session.commit()
            print("Користувача додано.\n")
        except Exception:
            print("Помилка при додаванні користувача.\n")

    def update_user(self, user_id, new_login, new_password):
        try:
            with self.Session() as session:
                user = session.get(UserModel, user_id)

                if user is None:
                    print("Користувача з таким Id не знайдено.\n")
                    return

                user.Login = new_login
                user.Password_hash = self.hash_password(new_password)

                session.commit()
                print("Дані користувача оновлено.\n")
        except Exception:
            print("Помилка при оновленні користувача.\n")

    def delete_user(self, user_id):
        try:
            with self.Session() as session:
                user = session.get(UserModel, user_id)

                if user is None:
                    print("Користувача з таким Id не знайдено.\n")
                    return

                session.delete(user)
                session.commit()
                print("Користувача видалено.\n")
        except Exception:
            print("Помилка при видаленні користувача.\n")


client = User()

while True:
    print("=== CRUD меню ===")
    print("C - Create (додати користувача)")
    print("R - Read (показати список)")
    print("U - Update (оновити користувача)")
    print("D - Delete (видалити користувача)")
    print("0 - Вихід")

    choice = input("Оберіть дію: ").strip().upper()

    if choice == "C":
        login = input("Введіть login: ").strip()
        password = input("Введіть пароль: ").strip()
        client.add_user(login, password)

    elif choice == "R":
        client.show_users()

    elif choice == "U":
        user_id = input("Введіть Id користувача: ").strip()

        if user_id.isdigit():
            new_login = input("Введіть новий login: ").strip()
            new_password = input("Введіть новий пароль: ").strip()
            client.update_user(int(user_id), new_login, new_password)
        else:
            print("Id має бути числом.\n")

    elif choice == "D":
        user_id = input("Введіть Id користувача для видалення: ").strip()

        if user_id.isdigit():
            client.delete_user(int(user_id))
        else:
            print("Id має бути числом.\n")

    elif choice == "0":
        print("Завершення програми.")
        break

    else:
        print("Невірний вибір.\n")