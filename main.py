from datetime import datetime

from data.data_countries import data_countries
from src.aircrafts import Aircraft
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


def user_interaction():
    print(f"{hello_by_current_time()}")
    print(
        f"Добро пожаловать в программу, которая собирает данные о самолетах\n"
        f"в воздушных пространствах тех стран, которые вы выберете.\n"
        f"Пример стран из списка:"
    )
    countries = data_countries()
    for i in range(0, len(countries), 9):
        print(countries[i : (9 + i)])
    country_user = []
    number = 0
    while number != "0":
        print("Для прекращения ввода введите цифру 0")
        number = input("Введите название страны: ")
        if number.isalpha() and number != "0":
            print(f"Вы ввели {number}")
            country_user.append(number)
        else:
            if number == "0":
                pass
            else:
                print("Вы ввели не число, попробуйте еще раз!")
    client = NominatimClient()
    coord = client.get_country_coordinates(country_user)
    # [['50.6765597', '75.3362128', '30.0027500', '180.00']] Russia
    print(coord)
    aircrafts = OpenSkyClient().get_aircraft_in_bbox(coord)
    print(len(aircrafts))
    list_class_aircraft = []
    for raw in aircrafts:
        try:
            plane = Aircraft(raw[0], raw[1], raw[2], raw[5], raw[6], raw[7], raw[8], raw[9], raw[10], raw[11], raw[13])
            list_class_aircraft.append(plane)
        except Exception as e:
            print(f"Не удалось создать объект для {raw[0]}: {e}")
    n = int(input("Введите количество самолетов для вывода в топ N: "))
    sorted_aircrafts = sorted(
        list_class_aircraft,
        key=lambda x: x.geo_altitude if x.geo_altitude is not None else float('int'),
        reverse=True  # чтобы получить самые высокие
    )
    for aircraft in sorted_aircrafts[:n]:
        print(aircraft)
    return sorted_aircrafts


if __name__ == "__main__":
    planes = user_interaction()

    # air_1 = planes[2]
    # air_2 = planes[5]
    # print(air_1)
    # print(air_2)
    # print(air_1 > air_2)
    # print(air_1 < air_2)
    # print(air_1 == air_2)

    # print(info_aircrafts)
    # print(i)
# 4, 5, 6, 13, 19, 20, 25, 27, 28, 30, 32, 33, 34, 38, 39, 40, 41, 42, 44, 48, 49,
# 51, 52, 55, 56, 58, 62, 66, 68, 70, 80, 82, 84, 86, 90, 93, 94, 97, 98, 99, 100,
# 101, 104, 105, 107, 108, 110, 111, 112, 114, 115, 120, 122, 123, 128, 129, 133, 134, 135, 138,
# 141, 144, 145, 148, 149, 150, 154, 155, 156, 159, 160, 162, 164, 165, 166, 167, 172, 175, 176, 177, 180,
# 182, 189, 190, 193, 194, 195


# from src.base_api import APIAdapter
#
# if __name__ == "__main__":
#     api = APIAdapter()
#     airplanes = api.get_aeroplanes(['Iran'])
#     for i in airplanes['states']:
#         print(i)
# user_interaction()


