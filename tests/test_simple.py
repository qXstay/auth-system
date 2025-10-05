import sys
import os
from pathlib import Path

# Добавляем корневую директорию проекта в Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from main import app
from fastapi.testclient import TestClient
import pytest

client = TestClient(app)


def test_main_endpoint():
    """Тест главной страницы"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Auth System API"}


def test_auth_flow():
    """Тест полного цикла аутентификации"""
    # Тестируем регистрацию
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test_pytest@example.com",
        "password": "testpass123",
        "role_id": 2
    }

    response = client.post("/auth/auth/register", json=user_data)
    assert response.status_code == 200

    # Тестируем логин
    response = client.post("/auth/auth/login", json={
        "email": "test_pytest@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

    token = response.json()["access_token"]

    # Тестируем защищенный endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200


def test_unauthenticated_access():
    """Тест доступа без аутентификации"""
    response = client.get("/resource/products")
    assert response.status_code == 401


def test_admin_access():
    """Тест админского доступа"""
    # Логинимся как админ (должен существовать в базе)
    response = client.post("/auth/auth/login", json={
        "email": "admin@example.com",
        "password": "admin123"
    })

    # Если админ активен - тестируем, если нет - пропускаем
    if response.status_code == 200:
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Проверяем админские права
        response = client.get("/users/all", headers=headers)
        assert response.status_code == 200
    else:
        # Если админ деактивирован, пропускаем тест
        pytest.skip("Admin account is deactivated")


def test_product_crud():
    """Тест CRUD операций с продуктами"""
    # Сначала регистрируем и логиним пользователя
    user_data = {
        "first_name": "Product",
        "last_name": "Test",
        "email": "product_test@example.com",
        "password": "testpass123",
        "role_id": 2
    }

    client.post("/auth/auth/register", json=user_data)
    response = client.post("/auth/auth/login", json={
        "email": "product_test@example.com",
        "password": "testpass123"
    })

    if response.status_code == 200:
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Создаем продукт
        product_data = {
            "name": "Test Product",
            "description": "Test Description"
        }
        response = client.post("/resource/products", headers=headers, json=product_data)
        assert response.status_code == 200
        product_id = response.json()["id"]

        # Получаем продукты
        response = client.get("/resource/products", headers=headers)
        assert response.status_code == 200

        # Обновляем продукт
        update_data = {
            "name": "Updated Product",
            "description": "Updated Description"
        }
        response = client.put(f"/resource/products/{product_id}", headers=headers, json=update_data)
        assert response.status_code == 200

        # Удаляем продукт
        response = client.delete(f"/resource/products/{product_id}", headers=headers)
        assert response.status_code == 200