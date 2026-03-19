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
        if user_input.isalpha(): # ('russia', 'rossia', 'russya')
            print(f"Вы ввели {user_input}")
            country_user.append(user_input)
        else:
            print("Вы ввели не название страны, попробуйте еще раз!")
    return country_user

def user_interaction():
    print(f"{hello_by_current_time()}")
    print(
        f"Добро пожаловать в программу, которая собирает данные о самолетах\n"
        f"в воздушных пространствах тех стран, которые вы выберете.\n"
        f"Пример стран из списка:"
    )
    countries = data_countries()
    user_country = country_for_coord(countries)
    client = NominatimClient()
    user_country_correct = [c for c in user_country if c.lower() not in (
        'russia', 'rossia', 'russya', 'rossya', 'rusiya', 'ru', 'rusia', 'rusland', 'rwasha'
    )]
    print(user_country)
    print(user_country_correct)
    coord = client.get_country_coordinates(user_country_correct)
    if user_country != user_country_correct:
        coord += [['41.1833333', '81.85', '19.6333333', '180.0'], ['41.1833333', '81.85', '-180.0', '-168.9833333']]
    # # [['41.1833333', '81.85', '19.6333333', '180.0'], ['41.1833333', '81.85', '-180.0', '-168.9833333']] Russia
    print(coord)
    aircrafts = OpenSkyClient().get_aircraft_in_bbox(coord)
    print(len(aircrafts))
    list_class_aircraft = []
    for i in aircrafts:
        try:
            plane = Aircraft(i[0], i[1], i[2], i[5], i[6], i[11], i[9], i[13], i[10], i[14], i[8], i[7])
            list_class_aircraft.append(plane)
        except Exception as e:
            print(f"Не удалось создать объект для {i[0]}: {e}")
    n = int(input("Введите количество самолетов для вывода в топ N: "))
    sorted_aircrafts = sorted(
        list_class_aircraft,
        key=lambda x: x.geo_altitude if x.geo_altitude is not None else float('inf'),
        reverse=True  # чтобы получить самые высокие
    )
    for aircraft in sorted_aircrafts[:n]:
        print(aircraft)
    return sorted_aircrafts


if __name__ == "__main__":
    planes = user_interaction()

    # Создаём несколько самолётов
    # a1 = planes[:100]
    # a2 = planes[30]
    # a3 = planes[50]

    # Работа с JSON-хранилищем
    # json_storage = JSONSaver("data/aircraft.json")
    # for u in planes:
    #     json_storage.add_aircraft(u)
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
    #
    # air_1 = planes[1]
    # air_2 = planes[3]
    # print(air_1)
    # print(air_2)
    # print(air_1 > air_2)
    # print(air_1 < air_2)
    # print(air_1 == air_2)

# 4, 5, 6, 13, 19, 20, 25, 27, 28, 30, 32, 33, 34, 38, 39, 40, 41, 42, 44, 48, 49,
# 51, 52, 55, 56, 58, 62, 66, 68, 70, 80, 82, 84, 86, 90, 93, 94, 97, 98, 99, 100,
# 101, 104, 105, 107, 108, 110, 111, 112, 114, 115, 120, 122, 123, 128, 129, 133, 134, 135, 138,
# 141, 144, 145, 148, 149, 150, 154, 155, 156, 159, 160, 162, 164, 165, 166, 167, 172, 175, 176, 177, 180,
# 182, 189, 190, 193, 194, 195

