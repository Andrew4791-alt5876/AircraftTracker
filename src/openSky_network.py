import time

from src.base_api import APIClient


class OpenSkyClient(APIClient):
    """
    Клиент для OpenSky Network API.
    Используется для получения информации о самолётах в заданном регионе.
    """

    def __init__(self):
        super().__init__("https://opensky-network.org/api")

    def get_data(self, endpoint: str, params: dict = None) -> dict:
        return self._make_request(endpoint, params)

    def get_aircraft_in_bbox(self, list_of_coord_country: list) -> list:
        """
        Получает список самолётов в прямоугольной области (bounding box).
        Возвращает сырые данные в виде списка.
        """
        if list_of_coord_country == []:
            print("В запросе отсутствуют координаты страны!")
        list_of_aircrafts = []
        n = 0
        for coord in list_of_coord_country:
            n += 1
            try:
                endpoint = "states/all"
                params = {"lamin": coord[0], "lamax": coord[1], "lomin": coord[2], "lomax": coord[3]}
                data = (self.get_data(endpoint, params))["states"]
                list_of_aircrafts += data
                time.sleep(1)
            except BaseException as e:
                print(f"Ошибка получения данных о самолетах {n} {e}!")
        return list_of_aircrafts
