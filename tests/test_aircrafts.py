import pytest

from src.aircrafts import Aircraft


class TestAircraftInit:
    """Тесты инициализации Aircraft."""

    def test_valid_aircraft(self) -> None:
        """Проверка корректного создания объекта."""
        plane = Aircraft(
            id_aircraft="ABC123",
            callsign="ABC123",
            origin_country="Russia",
            longitude=55.0,
            latitude=37.0,
            vertical_rate=10.5,
            velocity=250.3,
            geo_altitude=10000.0,
            true_track=180.0,
            squawk="1234",
            on_ground=False,
            bar_altitude=9500.0,
        )
        assert plane.id_aircraft == "ABC123"
        assert plane.callsign == "ABC123"
        assert plane.origin_country == "Russia"
        assert plane.longitude == 55.0
        assert plane.latitude == 37.0
        assert plane.vertical_rate == 10.5
        assert plane.velocity == 250.3
        assert plane.geo_altitude == 10000.0
        assert plane.true_track == 180.0
        assert plane.squawk == "1234"
        assert plane.on_ground is False
        assert plane.bar_altitude == 9500.0

    def test_default_values(self) -> None:
        """Проверка значений по умолчанию, если параметры не переданы."""
        plane = Aircraft(id_aircraft="ID", callsign="CALL", origin_country="Country")
        assert plane.longitude == 0.0
        assert plane.latitude == 0.0
        assert plane.vertical_rate == 0.0
        assert plane.velocity == 0.0
        assert plane.geo_altitude == 0.0  # т.к. bar_altitude тоже 0
        assert plane.true_track == 0.0
        assert plane.squawk == "0000"
        assert plane.on_ground is False
        assert plane.bar_altitude == 0.0

    def test_id_aircraft_non_string(self) -> None:
        """Если id_aircraft не строка, становится пустой строкой."""
        plane = Aircraft(id_aircraft=123, callsign="CALL", origin_country="Country")  # type: ignore[arg-type]
        assert plane.id_aircraft == ""

    def test_callsign_non_string(self) -> None:
        """Если callsign не строка, становится пустой строкой."""
        plane = Aircraft(id_aircraft="ID", callsign=456, origin_country="Country")  # type: ignore[arg-type]
        assert plane.callsign == ""

    def test_callsign_stripped(self) -> None:
        """callsign обрезается по краям."""
        plane = Aircraft(id_aircraft="ID", callsign="  CALL  ", origin_country="Country")
        assert plane.callsign == "CALL"

    def test_origin_country_non_string(self) -> None:
        """Если origin_country не строка, становится пустой строкой."""
        plane = Aircraft(id_aircraft="ID", callsign="CALL", origin_country=789)  # type: ignore[arg-type]
        assert plane.origin_country == ""

    def test_longitude_out_of_range(self) -> None:
        """longitude вне [-180,180] заменяется на 0.0."""
        plane = Aircraft(id_aircraft="ID", callsign="CALL", origin_country="Country", longitude=200)
        assert plane.longitude == 0.0

    def test_longitude_invalid_type(self) -> None:
        """longitude не число -> 0.0."""
        plane = Aircraft(
            id_aircraft="ID",
            callsign="CALL",
            origin_country="Country",
            longitude="invalid")  # type: ignore[arg-type]
        assert plane.longitude == 0.0

    def test_latitude_out_of_range(self) -> None:
        """latitude вне [-90,90] заменяется на 0.0."""
        plane = Aircraft(id_aircraft="ID", callsign="CALL", origin_country="Country", latitude=100)
        assert plane.latitude == 0.0

    def test_true_track_out_of_range(self) -> None:
        """true_track вне [0,360] заменяется на 0.0."""
        plane = Aircraft(id_aircraft="ID", callsign="CALL", origin_country="Country", true_track=450)
        assert plane.true_track == 0.0

    def test_on_ground_non_bool_converted_to_bool(self) -> None:
        """Небулевы значения приводятся к bool по правилам Python."""
        plane = Aircraft(
            id_aircraft="ID",
            callsign="CALL",
            origin_country="Country",
            on_ground="yes")  # type: ignore[arg-type]
        assert plane.on_ground is True

        plane = Aircraft(
            id_aircraft="ID",
            callsign="CALL",
            origin_country="Country",
            on_ground="")  # type: ignore[arg-type]
        assert plane.on_ground is False

        plane = Aircraft(
            id_aircraft="ID",
            callsign="CALL",
            origin_country="Country",
            on_ground=123)  # type: ignore[arg-type]
        assert plane.on_ground is True

    def test_on_ground_none(self) -> None:
        """on_ground None -> False."""
        plane = Aircraft(id_aircraft="ID", callsign="CALL", origin_country="Country", on_ground=None)
        assert plane.on_ground is False

    def test_squawk_non_string(self) -> None:
        """squawk не строка -> '0000'."""
        plane = Aircraft(
            id_aircraft="ID",
            callsign="CALL",
            origin_country="Country",
            squawk=777)  # type: ignore[arg-type]
        assert plane.squawk == "0000"

    def test_bar_altitude_negative(self) -> None:
        """Отрицательная bar_altitude -> 0.0."""
        plane = Aircraft(id_aircraft="ID", callsign="CALL", origin_country="Country", bar_altitude=-100)
        assert plane.bar_altitude == 0.0

    def test_geo_altitude_fallback(self) -> None:
        """Если geo_altitude не передан, берётся bar_altitude."""
        plane = Aircraft(id_aircraft="ID", callsign="CALL", origin_country="Country", bar_altitude=5000)
        assert plane.geo_altitude == 5000

    def test_geo_altitude_negative(self) -> None:
        """Отрицательная geo_altitude -> bar_altitude."""
        plane = Aircraft(
            id_aircraft="ID", callsign="CALL", origin_country="Country", bar_altitude=5000, geo_altitude=-100
        )
        assert plane.geo_altitude == 5000


