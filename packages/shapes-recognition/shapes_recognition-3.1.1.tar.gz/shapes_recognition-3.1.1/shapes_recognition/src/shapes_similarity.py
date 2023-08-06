import sys
import cv2 as cv
import numpy as np

from shapes_recognition.src import cfg
from shapes_recognition.src.get_peaks import get_peaks
from shapes_recognition.src.create_table import create_table
from shapes_recognition.src.create_joint_table import create_joint_table


def shapes_similarity(image: np.uint8, templ: np.uint8) -> float:

    image_magn_roi = get_magn_roi(image)
    image_magn_half = get_magn_half(image_magn_roi)
    image_list_of_peaks = get_peaks(image_magn_half)
    image_table, n_image_table_rows = create_table(image_list_of_peaks)

    if n_image_table_rows == 0:
        print(f'\nERROR: ' + cfg.path_image + ' - unacceptable shape')
        sys.exit(1)

    templ_magn_roi = get_magn_roi(templ)
    templ_magn_half = get_magn_half(templ_magn_roi)
    templ_list_of_peaks = get_peaks(templ_magn_half)
    templ_table, n_templ_table_rows = create_table(templ_list_of_peaks)

    if n_templ_table_rows == 0:
        print(f'\nERROR: ' + cfg.path_templ + ' - unacceptable shape')
        sys.exit(1)

    joint_table, n_joint_table_rows = \
        create_joint_table(image_table, n_image_table_rows,
                           templ_table, n_templ_table_rows)

    if n_joint_table_rows == 0:
        print(f"\nERROR: " + cfg.path_image + "  vs.  " + cfg.path_templ + " - we can't compare")
        sys.exit(1)

    similarity = shapes_similarity_a(
                        image_magn_roi, templ_magn_roi,
                        joint_table, n_joint_table_rows)

    return similarity


def get_magn_roi(any_image: np.uint8):

    height, width = any_image.shape

    array_dft = \
        np.zeros((cfg.size_dft, cfg.size_dft), dtype=np.float32)

    array_dft[0:height:, 0:width:] = any_image[0::, 0::]

    dft = cv.dft(array_dft, flags=cv.DFT_COMPLEX_OUTPUT)

    dft_shift = np.fft.fftshift(dft)

    re_shift = dft_shift[:, :, 0]
    im_shift = dft_shift[:, :, 1]

    re_roi = np.zeros((cfg.size_roi, cfg.size_roi), dtype=np.float32)
    im_roi = np.zeros((cfg.size_roi, cfg.size_roi), dtype=np.float32)
    magn_roi_norm = np.zeros((cfg.size_roi, cfg.size_roi), dtype=np.float32)

    y0 = (cfg.size_dft - cfg.size_roi) // 2
    x0 = y0

    re_roi[0:cfg.size_roi:, 0:cfg.size_roi:] = \
        re_shift[y0:y0+cfg.size_roi:, x0:x0+cfg.size_roi:]
    im_roi[0:cfg.size_roi:, 0:cfg.size_roi:] = \
        im_shift[y0:y0+cfg.size_roi:, x0:x0+cfg.size_roi:]

    magn_roi = cv.magnitude(re_roi, im_roi)

    cv.normalize(magn_roi, magn_roi_norm, 0, 255, cv.NORM_MINMAX)

    return magn_roi_norm


def get_magn_half(magn_roi: np.ndarray):

    size_roi_half_1 = cfg.size_roi_half + 1

    shape_magn_half = (size_roi_half_1, cfg.size_roi)

    magn_half = np.empty(shape_magn_half, dtype=np.float32)

    magn_half[0:size_roi_half_1, 0:cfg.size_roi] = \
        magn_roi[0:size_roi_half_1:, 0::]

    return magn_half


def shapes_similarity_a(
        image_magn, templ_magn,
        joint_table, joint_table_rows) -> float:

    similarity_max: float = 0

    for n in range(joint_table_rows):

        y1_image = joint_table[n, 0]
        x1_image = joint_table[n, 1]
        y2_image = joint_table[n, 2]
        x2_image = joint_table[n, 3]

        y1_templ = joint_table[n, 4]
        x1_templ = joint_table[n, 5]
        y2_templ = joint_table[n, 6]
        x2_templ = joint_table[n, 7]

        y_blue_in = y1_image
        x_blue_in = x1_image
        y_red_in = y2_image
        x_red_in = x2_image

        pts_image = np.float32([[x_red_in, y_red_in],
                                [x_blue_in, y_blue_in],
                                [cfg.X0, cfg.Y0]])

        y_blue_out = y1_templ
        x_blue_out = x1_templ
        y_red_out = y2_templ
        x_red_out = x2_templ

        pts_templ = np.float32([[x_red_out, y_red_out],
                                [x_blue_out, y_blue_out],
                                [cfg.X0, cfg.Y0]])

        mat_affine = cv.getAffineTransform(pts_image, pts_templ)

        image_magn_warped = cv.warpAffine(
                                    image_magn,
                                    mat_affine,
                                    image_magn.shape)

        similarity_current = \
            shapes_similarity_b(image_magn_warped, templ_magn)

        if similarity_current > similarity_max:
            similarity_max = similarity_current

    return similarity_max


def shapes_similarity_b(
        magnitude_1: np.float32,
        magnitude_2: np.float32) -> float:

    arr_min = np.minimum(magnitude_1, magnitude_2)
    arr_max = np.maximum(magnitude_1, magnitude_2)

    similarity_map = \
        np.divide(arr_min, arr_max,
                  out=np.zeros_like(arr_min),
                  where=arr_max > float(0))

    similarity = np.sum(similarity_map) / np.count_nonzero(similarity_map)

    return similarity