# afl_1 = Aircraft('gyg', 'afl1234', 'Russia', 123.67, 34.98, 5657.89, False, 887, 34.6, 12.23, 5800)
# afl_2 = Aircraft('r45', 'afl4321', 'Canada', 12.67, 134.98, 8657.89, False, 687, 178.8, 22.23, 8800)
# data_list_of_dict = [
#     {
#         'icao24': '461f9b', 'callsign': 'FIN576  ', 'origin_country': 'Finland',
#         'time_position': 1773249978, 'last_contact': 1773251363, 'longitude': 25.2791,
#         'latitude': 63.0449, 'baro_altitude': 11269.98, 'on_ground': False, 'velocity': 342.09,
#         'true_track': 183.1, 'vertical_rate': 0, 'sensors': None, 'geo_altitude': 11041.38,
#         'squawk': '0212', 'spi': False, 'position_source': 0
#     }, {
#         'icao24': '040102', 'callsign': 'ETH575  ', 'origin_country': 'Ethiopia',
#         'time_position': 1773251309, 'last_contact': 1773251321, 'longitude': -67.2032,
#         'latitude': 49.0149, 'baro_altitude': None, 'on_ground': True, 'velocity': 307.97,
#         'true_track': 73.5, 'vertical_rate': -0.33, 'sensors': None, 'geo_altitude': None,
#         'squawk': '2152', 'spi': False, 'position_source': 0
#     }, {
#         'icao24': 'ab7fe6', 'callsign': 'AAL176  ', 'origin_country': 'United States',
#         'time_position': 1773251363, 'last_contact': 1773251363, 'longitude': -118.5264,
#         'latitude': 44.7039, 'baro_altitude': 11269.98, 'on_ground': False, 'velocity': 307.24,
#         'true_track': 112.44, 'vertical_rate': -0.33, 'sensors': None, 'geo_altitude': 11308.08,
#         'squawk': '1441', 'spi': False, 'position_source': 0
#     }, {'icao24': 'a2a3af', 'callsign': 'UAL6    ', 'origin_country': 'United States',
#         'time_position': 1773251363, 'last_contact': 1773251363, 'longitude': -117.3252,
#         'latitude': 44.6882, 'baro_altitude': 11277.6, 'on_ground': False, 'velocity': 306.77,
#         'true_track': 113.94, 'vertical_rate': 0, 'sensors': None, 'geo_altitude': 11292.84,
#         'squawk': '1436', 'spi': False, 'position_source': 0
#         }
# ]
#
# client = OpenSkyNominatimClient()
# country = "Russia"
# coords = client.get_country_coordinates(country)
# aircraft = client.get_aircraft_in_area(min_lat=coords["min_lat"], max_lat=coords["max_lat"], min_lon=coords["min_lon"], max_lon=coords["max_lon"])
# print(len(aircraft))
# print(aircraft[90:100])
# print(aircraft[20])
# print(Aircraft.from_dict(aircraft[200]))
# print(data_list_of_dict[2] > data_list_of_dict[3])
# print(aircraft[10] < aircraft[20])