class TestAircraftDictConversion:
    """Тесты to_dict и from_dict."""

    def test_to_dict(self) -> None:
        plane = Aircraft(
            id_aircraft="ABC123",
            callsign="ABC123",
            origin_country="Russia",
            longitude=55.0,
            latitude=37.0,
            vertical_rate=10.5,
            velocity=250.3,
            geo_altitude=10000.0,
            true_track=180.0,
            squawk="1234",
            on_ground=False,
            bar_altitude=9500.0,
        )
        expected = {
            "id_aircraft": "ABC123",
            "callsign": "ABC123",
            "country": "Russia",
            "latitude": 37.0,
            "longitude": 55.0,
            "vertical_rate": 10.5,
            "velocity": 250.3,
            "altitude": 10000.0,
            "true_track": 180.0,
            "squawk": "1234",
            "on_ground": False,
            "bar_altitude": 9500.0,
        }
        assert plane.to_dict() == expected

    def test_from_dict(self) -> None:
        data = {
            "id_aircraft": "DEF456",
            "callsign": "DEF456",
            "country": "USA",
            "latitude": 40.0,
            "longitude": -80.0,
            "vertical_rate": 5.0,
            "velocity": 300.0,
            "altitude": 12000.0,
            "true_track": 90.0,
            "squawk": "5678",
            "on_ground": True,
            "bar_altitude": 11500.0,
        }
        plane = Aircraft.from_dict(data)
        assert plane.id_aircraft == "DEF456"
        assert plane.callsign == "DEF456"
        assert plane.origin_country == "USA"
        assert plane.latitude == 40.0
        assert plane.longitude == -80.0
        assert plane.vertical_rate == 5.0
        assert plane.velocity == 300.0
        assert plane.geo_altitude == 12000.0
        assert plane.true_track == 90.0
        assert plane.squawk == "5678"
        assert plane.on_ground is True
        assert plane.bar_altitude == 11500.0

    def test_from_dict_missing_keys(self) -> None:
        """Отсутствующие ключи заменяются значениями по умолчанию."""
        data = {"id_aircraft": "X", "callsign": "Y", "country": "Z"}
        plane = Aircraft.from_dict(data)
        assert plane.id_aircraft == "X"
        assert plane.callsign == "Y"
        assert plane.origin_country == "Z"
        assert plane.latitude == 0.0
        assert plane.longitude == 0.0
        assert plane.geo_altitude == 0.0
        assert plane.on_ground is False
        assert plane.squawk == "0000"


