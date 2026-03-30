from datetime import datetime

from data.data_countries import data_countries
from src.aircrafts import Aircraft
from src.json_saver import JSONSaver
from src.nominatim import NominatimClient
from src.openSky_network import OpenSkyClient


def hello_by_current_time() -> str:
    """Функция, которая формирует приветственное сообщение в зависимости от фактического времени суток."""
    now_hour = datetime.now().hour
    if 6 <= now_hour < 12:
        hello_message = "Доброе утро!"
    elif 12 <= now_hour < 18:
        hello_message = "Добрый день!"
    elif 18 <= now_hour <= 23:
        hello_message = "Добрый вечер!"
    else:
        hello_message = "Доброй ночи!"
    return hello_message

def country_for_coord(countries):
    for i in range(0, len(countries), 9):
        print(countries[i : (9 + i)])
    country_user = []
    while True:
        print("Для прекращения ввода введите цифру 0")
        user_input = input("Введите название страны: ")
        if user_input == "0":
            break
        if user_input.isalpha() or user_input in (
                'Russian Federation',
                'United Kingdom',
                'United States',
                'Viet Nam',
                'Republic of Moldova',
                'Dominican Republic', 
                'Kingdom of the Netherlands', 
                'Republic of Korea', 
                'Saudi Arabia', 
                'Trinidad and Tobago',
                'South Africa',
                'Brunei Darussalam',
                'San Marino',
                'United Arab Emirates',
                'New Zealand',
                'Libyan Arab Jamahiriya',
                'Saint Vincent and the Grenadines',
                'Czech Republic',
                "Lao People's Democratic Republic",
                'Sri Lanka'
        ):
            print(f"Вы ввели {user_input}")
            country_user.append(user_input)
        else:
            print("Вы ввели не название страны, попробуйте еще раз!")
    return country_user

def sort_aircraft_by_altitude(list_aircraft, sort_altitude):
    if sort_altitude == 'y':
        sort_reverse = False
    else:
        sort_reverse = True
    sorted_planes = sorted(
        list_aircraft,
        key=lambda x: x.geo_altitude if x.geo_altitude is not None else float('inf'),
        reverse=sort_reverse
    )
    return sorted_planes

def filter_aeroplanes_by_country(aeroplanes, filter_words):
    filtered = [plane for plane in aeroplanes if plane.origin_country in filter_words]
    return filtered

def filter_aeroplanes_altitude(aeroplanes):
    # Запрашиваем диапазон высот (например, "1000-5000" или "1000 5000")
    range_input = input("Введите диапазон высот полета (нижняя-верхняя через дефис или пробел): ")
    # Разбиваем ввод по дефису или пробелу
    if '-' in range_input:
        parts = range_input.split('-')
    else:
        parts = range_input.split()
    # Проверяем, что получили два значения
    if len(parts) == 2:
        try:
            low_alt = float(parts[0].strip())
            high_alt = float(parts[1].strip())
            altitude_range = (low_alt, high_alt)  # кортеж или список [low, high]
        except ValueError:
            print("Некорректный ввод. Используйте числа.")
            altitude_range = [0.0, 20000]
    else:
        print("Некорректный ввод. Нужно ввести два числа через дефис или пробел.")
        altitude_range = [0.0, 20000]
    # altitude_range = list(map(float, input("Введите диапазон высот (Пример: 10000-15000): ").split('-')))
    filtered = [plane for plane in aeroplanes if altitude_range[0] <= plane.geo_altitude <= altitude_range[1]]
    return filtered

def user_interaction():
    print(f"{hello_by_current_time()}")
    print(
        f"Добро пожаловать в программу, которая собирает данные о самолетах\n"
        f"в воздушных пространствах тех стран, которые вы выберете.\n"
        f"Пример стран из списка:"
    )
    countries = data_countries()
    user_country = country_for_coord(countries)
    user_country_correct = [c for c in user_country if c.lower() not in (
        'russia', 'rossia', 'russya', 'rossya', 'rusiya', 'ru', 'rus', 'rusia', 'rusland', 'rwasha'
    )]
    coord = NominatimClient().get_country_coordinates(user_country_correct)
    if user_country != user_country_correct:
        coord += [['41.1833333', '81.85', '19.6333333', '180.0'], ['41.1833333', '81.85', '-180.0', '-168.9833333']]
    # # [['41.1833333', '81.85', '19.6333333', '180.0'], ['41.1833333', '81.85', '-180.0', '-168.9833333']] Russia
    print(coord)
    aircrafts = OpenSkyClient().get_aircraft_in_bbox(coord)
    print(f'Над {user_country} находится {len(aircrafts)} самолетов.')
    if len(aircrafts) == 0:
        print("Проверьте соединение с интернетом и запустите программу!")
    list_class_aircraft = []
    for i in aircrafts:
        try:
            plane = Aircraft(i[0], i[1], i[2], i[5], i[6], i[11], i[9], i[13], i[10], i[14], i[8], i[7])
            list_class_aircraft.append(plane)
        except Exception as e:
            print(f"Не удалось создать объект под номером {i}: {e}")
    n = int(input("Введите количество самолетов для вывода в топ N: "))
    sort_altitude = input("Вам необходима сортировка самолетов от минимальной высоты и выше?: y/n ").lower()
    sorted_aircraft = sort_aircraft_by_altitude(list_class_aircraft, sort_altitude)
    for aircraft in sorted_aircraft[:n]:
        print(aircraft)
    unique_countries_tuple = tuple({plane.origin_country for plane in sorted_aircraft})
    print('Для сортировки самолетов по стране регистрации скопируйте страну из списка: ')
    for c in range(0, len(unique_countries_tuple), 9):
        print(unique_countries_tuple[c : (9 + c)])
    filter_words = country_for_coord([])
    filtered_aeroplanes = filter_aeroplanes_by_country(sorted_aircraft, filter_words)
    print(f'Получилось {len(filtered_aeroplanes)} самолетов по стране регистрации')
    for i in filtered_aeroplanes[:n]:
        print(i)
    filtered_aeroplanes_alt = filter_aeroplanes_altitude(sorted_aircraft)
    print(f'Получилось {len(filtered_aeroplanes_alt)} самолетов в диапазоне выбранных высот')
    for r in filtered_aeroplanes_alt[:n]:
        print(r)
    return filtered_aeroplanes_alt


if __name__ == "__main__":
    planes = user_interaction()

    # Работа с JSON-хранилищем
    timestamp = datetime.now().strftime("%Y%m%d")
    json_storage = JSONSaver(f"data/aircraft_{timestamp}.json")
    for u in planes:
        json_storage.add_aircraft(u)
    # json_storage.add_aircraft(a2)
    # json_storage.add_aircraft(a3)

    # Получение всех самолётов
    # all_aircraft = json_storage.get_aircraft()
    # print("Все самолёты:", all_aircraft)

    # # Получение самолётов из Ирландии
    # canada = json_storage.get_aircraft({"country": "United States"})
    # print("Самолёты из Канады:", canada)
    #
    # # Удаление самолёта из Швеции
    # json_storage.delete_aircraft({"country": "Armenia"})
    #
    # # Проверка после удаления
    # after_delete = json_storage.get_aircraft()
    # print("После удаления Канады:", after_delete)
    # planes = user_interaction()
    ## Создаём несколько самолётов

    # air_1 = planes[1]
    # air_2 = planes[3]
    # print(air_1)
    # print(air_2)
    # print(air_1 > air_2)
    # print(air_1 < air_2)
    # print(air_1 == air_2)
