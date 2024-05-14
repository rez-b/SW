import cv2
import imutils
import numpy as np
import math
import requests

class Recognizer:
    """распознает фото и выводит данные из ячеек таблицы"""
    def __init__(self, path, column_count,string_count):
        self.path = path
        self.column_count = column_count
        self.string_count = string_count

    def prepare_image(self):
        """загрузка и подготовка изображения"""
        response = requests.get(self.path)
        image_array = np.asarray(bytearray(response.content), dtype = np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        _, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)
        cs = cv2.Canny(thresh, 0, 255)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        closed = cv2.morphologyEx(cs, cv2.MORPH_CLOSE, kernel)

        lines = cv2.HoughLinesP(
            closed, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10
        )
        angle = (
            np.arctan2(lines[0][0][3] - lines[0][0][1], lines[0][0][2] - lines[0][0][0])
            * 180
            / np.pi
        )
        rows, cols = image.shape[:2]
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
        prepare_image = cv2.warpAffine(thresh, M, (cols, rows))
        return prepare_image

    def image_crop(self):
        """Обрезка изображения(таблицы)"""
        contours = cv2.findContours(
            self.prepare_image(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
        )
        contours = imutils.grab_contours(contours)

        def get_max_contours_index(contours):
            """функция для нахождения индекса контура с максимальной областью"""
            max_area = 0
            index_max_area = 0
            iteration = 0
            for cnt in contours:
                contour_area = cv2.contourArea(cnt, True)
                if max_area < contour_area:
                    max_area = contour_area
                    index_max_area = iteration
                iteration = iteration + 1
            return index_max_area

        index_max_area = get_max_contours_index(contours)
        x, y, w, h = cv2.boundingRect(contours[index_max_area])
        ROI = self.prepare_image()[y : y + h, x : x + w]
        return ROI

    def data_sheet(self):
        """вывод данных из ячеек таблицы в лист"""
        cropp = self.image_crop()
        x, y, w, h = cv2.boundingRect(cropp)

        def column_string_size(cell_lenth, row_count):
            """функиця для вычисления размеров ячейки"""
            cell_size = round((cell_lenth / row_count), 1)
            if cell_size * 10 % 10 <= 5:
                cell_size = math.floor(cell_size)
            else:
                cell_size = math.ceil(cell_size)
            return cell_size

        cell_width = column_string_size(w, self.column_count)
        cell_height = column_string_size(h, self.string_count)
        x = 0
        y = 0
        cell_square = cell_width * cell_height
        out_data = []
        for i in range(1, self.string_count + 1):
            for j in range(1, self.column_count + 1):
                cv2.rectangle(
                    cropp,
                    (x, y),
                    (cell_width * j, cell_height * i),
                    (255, 255, 255),
                    int((cell_width + cell_height) // 4),
                )
                roi = cropp[y : y + cell_height, x : x + cell_width]
                black_pixel = np.sum(roi == 0)
                if black_pixel > 0.01 * cell_square:
                    out_data.append(1)
                else:
                    out_data.append(0)
                x = cell_width * j
            x = 0
            y = cell_height * i
        str_out_data = [str(n) for n in out_data]
        return ''.join(str_out_data)


    
