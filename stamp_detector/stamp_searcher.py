"""
Программа выполняет поиск местоположения объекта на изображении по его образцу
Обязательные аргументы - путь к файлу образца, путь к файлу, на котором ищется объект
Опциональный аргумент (-d {1,2}) - выбор детектора SIFT или SURF
"""
import cv2 as cv
import numpy as np
import argparse


def stamp_detector(sample, test, detector=1):
    """
    Осуществляет поиск объекта (штампа) на изображении. Если соответствие найдено,
    возвращает местоположения объекта (координаты угловых точек), в противном случае
    возвращат пустой массив.
    """
    # минимальное количество соответствий
    min_match_count = 15
    # Порог детектора SURF    
    minHessian = 400
    # Параметры дескриптора FLANN
    flann_index_kdtree = 0
    index_params = dict(algorithm=flann_index_kdtree, trees=5)
    search_params = dict(checks=50)

    # Выбор детектора
    if detector == 1:
        det = cv.xfeatures2d.SIFT_create()
    elif detector == 2:
        det = cv.xfeatures2d_SURF.create(hessianThreshold=minHessian)

    # Выделение признаков
    keypoints_s, descr_s = det.detectAndCompute(sample, None)
    keypoints_t, descr_t = det.detectAndCompute(test, None)

    # Поиск соответствий   
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(descr_s, descr_t, k=2)

    # Отбор соответствий
    valid_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            valid_matches.append(m)

    # Если соответствий достаточно, выполняем поиск ПП, затем границ объекта
    if len(valid_matches) > min_match_count:
        sample_pts = np.float32([keypoints_s[m.queryIdx].pt for m in valid_matches]).reshape(-1, 1, 2)
        test_pts = np.float32([keypoints_t[m.trainIdx].pt for m in valid_matches]).reshape(-1, 1, 2)

        # Проективное преобразование, совмещающее образец со своим двойником на тестовом изображении
        homogr_mtrx, mask = cv.findHomography(sample_pts, test_pts, cv.RANSAC, 5.0)

        h, w = sample.shape  # работает только для чёрно-белого изображения
        # Контур (граница) образца
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        # Контур (граница) образца при отображении на плоскость тестового изображения
        dst = cv.perspectiveTransform(pts, homogr_mtrx)
        dst = dst.astype(int)

        return (dst, 'OK')
    else:
        return (np.nan, 'FAIL')


def clearance(rect: np.array, degrees=True):
    """
    Если в качестве аргумента принят массив с координатами четырёхугольника, то
    функция возвращает угол (в градусах или радианах) наклона стороны A[0]A[3].
    """
    side = (rect[3] - rect[0]).reshape(-1)
    angle = np.arctan(side[1] / side[0])
    if degrees:
        return np.around(np.degrees(angle), decimals=2)
    else:
        return np.around(angle, decimals=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sample", type=str, help="path to stamp sample.")
    parser.add_argument("test", type=str, help="path to the processing file.")
    parser.add_argument("-d", "--detector", type=int, choices=[1, 2], default=1,
                        help="Specify feature detector, 1 (default) - SIFT, 2 - SURF.")
    args = parser.parse_args()

    sample = cv.imread(args.sample, 0)
    test = cv.imread(args.test, 0)
    
    border, status = stamp_detector(sample, test, args.detector)
    if status == 'OK':
        angle = clearance(border)
        print(angle, border)
    else:
        print(status)