# ['ae1fa6', 'TALON57 ', 'United States', 1773715752, 1773715763, -116.1679, 43.5227, 967.74, False, 26.84, 347.83, 0, None, 1036.32, None, False, 0]
# ['a7e8bf', 'ASA64   ', 'United States', 1773715961, 1773715961, -123.436, 48.6761, 8374.38, False, 226.96, 147.97, -12.03, None, 8572.5, None, False, 0]
# ['aa56b5', 'UAL263  ', 'United States', 1773715961, 1773715961, -79.1391, 42.7863, 2316.48, False, 160.69, 51.37, -5.2, None, 2034.54, '3134', False, 0]
# ['ad4f72', 'JBU8052 ', 'United States', 1773715961, 1773715961, -70.9373, 42.5046, 975.36, False, 64.92, 199.44, -3.58, None, 838.2, '1033', False, 0]
# ['ae26ad', 'C6587   ', 'United States', 1773715949, 1773715949, -122.9048, 48.5633, 213.36, False, 48.77, 226.71, -0.98, None, 205.74, None, False, 0]
# ['abb3be', 'DAL1    ', 'United States', 1773715961, 1773715961, -62.9108, 43.6336, 10058.4, False, 277.94, 65.85, 0, None, 10347.96, None, False, 0]
# ['4952a6', 'TAP238  ', 'Portugal', 1773715936, 1773715938, -111.1931, 42.7665, 11277.6, False, 239.82, 69.27, 0, None, 11643.36, None, False, 0]
# ['a39bfa', 'UAL1702 ', 'United States', 1773715961, 1773715961, -89.5362, 41.896, 9448.8, False, 247.72, 80.56, 0, None, 8915.4, None, False, 0]
# ['a35592', 'JBU860  ', 'United States', 1773715961, 1773715961, -70.8687, 42.637, 1341.12, False, 74.3, 222.19, 0, None, 1203.96, '2674', False, 0]
# ['408142', 'DHK705  ', 'United Kingdom', 1773715961, 1773715961, -72.2262, 43.626, 10363.2, False, 212.62, 256.57, 0, None, 10424.16, '0702', False, 0]
# ['a798b9', 'LBQ792  ', 'United States', 1773715945, 1773715945, -77.662, 43.1176, None, True, 0.77, 230.62, None, None, None, None, False, 0]
# ['a3556f', 'JBU247  ', 'United States', 1773715961, 1773715961, -105.9045, 43.1545, 10972.8, False, 221.75, 257, 0.33, None, 11178.54, '3260', False, 0]
# ['c01b6c', 'JZA52   ', 'Canada', 1773715960, 1773715960, -65.9389, 45.4914, 1059.18, False, 136.84, 72.72, 0.98, None, 1005.84, '6347', False, 0]
# ['a69b92', 'ASA2    ', 'United States', 1773715961, 1773715961, -90.3584, 42.2124, 11277.6, False, 255.68, 112.85, -0.33, None, 10858.5, None, False, 0]
# ['accd69', 'DAL2377 ', 'United States', 1773715961, 1773715961, -105.7387, 41.9177, 10972.8, False, 225.09, 263.83, 0, None, 11186.16, '3171', False, 0]
# ['4b1887', 'SWR9G   ', 'Switzerland', 1773715960, 1773715960, -83.7024, 45.3568, 10668, False, 268.36, 47.56, 0.33, None, 10195.56, None, False, 0]
# ['4b1881', 'SWR23A  ', 'Switzerland', 1773715897, 1773715900, -57.7782, 44.5022, 11887.2, False, 260.75, 74.32, 0, None, 12161.52, None, False, 0]
# ['a38a05', 'N327TL  ', 'United States', 1773715961, 1773715961, -85.4075, 41.8752, 13716, False, 256.51, 84.13, 0.33, None, 13434.06, '1042', False, 0]
# ['a091d5', 'DAL567  ', 'United States', 1773715961, 1773715961, -77.9923, 42.1685, 9753.6, False, 234.97, 289.7, 0, None, 9540.24, '1524', False, 0]
# ['aa43c4', 'RPA3564 ', 'United States', 1773715961, 1773715961, -76.4095, 42.564, 9022.08, False, 184.93, 121.35, -5.2, None, 8884.92, None, False, 0]
# ['0d0abf', 'VOI1850 ', 'Mexico', 1773715961, 1773715961, -122.6626, 46.0355, 10248.9, False, 216.68, 350.16, -12.35, None, 10622.28, '1317', False, 0]
# ['c03517', 'WJA2153 ', 'Canada', 1773715961, 1773715961, -121.961, 46.9686, 10972.8, False, 212.93, 347.44, 0, None, 11308.08, '6630', False, 0]
# ['a4c4bb', 'UPS991  ', 'United States', 1773715961, 1773715961, -117.8116, 46.4919, 9037.32, False, 256.57, 183.1, 9.43, None, 9319.26, None, False, 0]
# ['a00929', 'RPA4336 ', 'United States', 1773715961, 1773715961, -87.2213, 42.1206, 4709.16, False, 182.57, 94.04, 9.43, None, 4351.02, None, False, 0]
# ['ad072a', 'DAL1620 ', 'United States', 1773715962, 1773715962, -83.1021, 42.2206, 1013.46, False, 75.14, 271.57, 0.33, None, 845.82, None, False, 0]
# ['a70aa1', 'ASA552  ', 'United States', 1773715961, 1773715961, -122.5978, 45.776, 10157.46, False, 210.17, 350.56, -11.7, None, 10530.84, '1355', False, 0]
# ['495305', 'TAP211  ', 'Portugal', 1773715961, 1773715961, -72.0962, 41.9938, 5920.74, False, 177.65, 263.35, -5.2, None, 5920.74, None, False, 0]
# ['495308', 'TAP203  ', 'Portugal', 1773715961, 1773715961, -72.3468, 41.9616, 5364.48, False, 169.82, 265.31, -5.53, None, 5341.62, None, False, 0]
# ['a33afa', 'SKW4100 ', 'United States', 1773715961, 1773715961, -122.6494, 46.8608, 4914.9, False, 201.34, 38.57, -7.15, None, 5044.44, None, False, 0]
# ['a15186', 'N184WK  ', 'United States', 1773715746, 1773715746, -88.3112, 42.6924, 327.66, False, 32.49, 113.32, -3.25, None, 297.18, None, False, 0]
# ['a99a3d', 'SKW4291 ', 'United States', 1773715961, 1773715961, -93.535, 45.7969, 4831.08, False, 160.25, 331.21, 0, None, 4495.8, None, False, 0]
# ['a8f77c', 'UAL904  ', 'United States', 1773715684, 1773715961, -66.2874, 43.4757, 10675.62, False, 272.18, 58.68, 0, None, 10911.84, '1577', False, 0]
# ['a76154', 'DAL697  ', 'United States', 1773715961, 1773715961, -82.5114, 44.972, 10058.4, False, 241.8, 89.39, 0, None, 9593.58, '3123', False, 0]
# ['a8a7eb', 'NDU57   ', 'United States', 1773715961, 1773715961, -96.3148, 46.5349, 1905, False, 51.08, 341.2, -0.33, None, 1783.08, None, False, 0]
# ['c07c7a', 'ACA543  ', 'Canada', 1773715961, 1773715961, -95.8082, 48.8013, 10363.2, False, 198.27, 274.91, 0, None, 9997.44, None, False, 0]
# ['3c6713', 'DLH461  ', 'Germany', 1773715961, 1773715961, -67.4011, 44.1837, 12496.8, False, 287.07, 50.89, 0, None, 12649.2, '1331', False, 0]
# ['3c6719', 'DLH413  ', 'Germany', 1773715962, 1773715962, -71.2072, 42.3267, 10043.16, False, 298.96, 54.31, 5.85, None, 10172.7, '7565', False, 0]
# ['a9b4a4', 'RPA3538 ', 'United States', 1773715960, 1773715961, -87.9555, 41.9858, 754.38, False, 83.66, 305.74, 5.2, None, 678.18, None, False, 0]
# ['a21c4c', 'ENY3873 ', 'United States', 1773715817, 1773715817, -87.9087, 41.9825, None, True, 7.72, 67.5, None, None, None, None, False, 0]
# ['aa91b6', 'NDU80T  ', 'United States', 1773715958, 1773715958, -95.5711, 47.1788, 1752.6, False, 76.45, 317.18, -0.98, None, 1615.44, None, False, 0]
# ['3c670d', 'DLH425  ', 'Germany', 1773715961, 1773715961, -63.9704, 45.9282, 11887.2, False, 283.37, 55.88, 0, None, 12077.7, '1466', False, 0]
# ['3c670c', 'DLH4W   ', 'Germany', 1773715960, 1773715961, -65.8352, 45.0171, 12496.8, False, 282.51, 54.49, 0, None, 12656.82, '3511', False, 0]
# ['aa9de7', 'RPA3492 ', 'United States', 1773715961, 1773715961, -87.912, 41.9704, None, True, 7.72, 90, None, None, None, '5751', False, 0]
# ['a27cb4', 'N26AR   ', 'United States', 1773715961, 1773715961, -97.4043, 43.5274, 3398.52, False, 133.77, 89.12, -8.78, None, 3246.12, None, False, 0]
# ['c08537', 'ACA1298 ', 'Canada', 1773715901, 1773715901, -79.6126, 43.6798, None, True, 0.06, 53.44, None, None, None, None, False, 0]
# ['c02ee9', 'ACA880  ', 'Canada', 1773715961, 1773715961, -77.5941, 44.1605, 9128.76, False, 273.86, 66.18, 3.58, None, 8884.92, None, False, 0]
# ['ab4ae9', 'AAL70   ', 'United States', 1773715961, 1773715961, -78.6834, 47.3253, 11277.6, False, 291.1, 67.56, 0.33, None, 10995.66, '2207', False, 0]
# ['c02eb9', 'ACA345  ', 'Canada', 1773715953, 1773715953, -123.1852, 49.2, None, True, 4.37, 174.38, None, None, None, None, False, 0]
# ['ad42db', 'N9535H  ', 'United States', 1773715961, 1773715961, -122.9345, 45.2872, 716.28, False, 30.87, 233.13, 0, None, 754.38, None, False, 0]
# ['a45091', 'DAL2442 ', 'United States', 1773715961, 1773715961, -119.221, 45.8655, 10363.2, False, 199.71, 310.09, 0, None, 10721.34, None, False, 0]
# ['c01040', 'ACA125  ', 'Canada', 1773715961, 1773715961, -92.1128, 48.6677, 12184.38, False, 243.68, 282.19, 0, None, 11803.38, None, False, 0]
# ['ad8b61', 'LYM5112 ', 'United States', 1773715961, 1773715961, -94.9763, 47.1447, 7437.12, False, 257.93, 135.73, 5.2, None, 7101.84, None, False, 0]
# ['a2c0ff', 'FDX1216 ', 'United States', 1773715958, 1773715958, -108.7713, 43.0618, 11277.6, False, 279.3, 116.47, 0.33, None, 11597.64, None, False, 0]
# ['4aca66', 'SAS944  ', 'Sweden', 1773715961, 1773715961, -83.8507, 45.6497, 11887.2, False, 277.27, 40.64, 0, None, 11468.1, None, False, 0]
# ['a8e3a8', 'FDX1382 ', 'United States', 1773715961, 1773715961, -96.272, 42.9097, 6941.82, False, 271.95, 148.14, 11.7, None, 6720.84, '5157', False, 0]
# ['c02f6a', '', 'Canada', 1773715929, 1773715929, -79.6226, 43.6799, None, True, 7.46, 137.81, None, None, None, None, False, 0]
# ['a0dbf4', 'N1544E  ', 'United States', 1773715781, 1773715781, -106.5074, 43.1475, 2613.66, False, 52.99, 0.56, -1.63, None, 2598.42, None, False, 0]
# ['c01c52', 'ACA50   ', 'Canada', 1773715959, 1773715961, -62.7209, 47.5565, 10668, False, 288.14, 78.57, 0.33, None, 10843.26, '0605', False, 0]
# ['a1c868', 'ASA649  ', 'United States', 1773715961, 1773715961, -122.6326, 45.2606, 2034.54, False, 144.72, 27.29, -6.5, None, 2103.12, '2743', False, 0]
# ['ab5db8', 'SCX218  ', 'United States', 1773715961, 1773715961, -92.5751, 42.4099, 9753.6, False, 193.97, 334.39, 0, None, 9357.36, '6617', False, 0]
# ['a83f8c', 'UPS99   ', 'United States', 1773715961, 1773715961, -104.8464, 50.6385, 10058.4, False, 312.3, 131.59, 0, None, 10027.92, '4170', False, 0]
# ['a16550', 'N1896L  ', 'United States', 1773715961, 1773715961, -123.0625, 48.0724, 1066.8, False, 96.96, 105.07, -0.65, None, 1028.7, None, False, 0]
# ['aa2abc', 'N754UW  ', 'United States', 1773715960, 1773715960, -87.9025, 41.9714, None, True, 1.54, 270, None, None, None, None, False, 0]
# ['c0101c', 'MBK811  ', 'Canada', 1773715961, 1773715961, -71.42, 46.8715, 3124.2, False, 106.96, 225.78, -5.85, None, 2964.18, None, False, 0]
# ['ad4eb3', 'ALFT    ', 'United States', 1773715960, 1773715960, -121.7477, 47.4785, 845.82, False, 63.51, 305.11, 0, None, 853.44, None, False, 0]
# ['ac9850', 'SKW404X ', 'United States', 1773715927, 1773715928, -87.9149, 41.973, None, True, 4.89, 345.94, None, None, None, None, False, 0]
# ['aa2b21', 'RPA3623 ', 'United States', 1773715961, 1773715961, -84.4724, 42.4225, 9144, False, 228.47, 296.05, -0.33, None, 8587.74, '2726', False, 0]
# ['c01c28', 'WJA616  ', 'Canada', 1773715961, 1773715961, -89.2391, 48.453, 10668, False, 245.3, 103.83, 0.33, None, 10142.22, None, False, 0]
# ['adb8b5', 'N9830V  ', 'United States', 1773715958, 1773715960, -121.1589, 43.991, 1905, False, 37.27, 173.66, 2.93, None, 1996.44, None, False, 0]
# ['c07193', 'WJA382  ', 'Canada', 1773715941, 1773715954, -88.3389, 48.3789, 12496.8, False, 248.92, 120.01, 0, None, 12077.7, None, False, 0]
# ['769104', 'SIA7430 ', 'Singapore', 1773715961, 1773715961, -97.1381, 47.9214, 10668, False, 295.29, 132.53, 0, None, 10370.82, None, False, 0]
# ['3c4ad9', 'DLH441  ', 'Germany', 1773715690, 1773715761, -65.2628, 50.2004, 11277.6, False, 302.16, 62.08, 0, None, 11285.22, '5662', False, 0]
# ['3c64f3', 'DLH447  ', 'Germany', 1773715961, 1773715961, -97.0056, 42.6373, 10058.4, False, 230.3, 63.03, 0, None, 9852.66, '1611', False, 0]
# ['a52e54', 'ASA427  ', 'United States', 1773715961, 1773715961, -122.1011, 42.8968, 10363.2, False, 226.27, 339.5, 0, None, 10843.26, '3141', False, 0]
# ['a0dd44', 'FDX1205 ', 'United States', 1773715779, 1773715956, -87.8906, 41.9718, None, True, 36.01, 5.62, None, None, None, None, False, 0]
# ['44a10f', 'OOHHO   ', 'Belgium', 1773715961, 1773715961, -78.3007, 44.7505, 13106.4, False, 225.65, 245.77, 0, None, 12885.42, '0704', False, 0]
# ['aa92f9', 'UAL23   ', 'United States', 1773715956, 1773715956, -62.5127, 46.6001, 10972.8, False, 283.67, 56.92, 0, None, 11178.54, '1714', False, 0]
# ['c06a80', 'TSC122  ', 'Canada', 1773715696, 1773715696, -79.6227, 43.6732, None, True, 3.34, 210.94, None, None, None, None, False, 0]
# ['a7888c', 'ASA237  ', 'United States', 1773715775, 1773715775, -128.3346, 41.7668, 10363.2, False, 199.91, 216.84, 0, None, 10805.16, None, False, 0]
# ['aa589c', 'JBU1462 ', 'United States', 1773715951, 1773715959, -71.0131, 42.3659, None, True, 0, 286.88, None, None, None, None, False, 0]
# ['c0712e', 'WJA1025 ', 'Canada', 1773715961, 1773715961, -117.7501, 47.402, 11582.4, False, 225.93, 27.09, -0.33, None, 11910.06, None, False, 0]
# ['a4771b', 'UPS473  ', 'United States', 1773715961, 1773715961, -79.9453, 41.7258, 9761.22, False, 194.26, 232.86, 0, None, 9418.32, '1043', False, 0]
# ['aa3226', 'AAL1572 ', 'United States', 1773715960, 1773715960, -79.6479, 43.6853, 320.04, False, 71.67, 225.87, 0.65, None, 137.16, None, False, 0]
# ['a2efec', 'FDX1358 ', 'United States', 1773715961, 1773715961, -91.3112, 43.6566, 10668, False, 278.29, 129.9, 0.33, None, 10226.04, None, False, 0]
# ['c07b05', 'ACA467  ', 'Canada', 1773715708, 1773715708, -79.6206, 43.6792, None, True, 4.89, 351.56, None, None, None, '0610', False, 0]
# ['738075', 'ELY1025 ', 'Israel', 1773715961, 1773715961, -71.7943, 42.1851, 5707.38, False, 185.57, 286.43, -4.23, None, 5707.38, None, False, 0]
# ['c058be', 'ACA808  ', 'Canada', 1773715961, 1773715961, -74.3502, 45.248, 9441.18, False, 292.39, 69.4, 0, None, 9395.46, '2231', False, 0]
# ['c080db', 'ACA1161 ', 'Canada', 1773715931, 1773715931, -79.6207, 43.6734, None, True, 4.12, 202.5, None, None, None, None, False, 0]
# ['a423d7', 'DAL2488 ', 'United States', 1773715961, 1773715961, -95.2464, 44.9825, 8717.28, False, 218.86, 272.56, 7.48, None, 8420.1, None, False, 0]
# ['a34c68', 'ENY3564 ', 'United States', 1773715961, 1773715961, -82.2904, 42.3388, 8839.2, False, 248.61, 83.35, -0.33, None, 8321.04, None, False, 0]
# ['ad6758', 'AAL2250 ', 'United States', 1773715961, 1773715961, -74.3985, 42.4093, 5791.2, False, 205.4, 97.34, 0, None, 5684.52, '3277', False, 0]
# ['ab5ade', 'SWA3988 ', 'United States', 1773715961, 1773715961, -89.3158, 46.7809, 9448.8, False, 237.68, 90.25, 0, None, 8884.92, '3267', False, 0]
# ['a005b3', 'N100LE  ', 'United States', 1773715961, 1773715961, -111.8496, 41.7762, 1318.26, False, 37.61, 3.14, -2.6, None, 1394.46, None, False, 0]
# ['a11eb4', 'UPS1013 ', 'United States', 1773715961, 1773715961, -70.9047, 42.2309, 4953, False, 199.8, 276.36, 14.63, None, 4937.76, None, False, 0]
# ['adaee8', 'AAL2804 ', 'United States', 1773715961, 1773715961, -82.5639, 42.5102, 9448.8, False, 268.34, 52.71, -0.33, None, 8953.5, '3446', False, 0]
# ['a0b81d', '', 'United States', 1773715949, 1773715949, -87.908, 41.9797, None, True, 5.92, 8.44, None, None, None, None, False, 0]
# ['c02029', 'MAL7062 ', 'Canada', 1773715961, 1773715961, -114.3024, 51.0811, 3398.52, False, 172.21, 20.28, -11.7, None, 3291.84, None, False, 0]
# ['c02028', 'MAL7082 ', 'Canada', 1773715961, 1773715962, -77.6896, 44.5129, 10363.2, False, 175.86, 239.98, 0.33, None, 10142.22, '0643', False, 0]
# ['c080a6', 'WJA2605 ', 'Canada', 1773715961, 1773715961, -111.0387, 51.5081, 10972.8, False, 163.67, 329.81, 0, None, 11049, None, False, 0]
# ['a3539d', 'SKW3817 ', 'United States', 1773715961, 1773715961, -120.5532, 46.0726, 10668, False, 272.36, 127.32, 0, None, 11026.14, None, False, 0]


