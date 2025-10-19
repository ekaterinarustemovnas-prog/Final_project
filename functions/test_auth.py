import os
import json
import builtins
import pytest
import auth
from auth import (
    hash_password,
    load_users,
    register_user,
    authenticate_user,
    USERS_FILE
)


@pytest.fixture
def clean_users_file(tmp_path, monkeypatch):
    test_file = tmp_path / "users.json"
    test_users = {
        "alice": hash_password("alice123"),
        "bob": hash_password("bob456")
    }
    with open(test_file, "w", encoding="utf-8") as f:
        json.dump(test_users, f)

    # Подменяем глобальную переменную в модуле auth_demo
    monkeypatch.setattr(auth, "USERS_FILE", str(test_file))
    yield (test_users, str(test_file))
    # monkeypatch автоматически откатит изменение после теста


def test_hash_password_consistent():
    """Проверка, что хэш пароля одинаков при повторных вызовах"""
    assert hash_password("secret") == hash_password("secret")


def test_load_users_creates_default(tmp_path, monkeypatch):
    """load_users создаёт файл, если его нет"""
    path = tmp_path / "users.json"
    monkeypatch.setattr("auth.USERS_FILE", str(path))
    users = load_users()
    assert os.path.exists(path)
    assert isinstance(users, dict)


def test_register_user_adds_user(clean_users_file):
    """Регистрация нового пользователя добавляет его в базу"""
    test_users, users_file_path = clean_users_file
    register_user(test_users, "charlie", "charlie789")

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "charlie" in data


def test_authenticate_user_valid(monkeypatch, clean_users_file):
    """Проверка успешной аутентификации"""
    test_users, users_file_path = clean_users_file
    monkeypatch.setattr(builtins, "input", lambda _: "n")
    authenticate_user(test_users, "alice", "alice123")  # просто не должно упасть


def test_authenticate_user_invalid_password(monkeypatch, clean_users_file):
    """Проверка неверного пароля"""
    test_users, users_file_path = clean_users_file
    monkeypatch.setattr(builtins, "input", lambda _: "n")
    authenticate_user(test_users, "alice", "wrongpass")


def test_authenticate_user_register_new(monkeypatch, clean_users_file):
    test_users, users_file_path = clean_users_file

    # Подменяем input() на согласие "y"
    monkeypatch.setattr("builtins.input", lambda _: "y")

    # Вызываем authenticate_user, передаём users (в памяти) и путь к файлу,
    # если функция принимает users_file — иначе она будет брать auth.USERS_FILE
    authenticate_user(test_users, "newuser", "1234")  # использует auth.USERS_FILE

    # Читаем файл по тому пути, который установили в fixture
    with open(users_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "newuser" in data
