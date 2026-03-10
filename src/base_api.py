from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseAPIClient(ABC):
    """Абстрактный класс для работы с внешними API."""

    @abstractmethod
    def get_country_coordinates(self, country_name: str) -> Optional[Dict[str, float]]:
        """
        Получить географические координаты (bounding box) страны по её названию.
        Возвращает словарь с ключами: 'min_lat', 'max_lat', 'min_lon', 'max_lon'.
        """
        pass

    @abstractmethod
    def get_aircraft_in_area(
        self, min_lat: float, max_lat: float, min_lon: float, max_lon: float
    ) -> List[Dict[str, Any]]:
        """
        Получить информацию о самолётах, находящихся в заданной прямоугольной области.
        Возвращает список словарей с данными о каждом самолёте.
        """
        pass
