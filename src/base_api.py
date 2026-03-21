from abc import ABC, abstractmethod

import requests


class APIClient(ABC):
    """
    Абстрактный класс для работы с внешними API.
    Определяет общий интерфейс и базовый метод выполнения HTTP-запросов.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    @abstractmethod
    def get_data(self, endpoint: str, params: dict = None) -> dict:
        """Этот метод должен быть реализован в наследниках."""
        pass

    def _make_request(self, endpoint: str, params: dict = None, headers: dict = None) -> dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            # Обязательно передаём headers в requests.get
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Проверьте соединение с интернетом!")
            # raise ConnectionError(f"Ошибка при запросе к API: {e}")
