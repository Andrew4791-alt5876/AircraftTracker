class Aircraft:
    """Класс для работы с информацией о самолетах"""

    def __init__(
        self,
        id_aircraft: str,
        callsign: str,
        origin_country: str,
        longitude: float,
        latitude: float,
        baro_altitude: float,
        on_ground: bool,
        velocity: float,
        true_track: float,
        vertical_rate: float,
        geo_altitude: float,
    ) -> None:

        if not isinstance(id_aircraft, str):
            raise ValueError("id_aircraft должен быть строкой")
        if not isinstance(callsign, str):
            raise ValueError("callsign должен быть строкой")
        if not isinstance(origin_country, str) or not origin_country.strip():
            raise ValueError("origin_country должен быть непустой строкой")
        if not isinstance(longitude, (int, float)) or not (-180 <= longitude <= 180):
            raise ValueError("longitude должен быть числом в диапазоне [-180, 180]")
        if not isinstance(latitude, (int, float)) or not (-90 <= latitude <= 90):
            raise ValueError("latitude должен быть числом в диапазоне [-90, 90]")
        if not isinstance(baro_altitude, (int, float)) and baro_altitude is not None:
            raise ValueError("baro_altitude должен быть неотрицательным числом")
        elif baro_altitude in (None, 0):
            baro_altitude = 0
        if not isinstance(on_ground, bool):
            raise ValueError("on_ground должен быть True или False")
        if velocity in (None, 0):
            velocity = 0.0
        if not isinstance(true_track, (int, float)) or not 0.0 <= true_track <= 359.99:
            raise ValueError("true_track должен быть числом в диапазоне [0.0, 359.99]")
        if vertical_rate in (None, 0):
            vertical_rate = 0.0
        if geo_altitude in (None, 0):
            geo_altitude = 0.0

        self.id_aircraft = id_aircraft
        self.callsign = callsign
        self.origin_country = origin_country
        self.longitude = float(longitude)
        self.latitude = float(latitude)
        self.baro_altitude = baro_altitude
        self.on_ground = bool(on_ground)
        self.velocity = float(velocity)
        self.true_track = float(true_track)
        self.vertical_rate = vertical_rate
        self.geo_altitude = geo_altitude

    def __repr__(self) -> str:
        """Строковое представление объекта для отладки."""
        return (
            f"Aircraft(id_aircraft='{self.id_aircraft}', "
            f"callsign='{self.callsign}',"
            f" origin='{self.origin_country}', "
            f"vel={self.velocity}, "
            f"alt={self.geo_altitude})"
        )

    def __eq__(self, other) -> bool:
        """Сравнение на равенство по скорости и высоте."""
        if not isinstance(other, Aircraft):
            return NotImplemented
        return (self.velocity, self.geo_altitude) == (other.velocity, other.geo_altitude)

    def __lt__(self, other) -> bool:
        """Сравнение 'меньше' по скорости и высоте."""
        if not isinstance(other, Aircraft):
            return NotImplemented
        return (self.velocity, self.geo_altitude) < (other.velocity, other.geo_altitude)

    def sort_aircrafts_by_altitude(self):
        pass