# info_aircrafts = [['4b1809', 'SWR8KY  ', 'Switzerland', 1773716158, 1773716158, 8.5586, 47.4535, None, True, 0, 5.62, None, None, None, None, False, 0], ['a4d881', 'N411GV  ', 'United States', 1773715893, 1773715893, -151.2473, 60.5653, None, True, 3.09, 25.31, None, None, None, '0525', False, 0], ['a7e8bf', 'ASA64   ', 'United States', 1773716162, 1773716162, -123.131, 48.3466, 5989.32, False, 203.29, 148.24, -11.7, None, 6118.86, None, False, 0], ['aa56b5', 'UAL263  ', 'United States', 1773716162, 1773716162, -78.8414, 42.9609, 1508.76, False, 148.43, 45.84, -3.25, None, 1272.54, '3134', False, 0], ['4b180c', 'SWR     ', 'Switzerland', 1773716157, 1773716159, 8.558, 47.4542, None, True, 0, 185.62, None, None, None, '2000', False, 0], ['a2cba6', 'TWY84   ', 'United States', 1773716162, 1773716162, -75.8422, 41.3163, 6393.18, False, 189.18, 110.7, -8.13, None, 6248.4, '1753', False, 0], ['ad4f72', 'JBU8052 ', 'United States', 1773716162, 1773716162, -70.9931, 42.3896, 243.84, False, 68.66, 199.25, -3.58, None, 99.06, '1033', False, 0], ['ae26ad', 'C6587   ', 'United States', 1773716089, 1773716089, -122.9362, 48.509, 144.78, False, 49.9, 180, -0.65, None, 129.54, None, False, 0], ['511171', 'MBU6146 ', 'Estonia', 1773716162, 1773716162, 20.3342, 43.2532, 10652.76, False, 225.6, 139.81, 0, None, 10561.32, '6022', False, 0], ['abb3be', 'DAL1    ', 'United States', 1773716161, 1773716162, -62.2803, 43.8363, 10058.4, False, 277.37, 66.38, 0, None, 10347.96, None, False, 0], ['4952a6', 'TAP238  ', 'Portugal', 1773715936, 1773715938, -111.1931, 42.7665, 11277.6, False, 239.82, 69.27, 0, None, 11643.36, None, False, 0], ['aae34c', 'EJA800  ', 'United States', 1773716162, 1773716162, -84.0987, 41.4531, 13106.4, False, 233.37, 273.03, -0.33, None, 12832.08, '3350', False, 0], ['3c6676', 'DLH1331 ', 'Germany', 1773716162, 1773716162, -2.3965, 42.4272, 10980.42, False, 221.6, 25.43, 0, None, 11170.92, '6441', False, 0], ['a39bfa', 'UAL1702 ', 'United States', 1773716162, 1773716162, -88.9444, 41.968, 9448.8, False, 248.48, 80.95, 0, None, 8907.78, None, False, 0], ['a35592', 'JBU860  ', 'United States', 1773716162, 1773716162, -70.928, 42.5237, 1097.28, False, 64.79, 200.45, -3.58, None, 960.12, '2674', False, 0], ['408142', 'DHK705  ', 'United Kingdom', 1773716162, 1773716162, -72.7412, 43.5351, 10363.2, False, 212.36, 256.27, 0.33, None, 10401.3, '0702', False, 0], ['a798b9', 'LBQ792  ', 'United States', 1773715945, 1773716112, -77.662, 43.1176, None, True, 0.77, 230.62, None, None, None, None, False, 0], ['a3556f', 'JBU247  ', 'United States', 1773716162, 1773716162, -106.4372, 43.0526, 10972.8, False, 227.29, 252.34, 0, None, 11201.4, '3260', False, 0], ['c01b6c', 'JZA52   ', 'Canada', 1773716162, 1773716162, -65.7813, 45.4364, 708.66, False, 67.7, 216.35, 0.33, None, 647.7, '6347', False, 0], ['a69b92', 'ASA2    ', 'United States', 1773716162, 1773716162, -89.7872, 42.0311, 11277.6, False, 254.66, 113.2, 0.33, None, 10850.88, None, False, 0], ['a04431', 'N116TL  ', 'United States', 1773716162, 1773716162, -149.9915, 61.2252, 487.68, False, 51.59, 343.19, -0.98, None, 281.94, None, False, 0], ['4b187b', 'SWR15X  ', 'Switzerland', 1773716162, 1773716162, -69.61, 41.7676, 10972.8, False, 272.06, 65.18, 0.33, None, 11193.78, '1716', False, 0], ['ade106', 'N9936V  ', 'United States', 1773716152, 1773716152, -121.198, 44.0752, 1165.86, False, 33.94, 194.04, 2.28, None, 1211.58, None, False, 0], ['accd69', 'DAL2377 ', 'United States', 1773716162, 1773716162, -106.2756, 41.8738, 10751.82, False, 224.18, 263.54, -4.88, None, 10980.42, '3171', False, 0], ['3c65ab', 'DLH773  ', 'Germany', 1773716162, 1773716162, 23.1606, 45.4784, 12192, False, 241.91, 292.64, 0, None, 12070.08, '3256', False, 0], ['4b1887', 'SWR9G   ', 'Switzerland', 1773716096, 1773716110, -83.3583, 45.5772, 10668, False, 264.07, 47.92, 0, None, 10195.56, None, False, 0], ['4b1881', 'SWR23A  ', 'Switzerland', 1773716141, 1773716161, -57.0105, 44.6537, 11887.2, False, 259.08, 74.8, 0, None, 12161.52, None, False, 0], ['3c65c4', 'DLH2559 ', 'Germany', 1773716162, 1773716162, 43.2415, 41.8856, 8442.96, False, 232.49, 273.68, 6.5, None, 8458.2, '6755', False, 0], ['a94b2e', 'UAL8117 ', 'United States', 1773716162, 1773716162, -105.365, 41.4672, 9144, False, 186.03, 331.24, 0, None, 9319.26, '3763', False, 0], ['a34291', 'UPS236  ', 'United States', 1773716162, 1773716162, 6.7544, 50.7084, 6736.08, False, 193.11, 288, 14.96, None, 6789.42, '4111', False, 0], ['a7c2cd', 'N6CP    ', 'United States', 1773716162, 1773716162, -7.9206, 50.0368, 12496.8, False, 280.5, 97.16, 0.65, None, 12573, None, False, 0], ['a38a05', 'N327TL  ', 'United States', 1773716162, 1773716162, -84.7886, 41.9215, 13716, False, 255.28, 84.57, -0.33, None, 13434.06, '1042', False, 0], ['a091d5', 'DAL567  ', 'United States', 1773716162, 1773716162, -78.5371, 42.3257, 9753.6, False, 252.42, 297.56, -0.33, None, 9494.52, '1524', False, 0], ['a808df', 'N617BG  ', 'United States', 1773716149, 1773716158, -122.2176, 47.4938, None, True, 0, 354.38, None, None, None, None, False, 0], ['a0311d', 'DAL1105 ', 'United States', 1773716162, 1773716162, -122.3079, 47.442, 228.6, False, 74.6, 179.21, 12.68, None, 228.6, None, False, 0], ['aa43c4', 'RPA3564 ', 'United States', 1773716162, 1773716162, -76.0301, 42.3922, 7940.04, False, 181.32, 121.66, -5.85, None, 7802.88, None, False, 0], ['0d0abf', 'VOI1850 ', 'Mexico', 1773716162, 1773716162, -122.7253, 46.4163, 7749.54, False, 210.48, 358.46, -13.33, None, 8016.24, '1317', False, 0], ['a58de0', 'UAL457T ', 'United States', 1773716161, 1773716161, -95.8531, 41.2579, 518.16, False, 63.81, 324.52, -3.9, None, 556.26, None, False, 0], ['c03517', 'WJA2153 ', 'Canada', 1773716162, 1773716162, -122.0842, 47.3421, 10972.8, False, 212.54, 347.28, 0, None, 11285.22, '6630', False, 0], ['a4c4bb', 'UPS991  ', 'United States', 1773716162, 1773716162, -117.8479, 46.0277, 11087.1, False, 252.46, 183.15, 8.13, None, 11445.24, None, False, 0], ['a00929', 'RPA4336 ', 'United States', 1773716162, 1773716162, -86.7609, 42.1235, 6339.84, False, 199.33, 87.19, 9.1, None, 5897.88, None, False, 0], ['ad072a', 'DAL1620 ', 'United States', 1773716162, 1773716162, -83.2616, 42.2186, 609.6, False, 57.1, 270, -3.9, None, 480.06, None, False, 0], ['accd09', 'N924AC  ', 'United States', 1773716161, 1773716162, -150.0594, 60.9774, 1036.32, False, 90.34, 37.13, -1.95, None, 777.24, None, False, 0], ['a70aa1', 'ASA552  ', 'United States', 1773716162, 1773716162, -122.6869, 46.1403, 7993.38, False, 199.42, 352.14, -9.75, None, 8267.7, '1355', False, 0], ['86d5c3', 'APJ567  ', 'Japan', 1773716162, 1773716162, 141.3934, 42.0026, 3352.8, False, 155.29, 26.57, -7.8, None, 3307.08, '2043', False, 0], ['495305', 'TAP211  ', 'Portugal', 1773716162, 1773716162, -72.5011, 41.9582, 5059.68, False, 168.46, 262.98, 0, None, 5013.96, None, False, 0]]