class TestAircraftComparison:
    """Тесты сравнения __eq__ и __lt__."""

    def test_eq_true(self) -> None:
        plane1 = Aircraft("A", "A", "RU", velocity=100, geo_altitude=5000)
        plane2 = Aircraft("B", "B", "US", velocity=100, geo_altitude=5000)
        assert plane1 == plane2

    def test_eq_false_different_velocity(self) -> None:
        plane1 = Aircraft("A", "A", "RU", velocity=100, geo_altitude=5000)
        plane2 = Aircraft("B", "B", "US", velocity=200, geo_altitude=5000)
        assert plane1 != plane2

    def test_eq_false_different_altitude(self) -> None:
        plane1 = Aircraft("A", "A", "RU", velocity=100, geo_altitude=5000)
        plane2 = Aircraft("B", "B", "US", velocity=100, geo_altitude=6000)
        assert plane1 != plane2

    def test_lt_true(self) -> None:
        plane1 = Aircraft("A", "A", "RU", velocity=100, geo_altitude=5000)
        plane2 = Aircraft("B", "B", "US", velocity=200, geo_altitude=5000)
        assert plane1 < plane2  # сначала сравнивается скорость

    def test_lt_false(self) -> None:
        plane1 = Aircraft("A", "A", "RU", velocity=200, geo_altitude=5000)
        plane2 = Aircraft("B", "B", "US", velocity=100, geo_altitude=5000)
        assert not (plane1 < plane2)

    def test_lt_altitude_second(self) -> None:
        """Если скорости равны, сравнивается geo_altitude."""
        plane1 = Aircraft("A", "A", "RU", velocity=100, geo_altitude=3000)
        plane2 = Aircraft("B", "B", "US", velocity=100, geo_altitude=5000)
        assert plane1 < plane2

    def test_lt_with_other_type(self) -> None:
        """Сравнение с объектом другого типа возвращает NotImplemented."""
        plane = Aircraft("A", "A", "RU")
        with pytest.raises(TypeError):
            plane < 123


class TestAircraftRepr:
    """Тест __repr__."""

    def test_repr(self) -> None:
        plane = Aircraft("ABC", "ABC", "Russia", latitude=37.0, longitude=55.0, velocity=250, geo_altitude=10000)
        repr_str = repr(plane)
        assert "Aircraft" in repr_str
        assert "id_aircraft='ABC'" in repr_str
        assert "callsign='ABC'" in repr_str
        assert "country='Russia'" in repr_str
        assert "lat=37.0" in repr_str
        assert "lon=55.0" in repr_str
        assert "vel=250" in repr_str
        assert "alt=10000" in repr_str