# info_aircrafts = [['4b1809', 'SWR8KY  ', 'Switzerland', 1773716158, 1773716158, 8.5586, 47.4535, None, True, 0, 5.62, None, None, None, None, False, 0], ['a4d881', 'N411GV  ', 'United States', 1773715893, 1773715893, -151.2473, 60.5653, None, True, 3.09, 25.31, None, None, None, '0525', False, 0], ['a7e8bf', 'ASA64   ', 'United States', 1773716162, 1773716162, -123.131, 48.3466, 5989.32, False, 203.29, 148.24, -11.7, None, 6118.86, None, False, 0], ['aa56b5', 'UAL263  ', 'United States', 1773716162, 1773716162, -78.8414, 42.9609, 1508.76, False, 148.43, 45.84, -3.25, None, 1272.54, '3134', False, 0], ['4b180c', 'SWR     ', 'Switzerland', 1773716157, 1773716159, 8.558, 47.4542, None, True, 0, 185.62, None, None, None, '2000', False, 0], ['a2cba6', 'TWY84   ', 'United States', 1773716162, 1773716162, -75.8422, 41.3163, 6393.18, False, 189.18, 110.7, -8.13, None, 6248.4, '1753', False, 0], ['ad4f72', 'JBU8052 ', 'United States', 1773716162, 1773716162, -70.9931, 42.3896, 243.84, False, 68.66, 199.25, -3.58, None, 99.06, '1033', False, 0], ['ae26ad', 'C6587   ', 'United States', 1773716089, 1773716089, -122.9362, 48.509, 144.78, False, 49.9, 180, -0.65, None, 129.54, None, False, 0], ['511171', 'MBU6146 ', 'Estonia', 1773716162, 1773716162, 20.3342, 43.2532, 10652.76, False, 225.6, 139.81, 0, None, 10561.32, '6022', False, 0], ['abb3be', 'DAL1    ', 'United States', 1773716161, 1773716162, -62.2803, 43.8363, 10058.4, False, 277.37, 66.38, 0, None, 10347.96, None, False, 0], ['4952a6', 'TAP238  ', 'Portugal', 1773715936, 1773715938, -111.1931, 42.7665, 11277.6, False, 239.82, 69.27, 0, None, 11643.36, None, False, 0], ['aae34c', 'EJA800  ', 'United States', 1773716162, 1773716162, -84.0987, 41.4531, 13106.4, False, 233.37, 273.03, -0.33, None, 12832.08, '3350', False, 0], ['3c6676', 'DLH1331 ', 'Germany', 1773716162, 1773716162, -2.3965, 42.4272, 10980.42, False, 221.6, 25.43, 0, None, 11170.92, '6441', False, 0], ['a39bfa', 'UAL1702 ', 'United States', 1773716162, 1773716162, -88.9444, 41.968, 9448.8, False, 248.48, 80.95, 0, None, 8907.78, None, False, 0], ['a35592', 'JBU860  ', 'United States', 1773716162, 1773716162, -70.928, 42.5237, 1097.28, False, 64.79, 200.45, -3.58, None, 960.12, '2674', False, 0], ['408142', 'DHK705  ', 'United Kingdom', 1773716162, 1773716162, -72.7412, 43.5351, 10363.2, False, 212.36, 256.27, 0.33, None, 10401.3, '0702', False, 0], ['a798b9', 'LBQ792  ', 'United States', 1773715945, 1773716112, -77.662, 43.1176, None, True, 0.77, 230.62, None, None, None, None, False, 0], ['a3556f', 'JBU247  ', 'United States', 1773716162, 1773716162, -106.4372, 43.0526, 10972.8, False, 227.29, 252.34, 0, None, 11201.4, '3260', False, 0], ['c01b6c', 'JZA52   ', 'Canada', 1773716162, 1773716162, -65.7813, 45.4364, 708.66, False, 67.7, 216.35, 0.33, None, 647.7, '6347', False, 0], ['a69b92', 'ASA2    ', 'United States', 1773716162, 1773716162, -89.7872, 42.0311, 11277.6, False, 254.66, 113.2, 0.33, None, 10850.88, None, False, 0], ['a04431', 'N116TL  ', 'United States', 1773716162, 1773716162, -149.9915, 61.2252, 487.68, False, 51.59, 343.19, -0.98, None, 281.94, None, False, 0], ['4b187b', 'SWR15X  ', 'Switzerland', 1773716162, 1773716162, -69.61, 41.7676, 10972.8, False, 272.06, 65.18, 0.33, None, 11193.78, '1716', False, 0], ['ade106', 'N9936V  ', 'United States', 1773716152, 1773716152, -121.198, 44.0752, 1165.86, False, 33.94, 194.04, 2.28, None, 1211.58, None, False, 0], ['accd69', 'DAL2377 ', 'United States', 1773716162, 1773716162, -106.2756, 41.8738, 10751.82, False, 224.18, 263.54, -4.88, None, 10980.42, '3171', False, 0], ['3c65ab', 'DLH773  ', 'Germany', 1773716162, 1773716162, 23.1606, 45.4784, 12192, False, 241.91, 292.64, 0, None, 12070.08, '3256', False, 0], ['4b1887', 'SWR9G   ', 'Switzerland', 1773716096, 1773716110, -83.3583, 45.5772, 10668, False, 264.07, 47.92, 0, None, 10195.56, None, False, 0], ['4b1881', 'SWR23A  ', 'Switzerland', 1773716141, 1773716161, -57.0105, 44.6537, 11887.2, False, 259.08, 74.8, 0, None, 12161.52, None, False, 0], ['3c65c4', 'DLH2559 ', 'Germany', 1773716162, 1773716162, 43.2415, 41.8856, 8442.96, False, 232.49, 273.68, 6.5, None, 8458.2, '6755', False, 0], ['a94b2e', 'UAL8117 ', 'United States', 1773716162, 1773716162, -105.365, 41.4672, 9144, False, 186.03, 331.24, 0, None, 9319.26, '3763', False, 0], ['a34291', 'UPS236  ', 'United States', 1773716162, 1773716162, 6.7544, 50.7084, 6736.08, False, 193.11, 288, 14.96, None, 6789.42, '4111', False, 0], ['a7c2cd', 'N6CP    ', 'United States', 1773716162, 1773716162, -7.9206, 50.0368, 12496.8, False, 280.5, 97.16, 0.65, None, 12573, None, False, 0], ['a38a05', 'N327TL  ', 'United States', 1773716162, 1773716162, -84.7886, 41.9215, 13716, False, 255.28, 84.57, -0.33, None, 13434.06, '1042', False, 0], ['a091d5', 'DAL567  ', 'United States', 1773716162, 1773716162, -78.5371, 42.3257, 9753.6, False, 252.42, 297.56, -0.33, None, 9494.52, '1524', False, 0], ['a808df', 'N617BG  ', 'United States', 1773716149, 1773716158, -122.2176, 47.4938, None, True, 0, 354.38, None, None, None, None, False, 0], ['a0311d', 'DAL1105 ', 'United States', 1773716162, 1773716162, -122.3079, 47.442, 228.6, False, 74.6, 179.21, 12.68, None, 228.6, None, False, 0], ['aa43c4', 'RPA3564 ', 'United States', 1773716162, 1773716162, -76.0301, 42.3922, 7940.04, False, 181.32, 121.66, -5.85, None, 7802.88, None, False, 0], ['0d0abf', 'VOI1850 ', 'Mexico', 1773716162, 1773716162, -122.7253, 46.4163, 7749.54, False, 210.48, 358.46, -13.33, None, 8016.24, '1317', False, 0], ['a58de0', 'UAL457T ', 'United States', 1773716161, 1773716161, -95.8531, 41.2579, 518.16, False, 63.81, 324.52, -3.9, None, 556.26, None, False, 0], ['c03517', 'WJA2153 ', 'Canada', 1773716162, 1773716162, -122.0842, 47.3421, 10972.8, False, 212.54, 347.28, 0, None, 11285.22, '6630', False, 0], ['a4c4bb', 'UPS991  ', 'United States', 1773716162, 1773716162, -117.8479, 46.0277, 11087.1, False, 252.46, 183.15, 8.13, None, 11445.24, None, False, 0], ['a00929', 'RPA4336 ', 'United States', 1773716162, 1773716162, -86.7609, 42.1235, 6339.84, False, 199.33, 87.19, 9.1, None, 5897.88, None, False, 0], ['ad072a', 'DAL1620 ', 'United States', 1773716162, 1773716162, -83.2616, 42.2186, 609.6, False, 57.1, 270, -3.9, None, 480.06, None, False, 0], ['accd09', 'N924AC  ', 'United States', 1773716161, 1773716162, -150.0594, 60.9774, 1036.32, False, 90.34, 37.13, -1.95, None, 777.24, None, False, 0], ['a70aa1', 'ASA552  ', 'United States', 1773716162, 1773716162, -122.6869, 46.1403, 7993.38, False, 199.42, 352.14, -9.75, None, 8267.7, '1355', False, 0], ['86d5c3', 'APJ567  ', 'Japan', 1773716162, 1773716162, 141.3934, 42.0026, 3352.8, False, 155.29, 26.57, -7.8, None, 3307.08, '2043', False, 0], ['495305', 'TAP211  ', 'Portugal', 1773716162, 1773716162, -72.5011, 41.9582, 5059.68, False, 168.46, 262.98, 0, None, 5013.96, None, False, 0]]
