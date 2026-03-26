from typing import Any, Optional


class Aircraft:
    """Класс для работы с информацией о самолетах"""

    # Аннотации атрибутов класса
    id_aircraft: str
    callsign: str
    origin_country: str
    longitude: Optional[float]
    latitude: Optional[float]
    vertical_rate: Optional[float]
    velocity: Optional[float]
    geo_altitude: Optional[float]
    true_track: Optional[float]
    squawk: Optional[str]
    on_ground: Optional[bool]
    bar_altitude: Optional[float]

    def __init__(
        self,
        id_aircraft: str,
        callsign: str,
        origin_country: str,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
        vertical_rate: Optional[float] = None,
        velocity: Optional[float] = None,
        geo_altitude: Optional[float] = None,
        true_track: Optional[float] = None,
        squawk: Optional[str] = None,
        on_ground: Optional[bool] = None,
        bar_altitude: Optional[float] = None,
    ) -> None:

        # id_aircraft
        if isinstance(id_aircraft, str):
            self.id_aircraft = id_aircraft
        else:
            raise ValueError("id_aircraft должен быть строкой")

        # callsign
        if isinstance(callsign, str):
            self.callsign = callsign
        else:
            raise ValueError("callsign должен быть строкой")

        # origin_country – непустая строка
        if isinstance(origin_country, str) and origin_country.strip():
            self.origin_country = origin_country
        else:
            raise ValueError("origin_country должен быть непустой строкой")

        # longitude
        if isinstance(longitude, (int, float)) and -180 <= longitude <= 180:
            self.longitude = float(longitude)
        else:
            raise ValueError("longitude должен быть числом в диапазоне [-180, 180]")

        # latitude
        if isinstance(latitude, (int, float)) and -90 <= latitude <= 90:
            self.latitude = float(latitude)
        else:
            raise ValueError("latitude должен быть числом в диапазоне [-90, 90]")

        # bar_altitude – может быть None или числом
        if bar_altitude is not None:
            self.bar_altitude = float(bar_altitude)
        else:
            self.bar_altitude = 0.0

        # on_ground
        if isinstance(on_ground, bool):
            self.on_ground = on_ground
        else:
            raise ValueError("on_ground должен быть True или False")

        # velocity – по умолчанию 0.0, если None
        if velocity is not None:
            self.velocity = float(velocity)
        else:
            self.velocity = 0.0

        # true_track – опционально
        if true_track is None:
            self.true_track = None
        elif isinstance(true_track, (int, float)) and 0.0 <= true_track <= 359.99:
            self.true_track = float(true_track)
        else:
            raise ValueError("true_track должен быть числом в диапазоне [0.0, 359.99] или None")

        # vertical_rate – по умолчанию 0.0, если None
        if vertical_rate is not None:
            self.vertical_rate = float(vertical_rate)
        else:
            self.vertical_rate = 0.0

        # geo_altitude – по умолчанию 0.0, если None
        if geo_altitude is not None:
            self.geo_altitude = float(geo_altitude)
        else:
            self.geo_altitude = 0.0

        # squawk – по умолчанию "0000", если None; иначе должна быть строка
        if squawk is None:
            self.squawk = "0000"
        elif isinstance(squawk, str):
            self.squawk = squawk
        else:
            raise ValueError("squawk должен быть строкой или None")

    def __repr__(self) -> str:
        """Строковое представление объекта для отладки."""
        return (
            f"Aircraft(id_aircraft='{self.id_aircraft}', callsign='{self.callsign}', country='{self.origin_country}', "
            f"lat={self.latitude}, lon={self.longitude}, vert_rate={self.vertical_rate}, "
            f"vel={self.velocity}, alt={self.geo_altitude}, "
            f"true_track={self.true_track}, squawk='{self.squawk}', on_ground={self.on_ground})"
        )

    def __eq__(self, other: Any) -> bool:
        """Сравнение на равенство по скорости и высоте."""
        if not isinstance(other, Aircraft):
            return NotImplemented
        return (self.velocity, self.geo_altitude) == (other.velocity, other.geo_altitude)

    def __lt__(self, other: Any) -> bool:
        """Сравнение 'меньше' по скорости и высоте."""
        if not isinstance(other, Aircraft):
            return NotImplemented
        return (self.velocity, self.geo_altitude) < (other.velocity, other.geo_altitude)

    def to_dict(self) -> dict:
        """Преобразует объект в словарь для сохранения в JSON."""
        return {
            "id_aircraft": self.id_aircraft,
            "callsign": self.callsign,
            "country": self.origin_country,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "vertical_rate": self.vertical_rate,
            "velocity": self.velocity,
            "altitude": self.geo_altitude,
            "true_track": self.true_track,
            "squawk": self.squawk,
            "on_ground": self.on_ground,
            "bar_altitude": self.bar_altitude,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Aircraft":
        """Создаёт объект Aircraft из словаря."""
        return cls(
            id_aircraft=data.get("id_aircraft", ""),
            callsign=data.get("callsign", ""),
            origin_country=data.get("country", ""),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            vertical_rate=data.get("vertical_rate"),
            velocity=data.get("velocity"),
            geo_altitude=data.get("altitude"),
            true_track=data.get("true_track"),
            squawk=data.get("squawk"),
            on_ground=data.get("on_ground"),
            bar_altitude=data.get("bar_altitude"),
        )
