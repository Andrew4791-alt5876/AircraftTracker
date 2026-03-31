# Курсовая работа на Python

# 📋 Содержание

1. Название проекта и описание
2. Требования
3. Установка (клонирование, виртуальное окружение, зависимости)
4. Запуск (основные функции)
5. Тестирование 
6. Линтеры и форматирование 
7. Структура проекта 
8. Примеры использования 
9. Лицензия 
10. Контакты

## 📖 Название проекта и описание

Программа для получения информации о самолетах в воздушном пространстве выбранных стран
с использованием открытых API (OpenSky Network, Nominatim). 
Данные сохраняются в JSON-файл и могут быть в дальнейшем обработаны.

### Трекер самолётов
- Запрашивает у пользователя список стран.
- Получает географические координаты (bounding box) для каждой страны через Nominatim API.
- С помощью OpenSky Network API получает данные о текущих самолетах в этих зонах.
- Создает объекты `Aircraft` с информацией о каждом самолете.
- Позволяет сортировать самолеты по высоте, фильтровать по стране регистрации и по диапазону высот.
- Выводит топ N самолетов после каждой фильтрации.
- Сохраняет выбранный набор данных в JSON-файл (с датой в имени файла).
- Поддерживает последующую загрузку, фильтрацию и удаление записей через класс `JSONSaver`.

## 📖 Требования
- Python 3.13 или выше
- Установленный Git

Основные требования расположены в файле
```
requirements.txt
```
### Основные функциональные зависимости
requests==2.32.5 – HTTP-клиент для обращения к API OpenSky и Nominatim
certifi==2026.2.25 – сертификаты SSL для requests
charset-normalizer==3.4.6 – нормализация кодировок (транзитивная зависимость requests)
idna==3.11 – поддержка интернациональных доменных имён (транзитивная)
urllib3==2.6.3 – низкоуровневый HTTP-клиент (транзитивная)

### Инструменты форматирования кода
black==26.3.1 – автоматическое форматирование кода по стандарту PEP 8
isort==8.0.1 – сортировка импортов

### Линтинг и статический анализ
flake8==7.3.0 – агрегатор линтеров (pycodestyle, pyflakes, mccabe)
pycodestyle==2.14.0 – проверка стиля кода
pyflakes==3.4.0 – проверка логических ошибок
mccabe==0.7.0 – анализ циклометрической сложности

### Тестирование и покрытие
pytest==9.0.2 – фреймворк для модульного тестирования
pytest-cov==7.1.0 – плагин для измерения покрытия кода
coverage==7.13.5 – инструмент для анализа покрытия
pluggy==1.6.0 – система плагинов, используется pytest
iniconfig==2.3.0 – парсинг конфигурационных файлов (транзитивная)
packaging==26.0 – утилиты для работы с версиями пакетов (транзитивная)

### Типизация
mypy==1.19.1 – статическая проверка типов
mypy_extensions==1.1.0 – расширения для mypy
typing_extensions==4.15.0 – обратная совместимость для типов
types-requests==2.32.4.20260107 – заглушки типов для requests

## 📖 Установка (клонирование, виртуальное окружение, зависимости)
1. **Клонируйте репозиторий**
   ```
   git clone https://github.com/Andrew4791-alt5876/AircraftTracker.git
   ```
2. **Создайте виртуальное окружение и активируйте его:**
   ```
   python -m venv venv

   source venv/bin/activate      # для Linux/macOS

   venv\Scripts\activate     # для Windows
   ```
3. **Установите зависимости:**
   ```
   pip install -r requirements.txt
   poetry instal
   ```
   **Для разработки также рекомендуется установить группы зависимостей (линтеры, тесты):**
   ```
   pip install -e . --group dev --group lint
   ```

## 📖 Запуск (основные функции)
### Запуск выполняется через запуск файла:
```
main.py
```
### Программа выполнит следующие шаги:
1. Приветствие в зависимости от времени суток.
2. Показ списка стран (данные из data_countries.py).
3. Запрос названий стран (ввод с клавиатуры, для завершения ввода введите 0).
4. Получение координат стран через Nominatim API.
5. Запрос данных о самолетах через OpenSky Network API.
6. Создание объектов Aircraft.
7. Сортировка по высоте (вопрос: y/n – от минимальной к максимальной или наоборот).
8. Вывод топ N самолетов.
9. Фильтрация по стране регистрации (пользователь выбирает из уникальных стран в текущем наборе).
10. Вывод топ N после фильтрации по стране.
11. Фильтрация по диапазону высот (ввод через дефис или пробел).
12. Вывод топ N после фильтрации по высоте.
13. Выбор набора данных для сохранения:
    1 – все самолеты из выбранных стран 
    2 – отфильтрованные по стране регистрации
    3 – отфильтрованные по диапазону высот
    4 – ничего не сохранять
