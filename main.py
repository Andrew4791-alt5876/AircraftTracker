from src.info_aircrafts_over_country import OpenSkyNominatimClient

if __name__ == "__main__":
    client = OpenSkyNominatimClient()

    country = "Canada"
    coords = client.get_country_coordinates(country)
    if coords:
        print(f"Координаты {country}: {coords}")
        aircraft = client.get_aircraft_in_area(
            min_lat=coords["min_lat"], max_lat=coords["max_lat"], min_lon=coords["min_lon"], max_lon=coords["max_lon"]
        )
        print(f"Найдено самолётов в воздушном пространстве {country}: {len(aircraft)}")
        if aircraft:
            # Выведем первые 3 для примера
            for i, plane in enumerate(aircraft[:10]):
                print(f"Самолёт {i + 1}: {plane.get('callsign')} ({plane.get('origin_country')})")
    else:
        print("Не удалось получить координаты страны.")
