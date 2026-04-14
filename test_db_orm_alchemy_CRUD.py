from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, select
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, joinedload
import hashlib


Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Login = Column(String(100), nullable=False, unique=True)
    Password_hash = Column(String(64), nullable=False)

    profile = relationship("ProfileModel", back_populates="user", uselist=False)


class ProfileModel(Base):
    __tablename__ = "profiles"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    UserId = Column(Integer, ForeignKey("users.Id"), unique=True)
    FullName = Column(String(255))
    Email = Column(String(255))

    user = relationship("UserModel", back_populates="profile")


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
                select(UserModel)
                .options(joinedload(UserModel.profile))
                .order_by(UserModel.Id)
            ).scalars().all()

            if not users:
                print("\nСписок користувачів порожній.\n")
                return

            print("\nСписок користувачів:")
            for user in users:
                profile = user.profile

                print(
                    f"Id: {user.Id}, "
                    f"Login: {user.Login}, "
                    f"Password_hash: {user.Password_hash}, "
                    f"FullName: {profile.FullName if profile else '—'}, "
                    f"Email: {profile.Email if profile else '—'}"
                )
            print()

    def add_user(self, login, password, full_name, email):
        if not login or not password or not full_name or not email:
            print("Усі поля мають бути заповнені.\n")
            return

        password_hash = self.hash_password(password)

        try:
            with self.Session() as session:
                user = UserModel(Login=login, Password_hash=password_hash)
                session.add(user)
                session.flush()

                profile = ProfileModel(
                    UserId=user.Id,
                    FullName=full_name,
                    Email=email
                )
                session.add(profile)

                session.commit()
                print("Користувача та профіль додано.\n")
        except Exception as e:
            print(f"Помилка при додаванні: {e}\n")

    def update_user(self, user_id, new_login, new_password, new_full_name, new_email):
        if not new_login or not new_password or not new_full_name or not new_email:
            print("Усі поля мають бути заповнені.\n")
            return

        try:
            with self.Session() as session:
                user = session.get(UserModel, user_id)

                if user is None:
                    print("Користувача з таким Id не знайдено.\n")
                    return

                user.Login = new_login
                user.Password_hash = self.hash_password(new_password)

                if user.profile is None:
                    profile = ProfileModel(
                        UserId=user.Id,
                        FullName=new_full_name,
                        Email=new_email
                    )
                    session.add(profile)
                else:
                    user.profile.FullName = new_full_name
                    user.profile.Email = new_email

                session.commit()
                print("Дані користувача та профілю оновлено.\n")
        except Exception as e:
            print(f"Помилка при оновленні: {e}\n")

    def delete_user(self, user_id):
        try:
            with self.Session() as session:
                user = session.get(UserModel, user_id)

                if user is None:
                    print("Користувача з таким Id не знайдено.\n")
                    return

                if user.profile is not None:
                    session.delete(user.profile)

                session.delete(user)
                session.commit()
                print("Користувача та профіль видалено.\n")
        except Exception as e:
            print(f"Помилка при видаленні: {e}\n")


client = User()

while True:
    print("=== CRUD меню ===")
    print("C - Create (додати користувача)")
    print("R - Read (показати список користувачів)")
    print("U - Update (оновити користувача)")
    print("D - Delete (видалити користувача)")
    print("0 - Вихід")

    choice = input("Оберіть дію: ").strip().upper()

    if choice == "C":
        login = input("Введіть логін: ").strip()
        password = input("Введіть пароль: ").strip()
        full_name = input("Введіть ім'я: ").strip()
        email = input("Введіть email: ").strip()
        client.add_user(login, password, full_name, email)

    elif choice == "R":
        client.show_users()

    elif choice == "U":
        user_id = input("Введіть Id користувача: ").strip()

        if user_id.isdigit():
            new_login = input("Введіть новий логін: ").strip()
            new_password = input("Введіть новий пароль: ").strip()
            new_full_name = input("Введіть нове ім'я: ").strip()
            new_email = input("Введіть новий email: ").strip()
            client.update_user(
                int(user_id),
                new_login,
                new_password,
                new_full_name,
                new_email
            )
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