from pytesseract import pytesseract
import numpy
from masks import Masks
import cv2
import constants
import re
import shutil
import requests


def convert_plot_to_curve_and_y_axis(img):
    # returns arrays with data
    masks = Masks(img)
    height, width, channels = img.shape
    grid_img = numpy.where(masks.plot_grid_mask(), 255, 0).astype(numpy.uint8).copy()
    _, contours, _ = cv2.findContours(grid_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    curve_img = numpy.where(masks.plot_curve_mask(), 255, 0)
    biggest_contur = [0, 0]
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area > biggest_contur[0]:
            biggest_contur[0] = area
            biggest_contur[1] = contours[i]

    x, y, w, h = cv2.boundingRect(biggest_contur[1])

    start_grid_x = 0
    end_grid_x = 0
    for index, y_axis_array in enumerate(numpy.transpose(grid_img)):
        try:
            if list(y_axis_array).index(255):
                if not start_grid_x:
                    start_grid_x = index
                end_grid_x = index
        except ValueError:
            continue
    start_grid_y = 0
    end_grid_y = 0
    for index, y_axis_array in enumerate(grid_img):
        try:
            if list(y_axis_array).index(255):
                if not start_grid_y:
                    start_grid_y = index
                end_grid_y = index
        except ValueError:
            continue

    curve_img = curve_img[start_grid_y:end_grid_y, start_grid_x:end_grid_x]
    y_axis = img[:, 0:start_grid_x]
    masks = Masks(y_axis)
    # replace blue color with pink
    y_axis[numpy.where(masks.axis_digits_mask())] = constants.PINK_ARRAY
    y, x, d = y_axis.shape
    # make new image with black background
    image = numpy.zeros((y, x*3, 3), numpy.uint8)
    image[:] = constants.BLACK_TUPLE
    M = numpy.float32([[1, 0, x], [0, 1, 0]])
    # using above translation matrix , we shift the image to 20 pixel right and 0 pixel to down
    shifted = cv2.warpAffine(y_axis, M, (image.shape[1], image.shape[0]))  # we get shifted image

    # remove black places after move image
    masks = Masks(shifted)
    shifted[numpy.where(masks.black_mask())] = constants.WHITE_ARRAY
    shifted[numpy.where(masks.plot_curve_mask())] = constants.WHITE_ARRAY
    shifted[numpy.where(masks.pink_mask())] = constants.BLACK_ARRAY
    scale = 150000/(height*width)*constants.RESIZE_SCALE
    shifted = cv2.resize(shifted, (0, 0), fx=scale, fy=scale)
    y_axis = extract_y_axis_values(shifted)
    return curve_img, y_axis


def extract_y_axis_values(image):
    test_str = pytesseract.image_to_string(image, config='--oem 2 --psm 6')
    y_numbers = []
    regex = r"[0-9\-\.]+"
    matches = re.finditer(regex, test_str, re.MULTILINE)

    for matchNum, match in enumerate(matches):
        y_numbers.append(float(match.group()))
    # reject outliers from a list Standard deviation
    m = 2
    numbers = []
    for index, not_error_value in enumerate(abs(y_numbers - numpy.mean(y_numbers)) < m * numpy.std(y_numbers)):
        if not_error_value:
            numbers.append(y_numbers[index])
    return numbers


def get_plot(url, file_name):
    session = requests.session()
    r = session.get(url, stream=True)

    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
