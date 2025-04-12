from unittest.mock import patch
import pytest
from httpx import AsyncClient
from app.main import app
from app.schemas.wallet import WalletRequestCreate
from app.models.wallet import WalletRequest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_create_wallet_request():
    # Мокируем функцию get_tron_info
    with patch('app.services.tron_client.get_tron_info') as mock_get_tron_info:
        # Здесь можно подставить тестовые данные
        mock_get_tron_info.return_value = {
            'bandwidth': 100,
            'energy': 200,
            'balance': 50.0
        }

        # Подготовка данных для POST-запроса
        request_data = WalletRequestCreate(wallet_address="valid_wallet_address")

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/api/v1/wallet", json=request_data.dict())

        # Проверка ответа
        assert response.status_code == 200
        data = response.json()
        assert data['wallet_address'] == "valid_wallet_address"
        assert data['bandwidth'] == 100
        assert data['energy'] == 200
        assert data['balance'] == 50.0


@pytest.mark.asyncio
async def test_create_wallet_request_not_found():
    # Мокируем функцию get_tron_info для случая, когда кошелек не найден
    with patch('app.services.tron_client.get_tron_info') as mock_get_tron_info:
        mock_get_tron_info.return_value = None  # Возвращаем None, чтобы сгенерировать ошибку 404

        # Подготовка данных для POST-запроса
        request_data = WalletRequestCreate(wallet_address="invalid_wallet_address")

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/api/v1/wallet", json=request_data.dict())

        # Проверка ответа на ошибку
        assert response.status_code == 404
        assert response.json() == {"detail": "Wallet not found"}
