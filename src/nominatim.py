from datetime import time

from src.base_api import APIClient


class NominatimClient(APIClient):
    """
    Клиент для Nominatim API (OpenStreetMap).
    Используется для получения географических координат стран.
    """

    def __init__(self):
        super().__init__("https://nominatim.openstreetmap.org")
        self.headers = {"User-Agent": "MyAircraftTracker/1.0 (tyrandr@list.ru)"}

    def _rate_limit(self):
        """Ожидает, чтобы с момента последнего запроса прошло не менее 1 секунды."""
        now = time.time()
        elapsed = now - NominatimClient._last_request_time
        if elapsed < 1.0:
            time.sleep(1.0 - elapsed)
        NominatimClient._last_request_time = time.time()

    def get_data(self, endpoint: str, params: dict = None) -> dict:
        """Реализация абстрактного метода get_data."""
        params = params or {}
        params["format"] = "json"  # добавляем обязательный параметр для Nominatim
        self._rate_limit()
        return self._make_request(endpoint, params, headers=self.headers)

    def get_country_coordinates(self, country_name: list) -> list:
        list_of_coord = []
        for country in country_name:
            try:
                params = {"q": country, "format": "json", "limit": 1, "addressdetails": 1}
                data = self._make_request("search", params, headers=self.headers)
                coord_of_country = data[0]["boundingbox"]
                list_of_coord.append(coord_of_country)
                return list_of_coord
            except (ValueError, IndexError, TypeError) as e:
                return []
