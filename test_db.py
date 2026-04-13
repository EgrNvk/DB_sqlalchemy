import pyodbc
import hashlib

server = 'LENOVO\\SQLEXPRESS'
database = 'test_db'
username = ''
password = ''

conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

try:
    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()

        login = input("Введіть логін: ")
        password = input("Введіть пароль: ")

        password_hash = hash_password(password)

        cursor.execute(
            "INSERT INTO users (Login, Password_hash) VALUES (?, ?)",
            (login, password_hash))

        conn.commit()

        print("Дані успішно додані")

except Exception as e:
    print(f"Помилка: {e}")

try:
    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")

        print("Список користувачів:")
        for row in cursor.fetchall():
            print(row)

except Exception as e:
    print(f"Помилка при вибірці: {e}")