# from typing import Any, Dict
#
# import pytest
#
# from src.aircrafts import Aircraft
#
#
# class TestAircraft:
#     """Тесты для класса Aircraft."""
#
#     # Данные для корректного создания объекта
#     valid_data: Dict[str, Any] = {
#         "id_aircraft": "ABC123",
#         "callsign": "ABC123",
#         "origin_country": "Russia",
#         "longitude": 55.0,
#         "latitude": 37.0,
#         "vertical_rate": 10.5,
#         "velocity": 250.3,
#         "geo_altitude": 10000.0,
#         "true_track": 180.0,
#         "squawk": "1234",
#         "on_ground": False,
#         "bar_altitude": 9500.0,
#     }
#
#     @pytest.fixture
#     def aircraft(self) -> Aircraft:
#         """Фикстура с полностью заполненным объектом."""
#         return Aircraft(**self.valid_data)
#
#     def test_create_aircraft_valid(self) -> None:
#         """Создание объекта с корректными данными."""
#         a = Aircraft(**self.valid_data)
#         assert a.id_aircraft == "ABC123"
#         assert a.callsign == "ABC123"
#         assert a.origin_country == "Russia"
#         assert a.longitude == 55.0
#         assert a.latitude == 37.0
#         assert a.vertical_rate == 10.5
#         assert a.velocity == 250.3
#         assert a.geo_altitude == 10000.0
#         assert a.true_track == 180.0
#         assert a.squawk == "1234"
#         assert a.on_ground is False
#         assert a.bar_altitude == 9500.0  # ожидаем 9500, но из-за бага будет 0.0
#
#     def test_id_aircraft_invalid_type(self) -> None:
#         """id_aircraft должен быть строкой."""
#         with pytest.raises(ValueError, match=""):
#             Aircraft(
#                 id_aircraft=123,  # type: ignore[arg-type]
#                 callsign="ABC",
#                 origin_country="Russia",
#                 longitude=55,
#                 latitude=37,
#                 on_ground=False,
#             )
#
#     def test_callsign_invalid_type(self) -> None:
#         """callsign должен быть строкой."""
#         with pytest.raises(ValueError, match=""):
#             Aircraft(
#                 id_aircraft="ABC",
#                 callsign=123,  # type: ignore[arg-type]
#                 origin_country="Russia",
#                 longitude=55,
#                 latitude=37,
#                 on_ground=False,
#             )
#
#     def test_origin_country_empty_string(self) -> None:
#         """origin_country не должен быть пустой строкой."""
#         with pytest.raises(ValueError, match=""):
#             Aircraft(
#                 id_aircraft="ABC",
#                 callsign="ABC",
#                 origin_country="",
#                 longitude=55,
#                 latitude=37,
#                 on_ground=False,
#             )
#
#     def test_origin_country_not_string(self) -> None:
#         """origin_country должен быть строкой (текущая реализация ломается при не-строке)."""
#         # В текущей реализации, если передать не строку, вызовет AttributeError при origin_country.strip()
#         with pytest.raises((AttributeError, ValueError)):
#             Aircraft(
#                 id_aircraft="ABC",
#                 callsign="ABC",
#                 origin_country=123,  # type: ignore[arg-type]
#                 longitude=55,
#                 latitude=37,
#                 on_ground=False,
#             )
#
#     def test_longitude_out_of_range(self) -> None:
#         """longitude должен быть в [-180, 180]."""
#         with pytest.raises(ValueError, match="longitude должен быть числом в диапазоне"):
#             Aircraft(
#                 id_aircraft="ABC",
#                 callsign="ABC",
#                 origin_country="Russia",
#                 longitude=200,
#                 latitude=37,
#                 on_ground=False,
#             )
#
#     def test_latitude_out_of_range(self) -> None:
#         """latitude должен быть в [-90, 90]."""
#         with pytest.raises(ValueError, match="latitude должен быть числом в диапазоне"):
#             Aircraft(
#                 id_aircraft="ABC",
#                 callsign="ABC",
#                 origin_country="Russia",
#                 longitude=55,
#                 latitude=100,
#                 on_ground=False,
#             )
#
#     def test_true_track_out_of_range(self) -> None:
#         """true_track должен быть в [0, 359.99]."""
#         with pytest.raises(ValueError, match="true_track должен быть числом в диапазоне"):
#             Aircraft(
#                 id_aircraft="ABC",
#                 callsign="ABC",
#                 origin_country="Russia",
#                 longitude=55,
#                 latitude=37,
#                 true_track=400,
#                 on_ground=False,
#             )
#
#     def test_on_ground_invalid_type(self) -> None:
#         """on_ground должен быть bool."""
#         with pytest.raises(ValueError, match="on_ground должен быть True или False"):
#             Aircraft(
#                 id_aircraft="ABC",
#                 callsign="ABC",
#                 origin_country="Russia",
#                 longitude=55,
#                 latitude=37,
#                 on_ground="False",  # type: ignore[arg-type]
#             )
#
#     def test_default_values(self) -> None:
#         """Проверка значений по умолчанию для опциональных полей."""
#         a = Aircraft(
#             id_aircraft="ABC",
#             callsign="ABC",
#             origin_country="Russia",
#             longitude=55,
#             latitude=37,
#             on_ground=False,
#         )
#         assert a.vertical_rate == 0.0
#         assert a.velocity == 0.0
#         assert a.geo_altitude == 0.0
#         # Из-за бага в bar_altitude всегда 0.0, даже если None
#         assert a.bar_altitude == 0.0
#         # true_track: ожидаем None, но из-за ошибки в коде будет исключение
#         # В текущей реализации, если true_track не передан, его нет в kwargs, параметр получает None,
#         # и проверка isinstance(None, (int,float)) возвращает False, попадаем в else -> ValueError.
#         # Поэтому этот тест пока пропускаем или ожидаем ValueError.
#         # В корректной реализации должно быть значение по умолчанию.
#         assert a.squawk == "0000"
#
#     def test_squawk_default(self) -> None:
#         """Если squawk не передан, должен быть '0000'."""
#         a = Aircraft(
#             id_aircraft="ABC",
#             callsign="ABC",
#             origin_country="Russia",
#             longitude=55,
#             latitude=37,
#             on_ground=False,
#         )
#         assert a.squawk == "0000"
#
#     def test_squawk_invalid_type(self) -> None:
#         """Если squawk передан не строкой и не None, должно быть исключение (в текущей реализации не обработано)."""
#         # В текущей реализации, если передать число, squawk останется неопределённым -> AttributeError
#         with pytest.raises((AttributeError, ValueError)):
#             Aircraft(
#                 id_aircraft="ABC",
#                 callsign="ABC",
#                 origin_country="Russia",
#                 longitude=55,
#                 latitude=37,
#                 on_ground=False,
#                 squawk=1234,  # type: ignore[arg-type]
#             )
#
#     def test_eq_comparison(self, aircraft: Aircraft) -> None:
#         """Проверка равенства по скорости и высоте."""
#         a1 = Aircraft(**self.valid_data)
#         a2 = Aircraft(**self.valid_data)
#         assert a1 == a2
#
#         a3 = Aircraft(
#             id_aircraft="ABC",
#             callsign="ABC",
#             origin_country="Russia",
#             longitude=55,
#             latitude=37,
#             velocity=300,
#             geo_altitude=11000,
#             on_ground=False,
#         )
#         assert a1 != a3
#
#     def test_lt_comparison(self) -> None:
#         """Проверка оператора меньше."""
#         a1 = Aircraft(
#             id_aircraft="A",
#             callsign="A",
#             origin_country="R",
#             longitude=0,
#             latitude=0,
#             velocity=100,
#             geo_altitude=5000,
#             on_ground=False,
#         )
#         a2 = Aircraft(
#             id_aircraft="B",
#             callsign="B",
#             origin_country="R",
#             longitude=0,
#             latitude=0,
#             velocity=200,
#             geo_altitude=10000,
#             on_ground=False,
#         )
#         assert a1 < a2
#         assert not a2 < a1
#
#     def test_to_dict(self, aircraft: Aircraft) -> None:
#         """Преобразование в словарь."""
#         d = aircraft.to_dict()
#         expected = {
#             "id_aircraft": "ABC123",
#             "callsign": "ABC123",
#             "country": "Russia",
#             "latitude": 37.0,
#             "longitude": 55.0,
#             "vertical_rate": 10.5,
#             "velocity": 250.3,
#             "altitude": 10000.0,
#             "true_track": 180.0,
#             "squawk": "1234",
#             "on_ground": False,
#             "bar_altitude": 9500.0,
#         }
#         assert d == expected
#
#     def test_from_dict(self) -> None:
#         """Создание объекта из словаря."""
#         data = {
#             "id_aircraft": "ABC123",
#             "callsign": "ABC123",
#             "country": "Russia",
#             "latitude": 37.0,
#             "longitude": 55.0,
#             "vertical_rate": 10.5,
#             "velocity": 250.3,
#             "altitude": 10000.0,
#             "true_track": 180.0,
#             "squawk": "1234",
#             "on_ground": False,
#             "bar_altitude": 9500.0,  # дополнительное поле
#         }
#         a = Aircraft.from_dict(data)
#         assert a.id_aircraft == "ABC123"
#         assert a.callsign == "ABC123"
#         assert a.origin_country == "Russia"
#         assert a.latitude == 37.0
#         assert a.longitude == 55.0
#         assert a.vertical_rate == 10.5
#         assert a.velocity == 250.3
#         assert a.geo_altitude == 10000.0
#         assert a.true_track == 180.0
#         assert a.squawk == "1234"
#         assert a.on_ground is False
#         # bar_altitude из словаря передаётся, но в текущей реализации всегда 0.0
#         assert a.bar_altitude == 9500.0  # ожидаем 9500, но из-за бага будет 0.0
#
#     def test_repr(self, aircraft: Aircraft) -> None:
#         """Проверка строкового представления (не строго, лишь бы не падало)."""
#         repr_str = repr(aircraft)
#         assert "Aircraft" in repr_str
#         assert "ABC123" in repr_str
