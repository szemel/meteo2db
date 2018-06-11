import time
import numpy as np
from create_db import MeteoData
from utils import convert_plot_to_curve_and_y_axis


def read_plot_image_and_save_to_db(start_day, end_day, img, session, plot_type):
    start = time.time()

    curve_img, y_axis = convert_plot_to_curve_and_y_axis(img)
    if len(y_axis):
        y_min = min(y_axis)
        y_max = max(y_axis)

        real_y_value = lambda y_val, y_axis: y_min + ((y_max - y_min) / len(y_axis) * y_val)
        test = []
        # days = []
        y, w = curve_img.shape
        time_delta = (end_day - start_day) / w
        for index, y_axis_array in enumerate(np.transpose(curve_img)):
            try:
                if list(y_axis_array).index(255):
                    y_val = len(list(y_axis_array)) - np.mean(np.argwhere(y_axis_array == 255))
                else:
                    continue
            except ValueError:
                continue
            time_stamp = time_delta * index
            if (start_day + time_stamp) > end_day:
                break
            test.append(real_y_value(y_val, y_axis_array))
            record = MeteoData(value=real_y_value(y_val, y_axis_array), when=start_day + time_stamp, type=plot_type)

            session.add(record)
            session.commit()

    end = time.time()
    print(end - start)
