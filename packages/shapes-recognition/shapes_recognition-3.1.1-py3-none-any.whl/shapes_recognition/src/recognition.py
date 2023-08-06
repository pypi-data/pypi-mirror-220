import numpy as np
import time
from tqdm import tqdm

from shapes_recognition.src import cfg
from shapes_recognition.src.get_column_data import get_column_data
from shapes_recognition.src.shapes_similarity import shapes_similarity


def recognition(list_self_study_out, list_recognition_in):

    time1: float = time.time()

    sl_out_data = get_column_data(list_self_study_out)
    recogn_in_data = get_column_data(list_recognition_in)

    arr_accum = np.empty(cfg.n_types, dtype=np.float32)

    recogn_dictionary = {}

    shape_recogn = np.zeros((cfg.calc_size, cfg.calc_size), dtype=np.uint8)
    shape_sl_out = np.zeros((cfg.calc_size, cfg.calc_size), dtype=np.uint8)

    for n in tqdm(range(cfg.n_items_recognition), desc='recognition'):

        path_recogn = list_recognition_in[n]

        shift_vert = n * cfg.calc_size

        shape_recogn[0::, 0::] = recogn_in_data[
                                        shift_vert:shift_vert + cfg.calc_size:,
                                        0:cfg.calc_size:]
        arr_accum.fill(0)

        for m in range(cfg.n_types):

            for k in range(m * cfg.n_items, (m + 1) * cfg.n_items):

                path_sl_out = list_self_study_out[k]

                shift_vert = k * cfg.calc_size

                shape_sl_out[0::, 0::] = \
                    sl_out_data[shift_vert:shift_vert + cfg.calc_size:,
                                0:cfg.calc_size:]

                cfg.path_image = path_recogn
                cfg.path_templ = path_sl_out
                similarity_1 = shapes_similarity(np.uint8(shape_recogn), np.uint8(shape_sl_out))

                cfg.path_image = path_sl_out
                cfg.path_templ = path_recogn
                similarity_2 = shapes_similarity(np.uint8(shape_sl_out), np.uint8(shape_recogn))

                similarity = min(similarity_1, similarity_2)

                arr_accum[m] += similarity

        index_max = np.argmax(arr_accum)

        match index_max:

            case 0:
                recogn_dictionary[path_recogn] = 'A'

            case 1:
                recogn_dictionary[path_recogn] = 'B'

            case 2:
                recogn_dictionary[path_recogn] = 'C'

            case 3:
                recogn_dictionary[path_recogn] = 'D'

    time2: float = time.time()
    minutes, seconds = divmod(int(time2 - time1), 60)
    cfg.time_recognition = f'{minutes:02d} min  {seconds:02d} sec'

    return recogn_dictionary
