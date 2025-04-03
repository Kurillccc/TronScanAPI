import tronpy
from typing import Optional, Dict

async def get_tron_info(wallet_address: str) -> Optional[Dict[str, int]]:
    """
    Получаем информацию о кошельке в сети Tron.
    Возвращает словарь с ключами 'bandwidth', 'energy', 'balance'.
    """
    # Создаем клиент для взаимодействия с сетью Tron
    client = tronpy.Tron()

    try:
        # Получаем данные о кошельке
        account = await client.get_account(wallet_address)

        if account:
            # Возвращаем данные о кошельке
            return {
                "bandwidth": account["bandwidth"],
                "energy": account["energy"],
                "balance": account["balance"]
            }
        else:
            return None
    except Exception as e:
        print(f"Ошибка при получении данных для адреса {wallet_address}: {e}")
        return None
