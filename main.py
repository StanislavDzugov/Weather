import requests
from weather_parse import WeatherMaker
from database import DatabaseConnection
from weather_picture import create_background
try:
    from settings import DBNAME, PORT, PASSWORD, HOST1, HOST, URL, HEADERS, USER
except ImportError:
    exit('DO cp settings.py.default settings.py and set token')

def get_html(url, headers, params=None):
    html = requests.get(url, headers=headers, params=params).text
    return html


def create_user_menu():
    menu_options = [
        'Добавить прогнозы за месяц в базу данных',
        'Создать открытку из полученных прогнозов',
        'Вывести прогнозы за месяц на консоль'
    ]
    for index, option in enumerate(menu_options):
        print(f'{index + 1}.{option}')
    while True:
        choice = input('Введите номер варианта:')
        if choice in ['1', '2', '3']:
            break
        else:
            print('Вы ввели неверный номер')
    if choice == '1':
        add_weather_prediction_to_database()
    if choice == '2':
        weather = WeatherMaker(get_html(URL, HEADERS))
        weathers = weather.get_content()
        create_background('weather_icons/background.jpg', weathers)
    if choice == '3':
        print_out_database_info()


def add_weather_prediction_to_database():
    weather = WeatherMaker(get_html(URL, HEADERS))
    weathers = weather.get_content()
    database = DatabaseConnection(DBNAME, USER, HOST1, PORT, PASSWORD, new_data=weathers)
    if database.check_if_table_exists() is False:
        database.create_table()
    database.insert_new_data()


def print_out_database_info():
    print('-' * 90)
    weather = WeatherMaker(get_html(URL, HEADERS))
    weathers = weather.get_content()
    for weather in weathers:
        day_weather = weather['weather']
        day_temperature = weather['temperature']
        day_date = weather['date']
        print(f'Дата:{day_date}  Температура:{day_temperature:3}  Погода:{day_weather}')
    print('-' * 90)


if __name__ == '__main__':
    create_user_menu()
