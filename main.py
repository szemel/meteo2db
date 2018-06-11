import cv2
import constants
from random import randint
from time import sleep
from create_db import CreateDatabase
from digitalize import read_plot_image_and_save_to_db
from datetime import timedelta, date, time, datetime
from utils import get_plot

start_day = datetime(2016, 8, 3, 23, 59)
week = timedelta(days=7)
end_day = start_day+week
db = CreateDatabase()
session = db.connect()
for end_date in [datetime(2017, 8, 3, 23, 59)]:
    while start_day < end_date:
        get_plot(constants.PRESSURE_URL % start_day.strftime('%d%m%y'), "PRESSURE_URL.png")
        get_plot(constants.TEMPERATURE_URL % start_day.strftime('%d%m%y'), "TEMPERATURE_URL.png")
        get_plot(constants.WIND_SPEED_URL % start_day.strftime('%d%m%y'), "WIND_SPEED_URL.png")
        get_plot(constants.SOLAR_RADIATION_URL % start_day.strftime('%d%m%y'), "SOLAR_RADIATION_URL.png")
        get_plot(constants.HUMIDITY_URL % start_day.strftime('%d%m%y'), "HUMIDITY_URL.png")
        get_plot(constants.RAIN_URL % start_day.strftime('%d%m%y'), "RAIN_URL.png")

        img = cv2.imread("PRESSURE_URL.png")
        read_plot_image_and_save_to_db(start_day, end_day, img, session, constants.PRESSURE_TYPE)

        img = cv2.imread("TEMPERATURE_URL.png")
        read_plot_image_and_save_to_db(start_day, end_day, img, session, constants.TEMPERATURE_TYPE)

        img = cv2.imread("WIND_SPEED_URL.png")
        read_plot_image_and_save_to_db(start_day, end_day, img, session, constants.WIND_SPEED_TYPE)

        img = cv2.imread("SOLAR_RADIATION_URL.png")
        read_plot_image_and_save_to_db(start_day, end_day, img, session, constants.SOLAR_RADIATION_TYPE)

        img = cv2.imread("HUMIDITY_URL.png")
        read_plot_image_and_save_to_db(start_day, end_day, img, session, constants.HUMIDITY_TYPE)

        img = cv2.imread("RAIN_URL.png")
        read_plot_image_and_save_to_db(start_day, end_day, img, session, constants.RAIN_TYPE)
        print(str(end_day))
        start_day += week
        end_day = start_day+week
    start_day = end_date
    sleep(randint(1, 10))
