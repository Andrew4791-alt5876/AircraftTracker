from typing import Any, Dict, List, Optional

import requests

from src.base_api import BaseAPIClient


class OpenSkyNominatimClient(BaseAPIClient):
    """
    Конкретная реализация для Nominatim (координаты стран) и OpenSky Network (самолёты).
    """

    def __init__(self) -> None:
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"
        self.session = requests.Session()
        # Nominatim требует указания User-Agent (можно изменить на свой)
        self.session.headers.update({"User-Agent": "test-app/1.0"})
        # self.session.headers.update({
        #     'User-Agent': 'MyPythonApp/1.0 (contact@example.com)'
        # })

    def get_country_coordinates(self, country_name: str) -> Optional[Dict[str, float]]:
        """
        Запрашивает у Nominatim bounding box страны.
        Возвращает словарь с границами или None, если страна не найдена.
        """
        params = {"q": country_name, "format": "json", "limit": '1', "addressdetails": '1', "featuretype": "country"}
        try:
            response = self.session.get(self.nominatim_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if not data:
                print(f"Страна '{country_name}' не найдена.")
                return None

            # Bounding box приходит как список [min_lat, max_lat, min_lon, max_lon] ?
            # На самом деле Nominatim возвращает "boundingbox": ["min_lat", "max_lat", "min_lon", "max_lon"] (строки)
            # Или в некоторых версиях массив чисел. Преобразуем в float.
            bbox = data[0].get("boundingbox")
            if not bbox or len(bbox) < 4:
                print("Некорректный ответ от Nominatim (отсутствует boundingbox).")
                return None

            return {
                "min_lat": float(bbox[0]),
                "max_lat": float(bbox[1]),
                "min_lon": float(bbox[2]),
                "max_lon": float(bbox[3]),
            }
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к Nominatim: {e}")
            return None
        except (ValueError, KeyError, IndexError) as e:
            print(f"Ошибка обработки ответа Nominatim: {e}")
            return None

    def get_aircraft_in_area(
        self, min_lat: float, max_lat: float, min_lon: float, max_lon: float
    ) -> List[Dict[str, Any]]:
        """
        Запрашивает у OpenSky Network самолёты в указанном прямоугольнике.
        Возвращает список самолётов (каждый самолёт представлен словарём).
        """
        params = {"lamin": min_lat, "lamax": max_lat, "lomin": min_lon, "lomax": max_lon}
        try:
            response = self.session.get(self.opensky_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            # Поле 'states' содержит список самолётов, каждый — массив фиксированной длины.
            # Преобразуем в список словарей для удобства.
            states = data.get("states", [])
            if not states:
                return []

            # Описание полей согласно документации OpenSky:
            # 0: icao24, 1: callsign, 2: origin_country, 3: time_position,
            # 4: last_contact, 5: longitude, 6: latitude, 7: baro_altitude,
            # 8: on_ground, 9: velocity, 10: true_track, 11: vertical_rate,
            # 12: sensors, 13: geo_altitude, 14: squawk, 15: spi, 16: position_source
            field_names = [
                "icao24",
                "callsign",
                "origin_country",
                "time_position",
                "last_contact",
                "longitude",
                "latitude",
                "baro_altitude",
                "on_ground",
                "velocity",
                "true_track",
                "vertical_rate",
                "sensors",
                "geo_altitude",
                "squawk",
                "spi",
                "position_source",
            ]

            aircraft_list = []
            for state in states:
                # Длина массива может быть меньше 17, дополняем None до нужной длины
                full_state = state + [None] * (len(field_names) - len(state))
                aircraft_dict = dict(zip(field_names, full_state))
                aircraft_list.append(aircraft_dict)
            return aircraft_list

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к OpenSky: {e}")
            return []
        except (ValueError, KeyError) as e:
            print(f"Ошибка обработки ответа OpenSky: {e}")
            return []