14. Сохранение выбранных данных в JSON-файл с именем data/aircraft_YYYYMMDD.json.

## 📖 Тестирование
Проект покрыт тестами pytest.
1. Запуск всех тестов:
```
pytest
```
2. Запуск с детальным выводом:
```
pytest -v
```
3. Запуск конкретного тестового файла
```
pytest tests/test_aircrafts.py
```
4. Запуск конкретного теста:
```
pytest tests/test_aircrafts.py::test_squawk_default -v
```
5. Запуск с покрытием кода:
```
pytest --cov=src --cov-report=html
```
6. Создание отчета о проверке:
```
poetry run pytest --cov
```
7. Расположение отчета в HTML-формате: 
```
В папке 'htmlcov' в модуле 'index.html'
```

## 📖 Линтеры и форматирование
### Для поддержания качества кода используются:
black – форматирование
isort – сортировка импортов (совместим с black)
flake8 – линтинг
mypy – статическая типизация

### Запустить форматирование:
```
black src/ tests/
isort src/ tests/
```
### Проверить стиль и типы:
```
flake8 src/ tests/
mypy src/ tests/
```

## 📖 Структура проекта
project/
├── data/                       # Папка для сохранения JSON-файлов (создается автоматически)
├── src/                        # Исходный код
│   ├── __init__.py
│   ├── aircrafts.py            # Класс Aircraft с методами to_dict/from_dict
│   ├── base_api.py             # Абстрактный класс APIClient
│   ├── json_saver.py           # Реализация Saver для JSON-файла
│   ├── nominatim.py            # Клиент для Nominatim API
│   ├── openSky_network.py      # Клиент для OpenSky Network API
│   └── saver.py                # Абстрактный класс Saver
├── tests/                      # Модульные тесты
│   ├── test_aircrafts.py       # Тесты для класса Aircraft 
│   ├── test_base_api.py        # Тесты для абстрактного класса APIClient
│   ├── test_json_saver.py      # Тесты для класса JSONSaver
│   ├── test_nominatim.py       # Тесты для класса NominatimClient
│   └── test_openSky_network.py # Тесты для класса OpenSkyClient
├── .flake8                     # Конфигурация линтера 
├── .gitignore                  # Git игнор 
├── data_countries.py           # Список стран для отображения пользователю
├── main.py                     # Главный модуль для запуска приложения
├── poetry.lock                 # Автоматически генерируемый файл poetry
├── poetry.toml                 # Конфигурация проекта и зависимостей 
├── pyproject.toml              # Конфигурация проекта и зависимостей 
├── README.md                   # Этот файл
└── requirements.txt            # Зависимости

## 📖 Примеры использования
Запускается файл main.py в корне проекта и 
пользователь вводит данные, которые запрашивает приложение.

