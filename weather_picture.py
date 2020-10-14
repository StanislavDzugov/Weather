import cv2
import numpy as np


def create_foreground(filename):
    foreground = cv2.imread(filename, -1)
    foreground_height = foreground.shape[0]
    foreground_width = foreground.shape[1]
    x = np.zeros((32, 32, 3))
    for i in range(foreground_height):
        for j in range(foreground_width):
            if foreground[i][j][3] > 0:
                x[i][j] = foreground[i][j][:3]
            else:
                x[i][j] = np.array([255, 255, 255])
    return x


def create_background(filename, weather):
    background = cv2.imread(filename)
    pixels = 0
    foreground_height = 32
    foreground_width = 32
    for day, value in enumerate(weather):
        date = value['date']
        temperature = value['temperature']
        if day in [8, 16, 24]:
            pixels = 0
        if day <= 7:
            start = 0
            multiplier = 1
        elif 7 < day <= 15:
            start = 64
            multiplier = 3
        elif 15 < day <= 23:
            start = 128
            multiplier = 5
        else:
            start = 192
            multiplier = 7
        weather_draw(background, multiplier * foreground_height, foreground_width, pixels, start, value, date, temperature)
        pixels += 64
    cv2.imshow('composited image', background)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def weather_draw(background, foreground_height, foreground_width, pixels, start, value, date, temperature):
    sun = 'ясно'
    rain = 'дождь'
    snow = 'снег'
    font = cv2.FONT_HERSHEY_COMPLEX
    step1 = pixels + foreground_width + 5
    step2 = foreground_height + 15
    if rain in value['weather'].lower():
        icon = 'weather_icons/rain.png'
    elif sun in value['weather'].lower():
        icon = 'weather_icons/sun.png'
    elif snow in value['weather'].lower():
        icon = 'weather_icons/snow.png'
    else:
        icon = 'weather_icons/sun_and_clouds.png'
    foreground = create_foreground(icon)
    background[start:foreground_height, pixels:pixels + foreground_width, :] = foreground
    cv2.putText(background, temperature, (step1, start + 20), font, 0.35, (0, 0, 0), 1)
    cv2.putText(background, date.strftime('%d %b'), (pixels, step2), font, 0.35, (0, 0, 0), 1)