from bs4 import BeautifulSoup
import datetime


class WeatherMaker:

    def __init__(self, html):
        self.html = html

    def get_content(self):
        weather = []
        soup = BeautifulSoup(self.html, 'html.parser')
        items = soup.select('[data-text]')
        date = datetime.datetime.today().date()
        for item in items:
            weather.append(
                {
                    'weather': item.attrs['data-text'],
                    'temperature': item.find('span', class_='value unit unit_temperature_c').get_text(strip=True),
                    'date': date
                }
            )
            date += datetime.timedelta(days=1)
        return weather