### Пример работы
```
Добрый день!
Добро пожаловать в программу, которая собирает данные о самолетах
в воздушных пространствах тех стран, которые вы выберете.
Пример стран из списка:
['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia']
['Austria', 'Azerbaijan', 'The Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize']
['Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso']
['Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'China']
['Colombia', 'Comoros', 'The Republic of the Congo', 'The Democratic Republic of the Congo', 'Costa Rica', 'Cote d’Ivoire', 'Croatia', 'Cuba', 'Cyprus']
['Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador']
['Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'The Gambia']
['Georgia', 'Germany', 'Ghana', 'GB', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau']
['Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq']
['Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati']
['North Korea', 'South Korea', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho']
['Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives']
['Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Federated States of Micronesia', 'Moldova', 'Monaco']
['Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'The Netherlands']
['New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama']
['Papua New Guinea', 'Paraguay', 'Peru', 'The Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia']
['Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal']
['Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa']
['South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria']
['Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey']
['Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'UAE', 'USA', 'Uruguay', 'Uzbekistan', 'Vanuatu']
['Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']
Для прекращения ввода введите цифру 0
Введите название страны: Russia
Вы ввели Russia
Для прекращения ввода введите цифру 0
Введите название страны: 0
Над ['Russia'] находится 378 самолетов.
Вам необходима сортировка самолетов от минимальной высоты и выше?: y/n 3
Введите количество самолетов для вывода в топ N: 3
Aircraft(id_aircraft='50034e', callsign='T7ADA', country='San Marino', lat=46.9518, lon=20.357, vert_rate=-4.88, vel=264.8, alt=13845.54, true_track=293.23, squawk='1000', on_ground=False)
Aircraft(id_aircraft='acae14', callsign='N916MM', country='United States', lat=48.112, lon=22.2794, vert_rate=0.0, vel=263.51, alt=13091.16, true_track=316.9, squawk='1000', on_ground=False)
Aircraft(id_aircraft='4bb0e2', callsign='THY801', country='Turkey', lat=42.9879, lon=24.2503, vert_rate=0.0, vel=263.43, alt=12466.32, true_track=116.82, squawk='2355', on_ground=False)
******************************************************************************************************************************************************
Для сортировки самолетов по стране регистрации скопируйте страну из списка: 
('Italy', 'Bulgaria', 'Egypt', 'Kingdom of the Netherlands', 'Turkey', 'Ukraine', 'Israel', 'Taiwan', 'Switzerland')
('Czech Republic', 'Republic of Moldova', 'Zambia', 'Poland', 'Greece', 'Canada', 'Denmark', 'Latvia', 'Luxembourg')
('Romania', 'Ireland', 'Japan', 'Singapore', 'Finland', 'Sweden', 'Norway', 'United States', 'Belarus')
('Kazakhstan', 'Bangladesh', 'Lebanon', 'Azerbaijan', 'Bahrain', 'Uzbekistan', 'Malaysia', 'Germany', 'Hungary')
('Australia', 'Turkmenistan', 'United Kingdom', 'San Marino', 'Lithuania', 'United Arab Emirates', 'Viet Nam', 'Armenia', 'Russian Federation')
('Malta', 'Republic of Korea', 'Austria', 'Spain', 'China', 'Georgia', 'Slovakia', 'France', 'Serbia')
Для прекращения ввода введите цифру 0
Введите название страны: Russian Federation
Вы ввели Russian Federation
Для прекращения ввода введите цифру 0
Введите название страны: 0
Получилось 37 самолетов по стране регистрации
Введите количество самолетов для вывода в топ N: 5
Aircraft(id_aircraft='151e58', callsign='PBD6838', country='Russian Federation', lat=59.8813, lon=25.5025, vert_rate=0.0, vel=248.8, alt=11765.28, true_track=76.37, squawk='6636', on_ground=False)
Aircraft(id_aircraft='151de4', callsign='SDM6602', country='Russian Federation', lat=46.3346, lon=52.6933, vert_rate=0.33, vel=218.77, alt=11498.58, true_track=218.89, squawk='0000', on_ground=False)
Aircraft(id_aircraft='151efb', callsign='SBI8872', country='Russian Federation', lat=65.6527, lon=61.8232, vert_rate=0.0, vel=216.98, alt=11277.6, true_track=242.46, squawk='0000', on_ground=False)
Aircraft(id_aircraft='151e0e', callsign='PBD6832', country='Russian Federation', lat=59.8931, lon=25.6057, vert_rate=0.0, vel=252.54, alt=11140.44, true_track=76.33, squawk='6634', on_ground=False)
Aircraft(id_aircraft='151dad', callsign='AFL1745', country='Russian Federation', lat=60.5604, lon=44.8803, vert_rate=0.0, vel=224.3, alt=11018.52, true_track=232.74, squawk='0000', on_ground=False)
******************************************************************************************************************************************************
Введите диапазон высот полета (нижняя-верхняя через дефис или пробел): 10000 20000
Получилось 221 самолетов в диапазоне выбранных высот
Введите количество самолетов для вывода в топ N: 5
Aircraft(id_aircraft='50034e', callsign='T7ADA', country='San Marino', lat=46.9518, lon=20.357, vert_rate=-4.88, vel=264.8, alt=13845.54, true_track=293.23, squawk='1000', on_ground=False)
Aircraft(id_aircraft='acae14', callsign='N916MM', country='United States', lat=48.112, lon=22.2794, vert_rate=0.0, vel=263.51, alt=13091.16, true_track=316.9, squawk='1000', on_ground=False)
Aircraft(id_aircraft='4bb0e2', callsign='THY801', country='Turkey', lat=42.9879, lon=24.2503, vert_rate=0.0, vel=263.43, alt=12466.32, true_track=116.82, squawk='2355', on_ground=False)
Aircraft(id_aircraft='5003b3', callsign='EAA7G', country='San Marino', lat=42.9733, lon=22.9403, vert_rate=-0.33, vel=281.92, alt=12435.84, true_track=89.58, squawk='6027', on_ground=False)
Aircraft(id_aircraft='4acac2', callsign='SWE42B', country='Sweden', lat=64.3304, lon=21.3056, vert_rate=4.88, vel=190.23, alt=12245.34, true_track=199.76, squawk='0000', on_ground=False)
******************************************************************************************************************************************************
Для сохранения данных в файл сделайте введите соответствующий пункт:
    1) Сохранить базу данных всех самолетов находящихся в пределах выбранных стран
    2) Сохранить базу данных самолетов, выбранных по стране регистрации
    3) Сохранить базу данных самолетов, выбранных по диапазону высот
    4) Ничего не сохранять (можно ничего не вводить)
Сделайте свой выбор: 2

```
## 📄 Лицензия:

## 👥 Авторы:
```
Тюрин Андрей Алексеевич - основной разработчик
```

## 📞 Контакты:
```
Email: tyrandr@list.ru

GitHub: Andrew4791-alt5876

Issue Tracker: Issues
```
