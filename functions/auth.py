import json
import hashlib
from typing import Dict

USERS_FILE = "data/users.json"


def hash_password(password: str) -> str:
    """Возвращает SHA256-хэш пароля"""
    return hashlib.sha256(password.encode()).hexdigest()


def load_users() -> Dict[str, str]:
    """Загружает базу пользователей из JSON"""
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Если файла нет — создаем с тремя пользователями
        users = {
            "alice": hash_password("alice123"),
            "bob": hash_password("bob123"),
            "charlie": hash_password("charlie123")
        }
        save_users(users)
        return users


def save_users(users: Dict[str, str]) -> None:
    """Сохраняет базу пользователей в JSON"""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


def register_user(users: Dict[str, str], username: str, password: str) -> None:
    """Добавляет нового пользователя"""
    users[username] = hash_password(password)
    save_users(users)
    print(f"✅ Пользователь '{username}' успешно зарегистрирован!")


def authenticate_user(users: Dict[str, str], username: str, password: str) -> None:
    """Проверяет логин и пароль"""
    if username not in users:
        print("⚠️ Нет такого пользователя.")
        choice = input("Хотите создать нового пользователя? (y/n): ").lower()
        if choice == "y":
            register_user(users, username, password)
        else:
            print("Операция отменена.")
        return

    if users[username] != hash_password(password):
        print("❌ Неверный пароль.")
    else:
        print(f"✅ Добро пожаловать, {username}!")


def main() -> None:
    users = load_users()
    print("=== Аутентификация ===")
    username = input("Логин: ").strip()
    password = input("Пароль: ").strip()
    authenticate_user(users, username, password)


if __name__ == "__main__":
    main()
