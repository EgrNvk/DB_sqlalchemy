from sqlalchemy import create_engine, text
import hashlib


class User:
    def __init__(self):
        self.engine = create_engine(
            "mssql+pyodbc://@LENOVO\\SQLEXPRESS/test_db?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
        )

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def show_users(self):
        with self.engine.connect() as conn:
            result = conn.execute(
                text("SELECT Id, Login, Password_hash FROM users ORDER BY Id")
            )
            users = result.fetchall()

            if not users:
                print("\nСписок користувачів порожній.\n")
                return

            print("\nСписок користувачів:")
            for user in users:
                print(f"Id: {user.Id}, Login: {user.Login}, Password_hash: {user.Password_hash}")
            print()

    def add_user(self, login: str, password: str):
        if not login or not password:
            print("Login і пароль не можуть бути порожніми.\n")
            return

        password_hash = self.hash_password(password)

        try:
            with self.engine.connect() as conn:
                conn.execute(
                    text("INSERT INTO users (Login, Password_hash) VALUES (:login, :password_hash)"),
                    {"login": login, "password_hash": password_hash}
                )
                conn.commit()
            print("Користувача додано.\n")
        except Exception as e:
            pass

    def delete_user(self, user_id: int):
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("DELETE FROM users WHERE Id = :id"),
                    {"id": user_id}
                )
                conn.commit()

                if result.rowcount == 0:
                    print("Користувача з таким Id не знайдено.\n")
                else:
                    print("Користувача видалено.\n")
        except Exception as e:
            pass


client = User()

while True:
    print("1 - Показати список користувачів")
    print("2 - Додати користувача")
    print("3 - Видалити користувача")
    print("0 - Вихід")

    choice = input("Оберіть дію: ").strip()

    if choice == "1":
        client.show_users()

    elif choice == "2":
        login = input("Введіть login: ").strip()
        password = input("Введіть пароль: ").strip()
        client.add_user(login, password)

    elif choice == "3":
        user_id = input("Введіть Id користувача для видалення: ").strip()

        if user_id.isdigit():
            client.delete_user(int(user_id))
        else:
            print("Id має бути числом.\n")

    elif choice == "0":
        print("Завершення програми.")
        break